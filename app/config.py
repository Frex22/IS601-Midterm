import os
import logging
from pathlib import Path
from dotenv import load_dotenv

def load_config():
    """Load configuration from .env file"""
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    config = {
        'LOG_LEVEL': os.environ.get('LOG_LEVEL', 'INFO').upper(),
        'LOG_FILE': os.environ.get('LOG_FILE', 'logs/app.log'),
        'HISTORY_FILE': os.environ.get('HISTORY_FILE', 'data/calculation_history.csv'),
        'PLUGINS_DIR': os.environ.get('PLUGINS_DIR', 'app/plugins'),
    }

    ensure_directory_exists(Path(config['LOG_FILE']).parent)
    ensure_directory_exists(Path(config['HISTORY_FILE']).parent)

    return config

def ensure_directory_exists(directory):
    if not directory.exists():
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Failed to create directory: {e}")
            logging.warning(f"Failed to create directory: {e}")
            raise e

def setup_logging(config):
    """Setup logging configuration"""
    log_level_name = config['LOG_LEVEL']
    log_level = getattr(logging, log_level_name, logging.INFO)

    log_file = config['LOG_FILE']

    logging.basicConfig(
        level = log_level,
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers = [ logging.FileHandler(log_file),
                    logging.StreamHandler()
                    
                    ]
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured with level: {log_level_name}, file: {log_file}")

    