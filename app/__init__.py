#changing this approach to use the plugins architecture
#changing app/__init to accomodate plugins
#changing app/commands/__init to accomodate plugins
import pkgutil
import importlib
import inspect
import os
from app.commands import CommandHandler
from app.commands import Command
import logging
import logging.config
from app.history.manager import HistoryManager
from dotenv import load_dotenv
class App:
    #linting this block
    """
    This class is the main application class
    """
    def __init__(self):
        """
        This is the constructor for the App class
        """
        os.makedirs('logs', exist_ok=True)  # create a logs directory if it does not exist
        os.makedirs('data', exist_ok=True)  # create a data directory for history files
    
    # Load config and set up logging
        load_dotenv()  # load the .env file
        from app.config import load_config, setup_logging
        config = load_config()
        setup_logging(config)
    
        self.settings = {key: value for key, value in os.environ.items()}
        self.settings.setdefault('ENV', 'DEV')
    
        # Initialize HistoryManager
        self.history_manager = HistoryManager()
        
        HistoryManager().add_calculation('add', [1, 2], 3)
        HistoryManager().save_history()

        logging.info('History Manager initialized')
    
        # Initialize CommandHandler
        self.command_handler = CommandHandler()

        

    #dynamically load all plugins
    def load_plugins(self):
        """
        This method loads all plugins"""

        logging.info('Loading Plugins')
        plugins_package = 'app.plugins'
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        plugin_path = os.path.join(base_dir, 'app', 'plugins')

        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugin_path]):
            if is_pkg:
                try:
                    plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                    logging.debug(f'Loaded Plugin: {plugin_name}')
                except Exception as e:
                    logging.error(f'Failed to load plugin: {plugin_name}', exc_info=True)
                    continue

                for item_name in dir(plugin_module):
                    item = getattr(plugin_module, item_name)
                    try:
                        if issubclass(item, (Command)) and item is not Command:
                            logging.debug(f'Found command: {item.__name__} in plugin: {plugin_name}')
                            sig = inspect.signature(item.__init__)
                            if 'command_handler' in sig.parameters:
                                self.command_handler.register_command(plugin_name, item(self.command_handler))
                                logging.info(f'Registered command: {item.__name__} in plugin: {plugin_name} with command handler')
                            else:       
                                self.command_handler.register_command(plugin_name, item())
                                logging.info(f'Registered command: {item.__name__} in plugin: {plugin_name}')
                    except TypeError:
                        continue
                    except Exception as e:
                        logging.error(f'Failed to register command: {item_name} in plugin: {plugin_name}')
                        logging.error(e)
                logging.info('Completed loading plugins')

      
    def start(self):
        """
        This method starts the application
        """
        logging.info('Starting Application')
        self.load_plugins()
        print("Type 'Exit to quit the program")
        while True: #REPL Read-Eval-Print Loop
            try:
                command = ""

                command = input(">>>").strip()
                if command.lower() == 'exit':
                    logging.info("Exit command entered. Exiting the program")
                    print("Exiting the program....")
                    raise SystemExit("Exiting the program")
                
                logging.debug(f"Executing command: {command}")
                self.command_handler.execute_command(command)
            
            except Exception as e:
                logging.error(f"An error occurred while executing command '{command if command else '<unknown>'}': {e}", exc_info=True)

