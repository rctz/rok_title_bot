from enum import Enum
import os


class CoordData():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def offset(self, x_offset, y_offset):
        self.x += x_offset
        self.y += y_offset

TESSERACT_PATH = os.path.abspath("tesseract-OCR/tesseract.exe")
ADB_PATH = os.path.abspath("platform-tools_r33.0.3-windows/platform-tools/adb.exe")
TITLE_ICON_PATH = os.path.abspath("img/title_icon.jpg")

ADB_HOST = "127.0.0.1"
ADB_PORT = 5037
KINGDOM_NUMBER = 2254
KVK_NUMBER = 11658

COORD_MESSAGE_LIST = (415, 45, 800, 895)
COORD_LOCATION_LIST = (332, 12, 550, 42)
COORD_FULLSCREEN_LIST = (33, 121, 1443, 760)
COORD_CROP_FIND_TITLE = (35, 135, 1476, 782)
COORD_TARGET_TITLE = CoordData(945, 240)
COORD_TARGET_TITLE_DUKE = CoordData(650, 495)
COORD_TARGET_TITLE_CONFIRM = CoordData(800, 800)
COORD_CLOSE_CHAT = CoordData(1168, 450)
COORD_SEARCH = CoordData(418, 27)
COORD_KINGDOM_INPUT = CoordData(574, 180)
COORD_X_INPUT = CoordData(775, 184)
COORD_Y_INPUT = CoordData(977, 177)
COORD_SEARCH_SUBMIT_INPUT = CoordData(1108, 174)
COORD_LABEL_OK = CoordData(1520, 850)
COORD_CHAT_BAR = CoordData(670, 875)
COORD_CHAT_MESSAGE_BOX = CoordData(185, 845)
COORD_CHAT_SWIPE_BEGIN = CoordData(813, 650)
COORD_CHAT_SWIPE_END = CoordData(842, 394)
COORD_CONFIRM_NETWORK_LOST = CoordData(805, 598)
COORD_MID_SCREEN = CoordData(790, 460)
COORD_TOP_RIGHT_SCREEN = CoordData(922, 365)
COORD_TOP_LEFT_SCREEN = CoordData(658, 365)
COORD_BOTTOM_LEFT_SCREEN = CoordData(658, 555)
COORD_BOTTOM_RIGHT_SCREEN = CoordData(922, 555)

# Mid -> Top right -> Top left, Bottom left, Bottom right
USER_POPUP_CLICK_LIST = [COORD_MID_SCREEN, COORD_TOP_RIGHT_SCREEN, \
                         COORD_TOP_LEFT_SCREEN, COORD_BOTTOM_LEFT_SCREEN, \
                         COORD_BOTTOM_RIGHT_SCREEN]

# Title location
COORD_DUKE = CoordData(650, 495)

class TitleInfo(Enum):
    DUKE = COORD_DUKE
    ARCH = 2
    JUST = 3
    SCI = 4
    TRAI = 5
    BEGG = 6
    EXIL = 7
    SLAV = 8
    SLUG = 9 
    FOLL = 10

class OptionImage(Enum):
    LOCATION = 1
    CHAT = 2
    PLAYSCREEN = 3

class BotLocation(Enum):
    KINGDOM = 1
    KVK = 2

class SearchOption(Enum):
    MAGNIFY = 1
    SHARED_COORD = 2

