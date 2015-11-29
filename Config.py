import ConfigParser
import os
class Config:
    def __init__(self):
        pass

    def read_config(self):
        config = ConfigParser.ConfigParser()
        config_file = os.path.dirname(os.path.abspath(__file__))+"/config.ini"
        config.read(config_file)
        return config
