# Is601M3

Video Link: https://drive.google.com/file/d/17jb9TiM-PVHENFubtHU6uszY6IqEPfUJ/view?usp=sharing
 Improved calculator, which uses oop concepts.
Adding and implemnting command design pattern and plugins

Here's an improved version of your submission answers:

---

## Implementation of Design Patterns

In this calculator project, I've implemented several key design patterns to create a maintainable and extensible architecture:

**Singleton Pattern**: Implemented in the HistoryManager class to ensure a single global instance manages calculation history throughout the application. This centralizes history management and provides consistent access to history data from any command.
```python
# app/history/manager.py
def __new__(cls, *args, **kwargs):
    """Implement Singleton pattern"""
    if cls._instance is None:
        cls._instance = super(HistoryManager, cls).__new__(cls)
        cls._instance._initialized = False
    return cls._instance
```

**Facade Pattern**: The HistoryManager provides a simplified interface to complex pandas operations for data storage and retrieval, abstracting the details of DataFrame manipulation and CSV file handling.
```python
# app/history/manager.py
def add_calculation(self, operation, inputs, result):
    # Simplified interface to complex pandas operations
    new_row = {'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
               'operation': operation, 'inputs': str(inputs), 'result': result}
    self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
```

**Command Pattern**: Each operation is encapsulated as a separate Command class with a consistent interface, allowing for modular extension of calculator functionality. New commands can be added without modifying existing code.
```python
# app/plugins/add/__init__.py
class AddCommand(Command):
    def execute(self):
        # Command implementation
```

## Environment Variables

The application uses environment variables for flexible configuration without code changes. Key environment variables include:

- `LOG_LEVEL`: Controls logging verbosity (DEBUG, INFO, WARNING, ERROR)
- `LOG_FILE`: Specifies the log file location
- `HISTORY_FILE`: Defines where calculation history is stored
- `PLUGINS_DIR`: Sets the directory for dynamic plugin loading

Environment variables are loaded using python-dotenv and accessed through `os.environ.get()` with sensible defaults:

```python
# app/config.py
def load_config():
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    
    config = {
        'LOG_LEVEL': os.environ.get('LOG_LEVEL', 'INFO').upper(),
        'LOG_FILE': os.environ.get('LOG_FILE', 'logs/app.log'),
        'HISTORY_FILE': os.environ.get('HISTORY_FILE', 'data/calculation_history.csv'),
        'PLUGINS_DIR': os.environ.get('PLUGINS_DIR', 'app/plugins'),
    }
    return config
```

## Logging Implementation

The application uses Python's built-in logging module to record operations, errors, and debugging information throughout the codebase. This provides visibility into application behavior and aids troubleshooting.

Logging is configured based on environment variables and includes both file and console output:

```python
# app/config.py
def setup_logging(config):
    log_level_name = config['LOG_LEVEL']
    log_level = getattr(logging, log_level_name, logging.INFO)
    log_file = config['LOG_FILE']
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
```

Logging is used consistently throughout the application to track operations, record errors, and provide debugging information, with appropriate severity levels (INFO, WARNING, ERROR).

## Exception Handling: LBYL vs EAFP

The application demonstrates both error handling approaches:

**Look Before You Leap (LBYL)**: Checking conditions before attempting operations, used in the delete_entry method:

```python
# app/history/manager.py
def delete_entry(self, index):
    try:
        if 0 <= index < len(self.df):  # Check before performing operation
            self.df = self.df.drop(index).reset_index(drop=True)
            return True
        else:
            self.logger.warning(f"Invalid index: {index}")
            return False
    except Exception as e:
        self.logger.error(f"Error deleting history entry: {e}")
        return False
```

**Easier to Ask for Forgiveness than Permission (EAFP)**: Using try/except blocks to handle exceptions, demonstrated in the save_history method:

```python
# app/history/manager.py
def save_history(self):
    try:
        # Attempt operation without checking conditions first
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        self.df.to_csv(self.history_file, index=False)
        self.logger.info(f"Saved history to {self.history_file}")
        return True
    except Exception as e:
        # Handle exception if it occurs
        self.logger.error(f"Error saving history: {e}")
        return False
```

The application uses robust exception handling throughout to ensure reliability, with appropriate error logging and recovery mechanisms.




