import const
from class_data.config_info import Config
from pytesseract import pytesseract, Output
import numpy as np
import math
import cv2 as cv
from configparser import ConfigParser


class ConfigValidator(ConfigParser):
    def validateStr(self, option, value):
        if isinstance(value, str) and value.strip() != "":
            return True
        else:
            raise ValueError("{} require string format and cannot be empty!".format(option))

    def validateInt(self, option, value):
        if isinstance(value, int) and not math.isclose(value, 0):
            return True
        else:
            raise ValueError("{} require integer format and cannot be 0!".format(option))
        
    def validateFloat(self, option, value):
        if isinstance(value, float) and not math.isclose(value, 0):
            return True
        else:
            raise ValueError("{} require float format and cannot be 0!".format(option))
        
    def validateConfigSection(self, config, section):
        if not config.has_section(section):
            raise Exception("{} require section [{}]".format(section))
        
    def getConfigOption(self, config, section, option, v):
        if config.has_option(section, option):
            if v is str:
                value = config.get(section, option)
                self.validateStr(option, value)
            elif v is int:
                value = config.getint(section, option)
                self.validateInt(option, value)
            elif v is float:
                value = config.getfloat(section, option)
                self.validateFloat(option, value)
            else:
                # not support other flag
                value = ""

            return value
        else:
            raise Exception("Require option {} in config file".format(option))


def is_connection_lost(image_data):
    for idx, data in enumerate(image_data):
        # Network unstable cas
        if data == "Network" :
            if image_data[idx+1] == "unstable," or image_data[idx+1] == "unstable":
                return True
        # Login fail case
        elif data == "Login":
            if image_data[idx+1] == "failed," or image_data[idx+1] == "failed":
                return True
        else:
            pass

    return False


def find_first_dup(previous, actual):
    if previous:
        previous_last = previous[-1]
        try:
            last_idx = actual.index(previous_last)
            
            return actual[last_idx+1:]
        except ValueError:
            # not found index of previous last
            return actual
    else:
        return actual
    

def convert_image_cv(image):
    cv_image = np.array(image) 
    cv_image = cv.cvtColor(cv_image, cv.COLOR_RGB2BGR)
    
    return cv_image


def get_data_image(img, config="", output_type=Output.STRING):
    data = pytesseract.image_to_data(img, lang='eng', config=config, output_type=output_type)
    
    return data

def validate_config(config):
    pass

def read_config_file():
    Config_ins = ConfigParser()
    Config_ins.read(const.CONFIG_NAME)
    Validator = ConfigValidator()

    Validator.validateConfigSection(Config_ins, "ADB config")
    Validator.validateConfigSection(Config_ins, "Title config")
    Validator.validateConfigSection(Config_ins, "Map config")
    Config_cls = Config()

    # read values from a section
    Config_cls.adb_host = Validator.getConfigOption(Config_ins, 'ADB config', 'ADB_HOST', str)
    Config_cls.adb_port = Validator.getConfigOption(Config_ins, 'ADB config', 'ADB_PORT', int)

    Config_cls.title_period = Validator.getConfigOption(Config_ins, 'Title config', 'TITLE_PERIOD', float)
    q_mode_number = Validator.getConfigOption(Config_ins, 'Title config', 'QUEUE_MODE', int)
    Config_cls.q_mode = const.Mode(q_mode_number)

    Config_cls.kingdom_number = Validator.getConfigOption(Config_ins, 'Map config', 'KINGDOM_MAP', int)
    Config_cls.kvk_number = Validator.getConfigOption(Config_ins, 'Map config', 'KVK_MAP', int)

    return Config_cls