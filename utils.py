import const
from class_data.config_info import Config
from pytesseract import pytesseract, Output
import numpy as np
import cv2 as cv
from configparser import ConfigParser

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

def read_config_file():
    # instantiate
    config_inst = ConfigParser()

    # parse existing file
    config_inst.read(const.CONFIG_NAME)
    
    Config_cls = Config()

    # read values from a section
    Config_cls.adb_host = config_inst.get('ADB config', 'ADB_HOST')
    Config_cls.adb_port = config_inst.getint('ADB config', 'ADB_PORT')

    Config_cls.title_period = config_inst.getfloat('Title config', 'TITLE_period')
    q_mode_number = config_inst.getint('Title config', 'QUEUE_MODE')
    Config_cls.q_mode = const.Mode(q_mode_number)

    Config_cls.kingdom_number = config_inst.getint('Map config', 'KINGDOM_MAP')
    Config_cls.kvk_number = config_inst.getint('Map config', 'KVK_MAP')

    return Config_cls