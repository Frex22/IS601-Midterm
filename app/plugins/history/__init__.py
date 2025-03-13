"""
History Plugin
Implements commands for managing calculation history.
"""

import logging
import shlex
from app.commands import Command
from app.history import HistoryManager

class HistoryCommand(Command):
    """Command to manage calculation history"""
    
    def __init__(self):
        """Initialize the history command"""
        self.logger = logging.getLogger(__name__)
        self.history_manager = HistoryManager()
    
    def execute(self):
        """
        Execute the history command
        
        This parses the command line input and routes to the appropriate history action
        """
        try:
            user_input = input("Enter history subcommand (show, clear, delete, save, search) or press Enter for recent history: ")
            
            # If no input, show recent history
            if not user_input.strip():
                self._show_recent_history()
                return
            
            # Parse the command arguments
            args = shlex.split(user_input)
            action = args[0].lower()
            
            if action == 'show':
                limit = int(args[1]) if len(args) > 1 else None
                self._show_history(limit)
            
            elif action == 'clear':
                self._clear_history()
            
            elif action == 'delete':
                if len(args) < 2:
                    print("Index required for delete operation. Usage: delete [index]")
                    return
                
                try:
                    index = int(args[1])
                    self._delete_entry(index)
                except ValueError:
                    print("Invalid index number. Usage: delete [index]")
            
            elif action == 'save':
                self._save_history()
            
            elif action == 'search':
                if len(args) < 2:
                    print("Search term required. Usage: search [term]")
                    return
                
                term = args[1]
                self._search_history(term)
            
            else:
                print(f"Unknown history action: {action}. Available actions: show, clear, delete, save, search")
                
        except Exception as e:
            self.logger.error(f"Error executing history command: {e}")
            print(f"An error occurred: {e}")
    
    def _show_recent_history(self, limit=10):
        """Show the most recent history entries"""
        self._show_history(limit)
    
    def _show_history(self, limit=None):
        """Show history entries with optional limit"""
        history_df = self.history_manager.get_history(limit)
        
        if history_df.empty:
            print("No calculation history found.")
            return
        
        # Format the dataframe for display
        print(f"Calculation History (showing {len(history_df)} records):")
        print("-------------------------------------------")
        
        for index, row in history_df.iterrows():
            print(f"{index}. [{row['timestamp']}] {row['operation']} {row['inputs']} = {row['result']}")
    
    def _clear_history(self):
        """Clear all history"""
        if self.history_manager.clear_history():
            self.history_manager.save_history()
            print("History cleared successfully.")
        else:
            print("Failed to clear history.")
    
    def _delete_entry(self, index):
        """Delete a specific history entry"""
        if self.history_manager.delete_entry(index):
            self.history_manager.save_history()
            print(f"Deleted entry at index {index}.")
        else:
            print(f"Failed to delete entry at index {index}. Index may be out of range.")
    
    def _save_history(self):
        """Save history to file"""
        if self.history_manager.save_history():
            print("History saved successfully.")
        else:
            print("Failed to save history.")
    
    def _search_history(self, term):
        """Search history for a term"""
        results_df = self.history_manager.search_history(term)
        
        if results_df.empty:
            print(f"No matches found for '{term}'.")
            return
        
        # Format the search results
        print(f"Search Results for '{term}' ({len(results_df)} matches):")
        print("-------------------------------------------")
        
        for index, row in results_df.iterrows():
            print(f"{index}. [{row['timestamp']}] {row['operation']} {row['inputs']} = {row['result']}")
