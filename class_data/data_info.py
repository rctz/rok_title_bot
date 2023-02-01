from ppadb.client import Client
from time import sleep
import const
from enum import Enum
import io
import re
from PIL import Image
import numpy as np
import cv2 as cv
from pytesseract import pytesseract, Output

pytesseract.tesseract_cmd = const.TESSERACT_PATH

def convert_image_cv(image):
    cv_image = np.array(image) 
    cv_image = cv.cvtColor(cv_image, cv.COLOR_RGB2BGR)
    
    return cv_image


def get_data_image(img, output_type=Output.STRING):
    data = pytesseract.image_to_data(img, lang='eng', config='', output_type=output_type)
    
    return data



    
class TitleInfo(Enum):
    DUKE = const.COORD_DUKE
    ARCH = 2
    JUST = 3
    SCI = 4
    TRAI = 5
    BEGG = 6
    EXIL = 7
    SLAV = 8
    SLUG = 9 
    FOLL = 10

class PlayerData():
    def __init__(self):
        self.checked = False

    def __eq__(self, other):
        other_key = "{}{}{}".format(other.kingdom_cord, other.x_cord, other.y_cord)
        current_key = "{}{}{}".format(self.kingdom_cord, self.x_cord, self.y_cord)
        return current_key == other_key
        
    @property
    def pos_img(self):
        return self._pos_img

    @pos_img.setter
    def pos_img(self, value):
        # Check flag found share location
        self.checked = True
        self._pos_img = value

    @property
    def kingdom_cord(self):
        return self._kingdom_cord

    @kingdom_cord.setter
    def kingdom_cord(self, value):
        self._kingdom_cord = value

    @property
    def x_cord(self):
        return self._x_cord

    @x_cord.setter
    def x_cord(self, value):
        self._x_cord = value

    @property
    def y_cord(self):
        return self._y_cord

    @y_cord.setter
    def y_cord(self, value):
        self._y_cord = value

    @property
    def left_image(self):
        return self._left_image

    @left_image.setter
    def left_image(self, value):
        self._left_image = value
        self._left_avatar_pos = self._left_image + 370
        self._left_coord_pos = self._left_image + 425

    @property
    def top_image(self):
        return self._top_image

    @top_image.setter
    def top_image(self, value):
        self._top_image = value
        self._top_avatar_pos = self._top_image + 40
        self._top_coord_pos = self._top_image + 55

    @property
    def left_pos_pic(self):
        return self._left_pos_pic

    @property
    def top_pos_pic(self):
        return self._top_pos_pic

    @property
    def left_avatar_pos(self):
        return self._left_avatar_pos

    @property
    def top_avatar_pos(self):
        return self._top_avatar_pos

    def is_kingdom_map(self):
        k_map_flg = True
        kingdom_cord_len = len(self.kingdom_cord)
        if kingdom_cord_len > 4:
            k_map_flg = False

        return k_map_flg

    def get_position_coord_pos(self):
        avatar_pos = const.CoordData(self._left_coord_pos, self._top_coord_pos)
        
        return avatar_pos

class Adb():
    def __init__(self) -> None:
        self.host = const.ADB_HOST
        self.port = const.ADB_PORT

        #Todo need revised
        self.connect_device()

    def connect_device(self):
        adb = Client(host=self.host, port=self.port)
        devices = adb.devices()

        if len(devices) == 0:
            self.device_status = False
        else:
            self.device_status = True
            self.device = devices[0]

    def take_screenshot(self):
        self.screen_image = self.device.screencap()
        sleep(1)

    def get_text_image(self):
        self.take_screenshot()

        img = Image.open(io.BytesIO(self.screen_image))
        chat_image = img.crop(const.COORD_MESSAGE_LIST)
        image_cv = convert_image_cv(chat_image)
        image_data = get_data_image(image_cv, Output.DICT)

        return image_data

    def game_chat(self, message):
        self.device.input_tap(const.COORD_CHAT_BAR.x, const.COORD_CHAT_BAR.y)
        self.device.input_text(message)
        self.device.input_tap(1565, 870) #click to send button
        self.device.input_tap(60, 25)
        print("Bot said: "+message)
        sleep(1)