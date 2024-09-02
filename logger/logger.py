import logging
import logging.config
import os

PATH = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = f'{PATH}/logging.conf'


class LoggerConfig:
    def __init__(self, config_file=CONFIG_PATH):
        self.config_file = config_file

    def get_logger(self, name):
        logging.config.fileConfig(self.config_file)
        return logging.getLogger(name)


logger = LoggerConfig().get_logger(__name__)
