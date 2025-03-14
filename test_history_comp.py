"""
Comprehensive test script for history functionality
Run this directly to test all aspects of the history management system
"""

import os
import pandas as pd
import logging
from pathlib import Path
from app.history import HistoryManager
import traceback
import time

# Set up logging for this test
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('history_test.log')
    ]
)

logger = logging.getLogger("history_test")

def test_history_functionality():
    """Test all aspects of history functionality"""
    try:
        # Log current working directory
        cwd = os.getcwd()
        logger.info(f"Current working directory: {cwd}")
        
        # Reset the HistoryManager singleton for testing
        logger.info("Resetting HistoryManager singleton instance")
        HistoryManager._instance = None
        
        # Get the path to the history file
        history_file = os.environ.get('HISTORY_FILE', 'data/calculation_history.csv')
        logger.info(f"History file should be at: {os.path.abspath(history_file)}")
        
        # Check if data directory exists
        data_dir = os.path.dirname(history_file)
        logger.info(f"Data directory path: {os.path.abspath(data_dir)}")
        logger.info(f"Data directory exists: {os.path.exists(data_dir)}")
        
        # Create data directory if it doesn't exist
        if not os.path.exists(data_dir):
            logger.info(f"Creating data directory: {data_dir}")
            os.makedirs(data_dir, exist_ok=True)
            logger.info(f"After creation, data directory exists: {os.path.exists(data_dir)}")
        
        # Delete the history file if it exists (for clean testing)
        file_existed = False
        if os.path.exists(history_file):
            file_existed = True
            file_size = os.path.getsize(history_file)
            logger.info(f"Found existing history file, size: {file_size} bytes")
            try:
                os.remove(history_file)
                logger.info(f"Deleted existing history file for clean testing")
            except Exception as e:
                logger.error(f"Failed to delete history file: {e}")
                logger.error(traceback.format_exc())
        else:
            logger.info(f"No existing history file found at {history_file}")
        
        # Create a HistoryManager instance
        logger.info("Creating HistoryManager instance...")
        start_time = time.time()
        history_manager = HistoryManager()
        logger.info(f"HistoryManager created in {time.time() - start_time:.3f} seconds")
        logger.info(f"HistoryManager's history_file attribute: {history_manager.history_file}")
        logger.info(f"Full path: {os.path.abspath(history_manager.history_file)}")
        
        # Add some test calculations
        logger.info("\nAdding test calculations...")
        operations = [
            ('add', [5, 3], 8),
            ('subtract', [10, 4], 6),
            ('multiply', [3, 7], 21),
            ('divide', [20, 5], 4)
        ]
        
        for op, inputs, result in operations:
            start_time = time.time()
            success = history_manager.add_calculation(op, inputs, result)
            logger.info(f"Added {op} calculation: {inputs} = {result}, Success: {success} in {time.time() - start_time:.3f} seconds")
        
        # Check current state of the dataframe
        logger.info(f"Current DataFrame has {len(history_manager.df)} rows and {len(history_manager.df.columns)} columns")
        logger.info(f"DataFrame columns: {history_manager.df.columns.tolist()}")
        
        # Save history to file
        logger.info("\nSaving history to file...")
        start_time = time.time()
        save_success = history_manager.save_history()
        logger.info(f"Save history completed in {time.time() - start_time:.3f} seconds")
        logger.info(f"Save history success: {save_success}")
        
        # Check if file exists
        file_exists = os.path.exists(history_file)
        logger.info(f"History file exists after save: {file_exists}")
        
        if file_exists:
            file_size = os.path.getsize(history_file)
            file_permissions = oct(os.stat(history_file).st_mode)[-3:]
            logger.info(f"History file size: {file_size} bytes")
            logger.info(f"History file permissions: {file_permissions}")
            
            # Read file contents if it exists
            try:
                df = pd.read_csv(history_file)
                logger.info(f"\nHistory file contents ({len(df)} rows):")
                for index, row in df.iterrows():
                    logger.info(f"Row {index}: {dict(row)}")
            except Exception as e:
                logger.error(f"Error reading history file: {e}")
                logger.error(traceback.format_exc())
        
        # Test search functionality
        logger.info("\nTesting search functionality...")
        start_time = time.time()
        search_results = history_manager.search_history('add')
        logger.info(f"Search completed in {time.time() - start_time:.3f} seconds")
        logger.info(f"Search results for 'add' ({len(search_results)} rows):")
        if not search_results.empty:
            for index, row in search_results.iterrows():
                logger.info(f"Search result {index}: {dict(row)}")
        
        # Test delete functionality
        if len(history_manager.df) > 0:
            logger.info("\nTesting delete functionality...")
            index_to_delete = 0
            logger.info(f"Before delete: {len(history_manager.df)} entries")
            start_time = time.time()
            delete_success = history_manager.delete_entry(index_to_delete)
            logger.info(f"Delete completed in {time.time() - start_time:.3f} seconds")
            logger.info(f"Delete entry at index {index_to_delete} success: {delete_success}")
            logger.info(f"After delete: {len(history_manager.df)} entries")
            
            # Save after delete
            start_time = time.time()
            save_after_delete = history_manager.save_history()
            logger.info(f"Save after delete completed in {time.time() - start_time:.3f} seconds")
            logger.info(f"Save after delete success: {save_after_delete}")
            
            # Check file after delete
            if os.path.exists(history_file):
                file_size = os.path.getsize(history_file)
                logger.info(f"History file size after delete: {file_size} bytes")
                
                try:
                    df = pd.read_csv(history_file)
                    logger.info(f"History file contents after delete ({len(df)} rows):")
                    for index, row in df.iterrows():
                        logger.info(f"Row {index}: {dict(row)}")
                except Exception as e:
                    logger.error(f"Error reading history file after delete: {e}")
        
        # Test clear functionality
        logger.info("\nTesting clear functionality...")
        logger.info(f"Before clear: {len(history_manager.df)} entries")
        start_time = time.time()
        clear_success = history_manager.clear_history()
        logger.info(f"Clear completed in {time.time() - start_time:.3f} seconds")
        logger.info(f"Clear history success: {clear_success}")
        logger.info(f"After clear: {len(history_manager.df)} entries")
        
        # Save after clear
        start_time = time.time()
        save_after_clear = history_manager.save_history()
        logger.info(f"Save after clear completed in {time.time() - start_time:.3f} seconds")
        logger.info(f"Save after clear success: {save_after_clear}")
        
        # Check if file still exists after clear
        file_exists = os.path.exists(history_file)
        logger.info(f"History file still exists after clear: {file_exists}")
        
        if file_exists:
            file_size = os.path.getsize(history_file)
            logger.info(f"History file size after clear: {file_size} bytes")
            
            try:
                df = pd.read_csv(history_file)
                logger.info(f"History file contents after clear ({len(df)} rows):")
                for index, row in df.iterrows():
                    logger.info(f"Row {index}: {dict(row)}")
            except Exception as e:
                logger.error(f"Error reading history file after clear: {e}")
        
        logger.info("\nHistory functionality test completed successfully.")
        return True
        
    except Exception as e:
        logger.error(f"Test failed with exception: {e}")
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    logger.info("Starting comprehensive history functionality test...\n")
    success = test_history_functionality()
    logger.info(f"Test completed with {'SUCCESS' if success else 'FAILURE'}")
