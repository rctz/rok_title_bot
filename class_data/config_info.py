import const

class Config:
    ######## Title config ########
    title_period = const.TITLE_PERIOD
    q_mode = const.QUEUE_MODE

    ######## Kingdom config ########
    kingdom_number = const.KINGDOM_NUMBER
    kvk_number = const.KVK_NUMBER

    ######## ADB config ########
    adb_host = const.ADB_HOST
    adb_port = const.ADB_PORT

    ######## PATH config ########
    tesseract_path = const.TESSERACT_PATH
    adb_path = const.ADB_PATH
    title_icon_path = const.TITLE_ICON_PATH
    
    def __init__(self):
        pass
