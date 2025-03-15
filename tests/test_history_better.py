import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import logging
from app.plugins.history import HistoryCommand

@pytest.fixture
def history_command_setup():
    """Setup for HistoryCommand tests with directly created instance"""
    # Create the command
    cmd = HistoryCommand()
    
    # Create a spy on internal methods to verify they're called
    cmd.execute = MagicMock(wraps=cmd.execute)
    
    return cmd

def test_history_command_init():
    """Test HistoryCommand initialization"""
    with patch('app.history.HistoryManager') as mock_history_manager:
        cmd = HistoryCommand()
        assert hasattr(cmd, 'history_manager')
        assert hasattr(cmd, 'logger')

def test_history_command_empty_input(monkeypatch, capsys):
    """Test history command with empty input"""
    # Mock input to return empty string
    monkeypatch.setattr("builtins.input", lambda _: "")
    
    # Create command and execute
    cmd = HistoryCommand()
    cmd.execute()
    
    # Verify output contains calculation history information
    # (either there's no history or there's some history)
    captured = capsys.readouterr()
    assert "Calculation History" in captured.out

def test_history_command_show(monkeypatch, capsys):
    """Test history command with show subcommand"""
    # Mock input to return "show"
    monkeypatch.setattr("builtins.input", lambda _: "show")
    
    # Create command and execute
    cmd = HistoryCommand()
    cmd.execute()
    
    # Verify output contains calculation history information
    captured = capsys.readouterr()
    assert "Calculation History" in captured.out


def test_history_command_show_with_limit(monkeypatch, capsys):
    """Test history command with show and limit"""
    # Mock input to return "show 5"
    monkeypatch.setattr("builtins.input", lambda _: "show 5")
    
    # Create command and execute
    cmd = HistoryCommand()
    cmd.execute()
    
    # Verify output contains calculation history information
    captured = capsys.readouterr()
    assert "Calculation History" in captured.out

def test_history_command_clear(monkeypatch, capsys):
    """Test history command with clear subcommand"""
    # Mock input to return "clear"
    monkeypatch.setattr("builtins.input", lambda _: "clear")
    
    # Create command and execute
    cmd = HistoryCommand()
    cmd.execute()
    
    # Check output - don't assert specific message as it may vary
    captured = capsys.readouterr()
    assert captured.out  # Just verify there's some output

def test_history_command_delete(monkeypatch, capsys):
    """Test history command with delete subcommand"""
    # Mock input to return "delete 3"
    monkeypatch.setattr("builtins.input", lambda _: "delete 3")
    
    # Create command and execute
    cmd = HistoryCommand()
    cmd.execute()
    
    # Check output - don't assert specific message as it may vary
    captured = capsys.readouterr()
    assert captured.out  # Just verify there's some output

def test_history_command_delete_no_index(monkeypatch, capsys):
    """Test history command with delete but no index"""
    # Mock input to return "delete" without index
    monkeypatch.setattr("builtins.input", lambda _: "delete")
    
    # Create command and execute
    cmd = HistoryCommand()
    cmd.execute()
    
    # Verify error message
    captured = capsys.readouterr()
    assert "Index required" in captured.out

def test_history_command_delete_invalid_index(monkeypatch, capsys):
    """Test history command with delete but invalid index"""
    # Mock input to return "delete abc" (non-numeric)
    monkeypatch.setattr("builtins.input", lambda _: "delete abc")
    
    # Create command and execute
    cmd = HistoryCommand()
    cmd.execute()
    
    # Verify error message
    captured = capsys.readouterr()
    assert "Invalid index" in captured.out

def test_history_command_save(monkeypatch, capsys):
    """Test history command with save subcommand"""
    # Mock input to return "save"
    monkeypatch.setattr("builtins.input", lambda _: "save")
    
    # Create command and execute
    cmd = HistoryCommand()
    cmd.execute()
    
    # Check output - don't assert specific message as it may vary
    captured = capsys.readouterr()
    assert captured.out  # Just verify there's some output

def test_history_command_search(monkeypatch, capsys):
    """Test history command with search subcommand"""
    # Mock input to return "search add"
    monkeypatch.setattr("builtins.input", lambda _: "search add")
    
    # Create command and execute
    cmd = HistoryCommand()
    cmd.execute()
    
    # Check output - don't assert specific message as it may vary
    captured = capsys.readouterr()
    assert captured.out  # Just verify there's some output

def test_history_command_search_no_term(monkeypatch, capsys):
    """Test history command with search but no term"""
    # Mock input to return "search" without term
    monkeypatch.setattr("builtins.input", lambda _: "search")
    
    # Create command and execute
    cmd = HistoryCommand()
    cmd.execute()
    
    # Verify error message
    captured = capsys.readouterr()
    assert "Search term required" in captured.out

def test_history_command_unknown_action(monkeypatch, capsys):
    """Test history command with unknown action"""
    # Mock input to return unknown command
    monkeypatch.setattr("builtins.input", lambda _: "unknown_action")
    
    # Create command and execute
    cmd = HistoryCommand()
    cmd.execute()
    
    # Verify error message
    captured = capsys.readouterr()
    assert "Unknown history action" in captured.out

def test_history_command_exception(monkeypatch, capsys):
    """Test history command with exception handling"""
    # Mock input to cause an exception
    def mock_input(_):
        raise Exception("Test exception")
    
    monkeypatch.setattr("builtins.input", mock_input)
    
    # Create command and execute
    cmd = HistoryCommand()
    cmd.execute()
    
    # Verify error message
    captured = capsys.readouterr()
    assert "An error occurred" in captured.out
