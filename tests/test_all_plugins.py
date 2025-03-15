import pytest
from unittest.mock import patch, MagicMock
import logging
import types

# Import all plugin commands
from app.plugins.add import AddCommand
from app.plugins.sub import SubCommand
from app.plugins.multiply import MultiplyCommand
from app.plugins.divide import DivideCommand
from app.plugins.exit import ExitCommand
from app.plugins.greet import GreetCommand
from app.plugins.menu import MenuCommand
from app.history import HistoryManager

# Test fixtures
@pytest.fixture
def mock_history_manager():
    """Mock history manager for testing"""
    with patch('app.history.HistoryManager') as mock:
        instance = mock.return_value
        instance.add_calculation.return_value = True
        instance.save_history.return_value = True
        yield instance

@pytest.fixture
def command_handler():
    """Create a command handler with mocked commands"""
    from app.commands import CommandHandler
    handler = CommandHandler()
    
    # Register all plugin commands
    handler.register_command("add", AddCommand())
    handler.register_command("sub", SubCommand())
    handler.register_command("multiply", MultiplyCommand())
    handler.register_command("divide", DivideCommand())
    handler.register_command("exit", ExitCommand())
    handler.register_command("greet", GreetCommand())
    handler.register_command("menu", MenuCommand(handler))
    
    return handler

# Comprehensive tests for each plugin
def test_add_command(monkeypatch, capsys, mock_history_manager):
    """Test the add command"""
    # Mock history manager
    monkeypatch.setattr('app.history.HistoryManager', MagicMock(return_value=mock_history_manager))
    
    # Mock input to provide test numbers
    inputs = ["10", "15"]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0) if inputs else "0")
    
    # Create and execute command
    cmd = AddCommand()
    cmd.execute()
    
    # Check output
    captured = capsys.readouterr()
    assert "25" in captured.out  # 10 + 15 = 25
    
    # Check history
    if hasattr(cmd, 'history_manager'):
        mock_history_manager.add_calculation.assert_called_once()
        mock_history_manager.save_history.assert_called_once()

def test_subtract_command(monkeypatch, capsys, mock_history_manager):
    """Test the subtract command"""
    # Mock history manager
    monkeypatch.setattr('app.history.HistoryManager', MagicMock(return_value=mock_history_manager))
    
    # Mock input to provide test numbers
    inputs = ["20", "8"]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0) if inputs else "0")
    
    # Create and execute command
    cmd = SubCommand()
    cmd.execute()
    
    # Check output
    captured = capsys.readouterr()
    assert "12" in captured.out  # 20 - 8 = 12
    
    # Check history
    if hasattr(cmd, 'history_manager'):
        mock_history_manager.add_calculation.assert_called_once()
        mock_history_manager.save_history.assert_called_once()

def test_multiply_command(monkeypatch, capsys, mock_history_manager):
    """Test the multiply command"""
    # Mock history manager
    monkeypatch.setattr('app.history.HistoryManager', MagicMock(return_value=mock_history_manager))
    
    # Mock input to provide test numbers
    inputs = ["7", "6"]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0) if inputs else "0")
    
    # Create and execute command
    cmd = MultiplyCommand()
    cmd.execute()
    
    # Check output
    captured = capsys.readouterr()
    assert "42" in captured.out  # 7 * 6 = 42
    
    # Check history
    if hasattr(cmd, 'history_manager'):
        mock_history_manager.add_calculation.assert_called_once()
        mock_history_manager.save_history.assert_called_once()

def test_divide_command(monkeypatch, capsys, mock_history_manager):
    """Test the divide command"""
    # Mock history manager
    monkeypatch.setattr('app.history.HistoryManager', MagicMock(return_value=mock_history_manager))
    
    # Mock input to provide test numbers
    inputs = ["20", "4"]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0) if inputs else "0")
    
    # Create and execute command
    cmd = DivideCommand()
    cmd.execute()
    
    # Check output
    captured = capsys.readouterr()
    assert "5" in captured.out  # 20 / 4 = 5
    
    # Check history
    if hasattr(cmd, 'history_manager'):
        mock_history_manager.add_calculation.assert_called_once()
        mock_history_manager.save_history.assert_called_once()

def test_divide_by_zero(monkeypatch, capsys, mock_history_manager):
    """Test divide by zero handling"""
    # Mock history manager
    monkeypatch.setattr('app.history.HistoryManager', MagicMock(return_value=mock_history_manager))
    
    # Mock input to provide test numbers
    inputs = ["10", "0"]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0) if inputs else "0")
    
    # Create and execute command
    cmd = DivideCommand()
    cmd.execute()
    
    # Check output
    captured = capsys.readouterr()
    assert "Cannot divide by zero" in captured.out or "zero" in captured.out.lower()

def test_exit_command(monkeypatch):
    """Test the exit command"""
    # Use pytest.raises instead of mocking sys.exit
    cmd = ExitCommand()
    with pytest.raises(SystemExit):
        cmd.execute()


def test_greet_command(capsys):
    """Test the greet command"""
    # Create and execute command
    cmd = GreetCommand()
    cmd.execute()
    
    # Check output
    captured = capsys.readouterr()
    assert "hello" in captured.out.lower() or "hi" in captured.out.lower() or "greet" in captured.out.lower()

def test_menu_command(command_handler, capsys):
    """Test the menu command"""
    # Create and execute command with command handler
    cmd = MenuCommand(command_handler)
    cmd.execute()
    
    # Check output for command names
    captured = capsys.readouterr()
    for command in ["add", "sub", "multiply", "divide", "exit", "greet"]:
        assert command in captured.out.lower()

def test_invalid_input_handling(monkeypatch, capsys):
    """Test handling of invalid input"""
    # Test with AddCommand but similar for other commands
    
    # Mock input to provide invalid then valid input
    inputs = ["not_a_number", "10", "20"]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0) if inputs else "0")
    
    # Create and execute command
    cmd = AddCommand()
    cmd.execute()
    
    # Check output
    captured = capsys.readouterr()
    assert "30" in captured.out  # 10 + 20 = 30 after ignoring invalid input

# Test for get_float helper function if present
def test_get_float_function(monkeypatch, capsys):
    """Test the get_float function used by commands"""
    try:
        # Try to import get_float from one of the command modules
        from app.plugins.add import get_float
        
        # Mock input to provide invalid then valid input
        inputs = ["bad", "42.5"]
        monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0) if inputs else "0")
        
        # Call the function
        result = get_float("Enter a number:")
        
        # Check result
        assert result == 42.5
    except ImportError:
        # If function doesn't exist, skip test
        pytest.skip("get_float function not found")

# Test for command registration in the application
def test_command_registration(command_handler):
    """Test that all commands are properly registered"""
    # Check all commands are registered
    assert "add" in command_handler.commands
    assert "sub" in command_handler.commands
    assert "multiply" in command_handler.commands
    assert "divide" in command_handler.commands
    assert "exit" in command_handler.commands
    assert "greet" in command_handler.commands
    assert "menu" in command_handler.commands
    
    # Check instances match expected types
    assert isinstance(command_handler.commands["add"], AddCommand)
    assert isinstance(command_handler.commands["sub"], SubCommand)
    assert isinstance(command_handler.commands["multiply"], MultiplyCommand)
    assert isinstance(command_handler.commands["divide"], DivideCommand)
    assert isinstance(command_handler.commands["exit"], ExitCommand)
    assert isinstance(command_handler.commands["greet"], GreetCommand)
    assert isinstance(command_handler.commands["menu"], MenuCommand)
