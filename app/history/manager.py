"""
History Manager Module
"""
import os
import logging
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union, Any

class HistoryManager:
    """
    History Manager class to handle calculation history using pandas.
    Implements the Facade pattern for pandas operations and Singleton pattern for one instance.
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        """implement Singleton pattern"""
        if cls.__instance is None:
            cls.__instance = super(HistoryManager, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance
    
    def __init__(self):
        """initilising history manager"""
        if not getattr(self, '__initialized', False):
            self.logger = logging.getLogger(__name__)
            self.logger.info('History Manager initialised')
            self.history_file = os.environ.get('HISTORY_FILE', 'data/calculation_history.csv')

            history_dir = Path(self.history_file).parent
            if not history_dir.exists():
                try:
                    history_dir.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    self.logger.warning(f"Failed to create history directory: {e}")

            self.columns = ['timestamp', 'operation', 'inputs' , 'result']


            try:
                self._load_history()
                self.logger.info('History manager initialised successfully with history file: {self.history_file}') 
            except Exception as e:
                self.logger.warning(f"could not load history file: {e}")
                self.df = pd.DataFrame(columns=self.columns)

            self.__initialized = True

    def _load_history(self) -> None:
        """load history from csv file"""
        try:
            if os.path.exists(self.history_file):
                self.df = pd.read_csv(self.history_file)
                self.logger.info(f"History loaded from {self.history_file}")
            else:
                self.df = pd.DataFrame(columns=self.columns)
                self.logger.info(f"History file not found, creating new file: '{self.history_file}'")
        except Exception as e:
            self.logger.error(f"Failed to load history file: {e}")
            raise e
        
    def add_calculation(self, operation: str, inputs: List[Any], result: Any) -> bool:
        """add calulation to history"""
        try:
            new_row = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'operation': operation,
                'inputs': str(inputs),
                'result': result
            }
            self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
            self.logger.info(f"Calculation added to history: {new_row}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add calculation to history: {e}")
            return False
    
    def save_history(self):
            """save history to csv file"""
            try:
                os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
                self.df.to_csv(self.history_file, index=False)
                self.logger.info(f"History saved to {self.history_file}")
                return True
            except Exception as e:
                    self.logger.error(f"Failed to save history file: {e}")
                    return False
            
    def get_history(self, limit: Optional[int] = None) -> pd.DataFrame:
        """get history"""
        try:
            if limit and limit > 0:
                return self.df.tail(limit)
            return self.df
        except Exception as e:
            self.logger.error(f"Failed to get history: {e}")
            return pd.DataFrame()
    
    def clear_history(self) -> bool:
        """clear history"""
        try:
            self.df = pd.DataFrame(columns=self.columns)
            self.logger.info("History Cleared")
        except Exception as e:
            self.logger.error(f"Failed to clear history: {e}")
            return False
        
    def delete_entry(self, index:int) -> bool:
        """delete entry from history"""
        try:
            if 0<= index < len(self.df):
                self.df = self.df.drop(index).reset_index(drop=True)
                self.logger.info(f"Entry deleted from history: {index}")    
                return True
            else:
                self.logger.warning(f"Index out of range: {index}")
                return False
        except Exception as e:
            self.logger.error(f"Failed to delete entry from history: {e}")
            return False
    
    def search_history(self, term: str) -> pd.DataFrame:
        """Search history"""
        try:
            str_df = self.df.astype(str)

            mask = str_df.apply(lambda row: row.str.contains(term, case=False).any(), axis=1)
            result = self.df[mask]

            self.logger.info(f"Search history for term: {term}")
            return result
        except Exception as e:  
            self.logger.error(f"Failed to search history: {e}")
            return pd.DataFrame()






