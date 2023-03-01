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


def convert_image_cv(image):
    cv_image = np.array(image) 
    cv_image = cv.cvtColor(cv_image, cv.COLOR_RGB2BGR)
    
    return cv_image


def get_data_image(img, config="", output_type=Output.STRING):
    data = pytesseract.image_to_data(img, lang='eng', config=config, output_type=output_type)
    
    return data


class PlayerData():
    def __init__(self):
        pass

    def __repr__(self):
        return "{}, X:{} Y:{}".format(self.kingdom_cord, self.x_cord, self.y_cord)

    def __eq__(self, other):
        other_key = "{}{}{}".format(other.kingdom_cord, other.x_cord, other.y_cord)
        current_key = "{}{}{}".format(self.kingdom_cord, self.x_cord, self.y_cord)
        return current_key == other_key
    
    def __str__(self):
        return "Kingdom: {}, cord_x: {}, cord_y: {}".format(self.kingdom_cord, \
                self.x_cord, self.y_cord)

    @property
    def pos_img(self):
        return self._pos_img

    @pos_img.setter
    def pos_img(self, value):
        self._pos_img = value

    @property
    def kingdom_cord(self):
        return self._kingdom_cord

    @kingdom_cord.setter
    def kingdom_cord(self, value):
        if isinstance(value, int):
            value = str(value)
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
            self.kingdom_cord = "C" + self.kingdom_cord
            k_map_flg = False

        return k_map_flg

    def get_position_coord_pos(self):
        avatar_pos = const.CoordData(self._left_coord_pos, self._top_coord_pos)
        
        return avatar_pos

    def is_valid(self):
        try:
            if self.kingdom_cord and self.x_cord and self.y_cord:
                return True
            else:
                return False
        # missing some property
        except:
            return False

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
        image = self.device.screencap()
        sleep(1)

        return image

    def get_text_image(self, image=None, opt=const.OptionImage.CHAT):
        if image is None:
            image = self.take_screenshot()

        img = Image.open(io.BytesIO(image))
        if opt == const.OptionImage.CHAT:
            tesseract_config = ""
            coord_crop = const.COORD_MESSAGE_LIST
        elif opt == const.OptionImage.LOCATION:
            tesseract_config = r'--psm 13 tessedit_char_whitelist=C0123456789'
            coord_crop = const.COORD_LOCATION_LIST
        # Not support other flag
        elif opt == const.OptionImage.PLAYSCREEN:
            tesseract_config = ""
            coord_crop = const.COORD_FULLSCREEN_LIST
        else:
            pass

        crop_image = img.crop(coord_crop)
        image_cv = convert_image_cv(crop_image)
        image_data = get_data_image(image_cv, tesseract_config, Output.DICT)
        return image_data

    def find_cv_title_icon(self):
        image = self.take_screenshot()

        #Confirm user popup is showed

        image_data = self.get_text_image(image=image, opt=const.OptionImage.PLAYSCREEN)
        if ("Power" in image_data["text"] or ("Kill" in image_data["text"] \
            and "Points" in image_data["text"]) or "Alliance" in image_data["text"]) \
            or len(image_data["text"]) > 45:
            nparr = np.frombuffer(image, np.uint8)
            img = cv.imdecode(nparr, cv.IMREAD_COLOR)
            icon = cv.imread(const.TITLE_ICON_PATH)

            result = cv.matchTemplate(img, icon, cv.TM_CCOEFF_NORMED)

            _, _, _, max_loc = cv.minMaxLoc(result)

            top_left = max_loc
            bottom_right = (top_left[0] + icon.shape[1], top_left[1] + icon.shape[0])

            middle_lo = const.CoordData((top_left[0] + bottom_right[0])/2, (top_left[1] + bottom_right[1])/2)

            return middle_lo
        else:
            # Cannot find user popup
            print("Not found popup")
            print(image_data["text"])
            print("===")
            return None

    def game_chat(self, message):
        self.device.input_tap(const.COORD_CHAT_BAR.x, const.COORD_CHAT_BAR.y)
        self.device.input_text(message)
        self.device.input_tap(1565, 870) #click to send button
        self.device.input_tap(60, 25)
        print("Bot said: "+message)
        sleep(1)

    def chat_scoll_down(self):
        self.device.input_swipe(const.COORD_CHAT_SWIPE_BEGIN.x, const.COORD_CHAT_SWIPE_BEGIN.y, \
                                const.COORD_CHAT_SWIPE_END.x, const.COORD_CHAT_SWIPE_END.y, 500)

    def clickToTarget(self, coord_data, sleep_time=1):
        sleep(0.3)
        self.device.input_tap(coord_data.x, coord_data.y)
        sleep(sleep_time)