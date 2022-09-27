import yaml
import logging
import logging.config
import os
import time
import sys
import signal
from pathlib import Path
from dotenv import Dotenv
from is_iot_collector.collector import Collector


collector = Collector()


def set_env_variables():
    env_file_path = Path(os.getenv('PROJECT_PATH') + '/.env')
    dotenv = Dotenv(env_file_path)
    os.environ.update(dotenv)


def init_logger(file_path: str):
    with open(file_path, 'r') as f:
        config = yaml.safe_load(f.read())
    config['handlers']['file_handler']['filename'] = f"{os.getenv('PROJECT_PATH')}/{config['handlers']['file_handler']['filename']}"

    logging.config.dictConfig(config)


def signal_handler(sig, frame):
    logging.info("SIGINT received!")
    collector.stop()
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)
    set_env_variables()
    init_logger(os.getenv('PROJECT_PATH') + '/logger_config.yml')
    collector.start()
    while collector.status() == True:
        time.sleep(1)

if __name__ == "__main__":
    main()
