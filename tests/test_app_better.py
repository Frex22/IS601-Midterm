import pytest
import os
import logging
from unittest.mock import patch, MagicMock, mock_open
from app import App

@pytest.fixture
def app_instance():
    """Fixture to create an App instance for testing"""
    with patch('os.makedirs') as mock_makedirs:
        with patch('app.config.load_config') as mock_load_config:
            mock_load_config.return_value = {
                'LOG_LEVEL': 'INFO',
                'LOG_FILE': 'logs/app.log',
                'HISTORY_FILE': 'data/calculation_history.csv',
                'PLUGINS_DIR': 'app/plugins'
            }
            with patch('app.config.setup_logging') as mock_setup_logging:
                yield App()

def test_app_init(app_instance, monkeypatch):
    """Test App initialization"""
    assert app_instance is not None
    assert hasattr(app_instance, 'settings')
    assert hasattr(app_instance, 'history_manager')
    assert hasattr(app_instance, 'command_handler')

def test_app_load_plugins(app_instance, monkeypatch):
    """Test App.load_plugins method"""
    # Mock pkgutil.iter_modules to return a test plugin
    test_modules = [(None, "test_plugin", True)]
    monkeypatch.setattr('pkgutil.iter_modules', lambda _: test_modules)
    
    # Mock importlib.import_module
    mock_import = MagicMock()
    monkeypatch.setattr('importlib.import_module', mock_import)
    
    # Call load_plugins
    app_instance.load_plugins()
    
    # Verify importlib.import_module was called at least once
    assert mock_import.called


def test_app_load_plugins_exception(app_instance, monkeypatch, caplog):
    """Test App.load_plugins handling exceptions"""
    # Mock pkgutil.iter_modules to return a test plugin
    test_modules = [(None, "test_plugin", True)]
    monkeypatch.setattr('pkgutil.iter_modules', lambda _: test_modules)
    
    # Mock importlib.import_module to raise an exception
    def mock_import_error(_):
        raise ImportError("Test import error")
    monkeypatch.setattr('importlib.import_module', mock_import_error)
    
    # Call load_plugins with error logging captured
    with caplog.at_level(logging.ERROR):
        app_instance.load_plugins()
    
    # Verify error was logged
    assert "Failed to load plugin" in caplog.text

def test_app_start(app_instance, monkeypatch):
    """Test App.start method"""
    # Mock load_plugins
    app_instance.load_plugins = MagicMock()
    
    # Mock input to simulate exit command
    inputs = iter(["exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    
    # Test start method raises SystemExit
    with pytest.raises(SystemExit):
        app_instance.start()
    
    # Verify load_plugins was called
    app_instance.load_plugins.assert_called_once()

def test_app_start_command_execution(app_instance, monkeypatch):
    """Test command execution in App.start method"""
    # Mock load_plugins
    app_instance.load_plugins = MagicMock()
    
    # Mock command handler
    app_instance.command_handler.execute_command = MagicMock()
    
    # Mock input to simulate command then exit
    inputs = iter(["test_command", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    
    # Test start method
    with pytest.raises(SystemExit):
        app_instance.start()
    
    # Verify execute_command was called
    app_instance.command_handler.execute_command.assert_called_with("test_command")

def test_app_start_exception_handling(app_instance, monkeypatch, caplog):
    """Test exception handling in App.start method"""
    # Mock load_plugins
    app_instance.load_plugins = MagicMock()
    
    # Mock input to raise exception, then exit
    mock_input = MagicMock(side_effect=[Exception("Test exception"), "exit"])
    monkeypatch.setattr("builtins.input", mock_input)
    
    # Mock execute_command to not be called (since input raises exception)
    app_instance.command_handler.execute_command = MagicMock()
    
    # Run with error logging captured
    with caplog.at_level(logging.ERROR):
        with pytest.raises(SystemExit):
            app_instance.start()
    
    # Verify error was logged
    assert "An error occurred while executing command" in caplog.text
