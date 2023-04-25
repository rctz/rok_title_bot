import const

class Config:
    ######## Title config ########
    title_period = const.TITLE_PERIOD
    q_mode = const.QUEUE_MODE

    ######## Kingdom config ########
    kingdom_number = ""
    kvk_number = ""

    ######## ADB config ########
    adb_host = ""
    adb_port = ""

    ######## PATH config ########
    tesseract_path = const.TESSERACT_PATH
    adb_path = const.ADB_PATH
    title_icon_path = const.TITLE_ICON_PATH
    
    def __init__(self):
        pass
