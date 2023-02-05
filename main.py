import threading
import re
from class_data.data_info import Adb, PlayerData, TitleInfo
from time import sleep
import cv2 as cv
from queue import Queue
from pytesseract import pytesseract, Output
import const

pytesseract.tesseract_cmd = const.TESSERACT_PATH

class TitleGiver():
    def __init__(self):
        self.manage_queue_flg = True
        self.action_title_flg = False
        self.previous_player_list = []
        self.title_queue = Queue()


    def manage_queue(self):
        while self.action_title_flg:
            print("Waiting action title")
            sleep(4)

        self.manage_queue_flg = True
        self.actual_player = get_player_list()
        if self.actual_player == self.previous_player_list:
            pass
        else:
            dup_input = find_first_dup(self.previous_player_list, self.actual_player)
            if dup_input:
                for item in dup_input:
                    self.title_queue.put(item)

        self.previous_player_list = self.actual_player
        self.manage_queue_flg = False


    def action_title(self):
        print(self.title_queue.queue)
        if not self.title_queue.empty():
            while self.manage_queue_flg:
                print("Waiting manage queue")
                sleep(2)

            self.action_title_flg = True
            print("Title action process")

            # Get player from queue
            player_info = self.title_queue.get()
            print(player_info)
            # If player is in kingdom map, can use magnify dude no forge
            if player_info.is_kingdom_map():
                search_with_magnifying(player_info)
            else:
                search_with_shared_coord(player_info)

            sleep(3)
            give_title(TitleInfo.DUKE)
            adb_cls.clickToTarget(const.COORD_CHAT_MESSAGE_BOX, sleep_time=1.5)

            self.action_title_flg = False


def get_player_list():
    player_list = []
    image_data = adb_cls.get_text_image()
    #print(image_data["text"])
    for idx, value in enumerate(image_data["text"]):
        if "Shared" in value:
            image_data_left = image_data["left"][idx:]
            image_data_top = image_data["top"][idx:]
            image_data_text = image_data["text"][idx:]

            player_data = get_coord_info(image_data_left, image_data_top, image_data_text)
            if player_data.is_valid():
                if player_list:
                    if player_list[-1] != player_data:
                        player_list.append(player_data)
                else:
                    player_list.append(player_data)
            else:
                print("Not found user request duke!")

    return player_list




def clickToTarget(coord_data, sleep_time=1):
    sleep(0.1)
    adb_cls.input_tap(coord_data.x, coord_data.y)
    sleep(sleep_time)


def get_coord_info(data_left, data_top, data_text):
    player_info = PlayerData()
    try:
        data_text = list(filter(lambda data: data!="", data_text))
        for i in range(len(data_text)):
            if data_text[i] == "Shared":
                if data_text[i+1] == "a" or data_text[i+2] == "coordinate." or data_text[i+2] == "coordinate":
                    player_info.left_image = data_left[i]
                    player_info.top_image = data_top[i]
                    player_info.pos_img = i

                    res = [False, False]
                    for j in range(i+1, len(data_text)):
                        if data_text[j] != '':
                            if "(#" in data_text[j]:
                                str_num_kd = len(data_text[j])
                                # Get Kingdom format (#2254
                                if str_num_kd == 6:
                                    player_info.kingdom_cord = data_text[j][2:]
                                else:
                                    player_info.kingdom_cord = data_text[j][3:]

                            elif data_text[j][0] == "X":
                                player_info.x_cord = int(re.findall(r'\d+', data_text[j])[0])
                                res[0] = True

                            elif data_text[j][0] == "Y":
                                y_cord = re.findall(r'\d+', data_text[j])
                                if y_cord:
                                    y_cord = int(y_cord[0])
                                else:
                                    y_cord = int(re.findall(r'\d+', data_text[j+1])[0])

                                player_info.y_cord = y_cord
                                res[1] = True

                            if res[0] is True and res[1] is True:
                                break
                    break
            else:
                continue

    except Exception as e:
        print(str(e))

    return player_info


def search_with_magnifying(player_info):
    # Close chat
    adb_cls.clickToTarget(const.COORD_CLOSE_CHAT)
    print("Close chat")

    # Click mafi icon
    adb_cls.clickToTarget(const.COORD_SEARCH)

    # Click kingdom input textbox
    adb_cls.clickToTarget(const.COORD_KINGDOM_INPUT, sleep_time=0.5)

    # Backspace 10 time
    for _ in range(10):
        adb_cls.input_keyevent(67)
    sleep(0.2)
    adb_cls.input_text(player_info.kingdom_cord)
    sleep(0.5)

    # Click label ok
    adb_cls.clickToTarget(const.COORD_LABEL_OK, sleep_time=0.1)

    # Click x input textbox
    adb_cls.clickToTarget(const.COORD_X_INPUT, sleep_time=0.5)
    adb_cls.input_text(player_info.x_cord)

    # Click label ok
    adb_cls.clickToTarget(const.COORD_LABEL_OK, sleep_time=0.1)

    # Click y input textbox
    adb_cls.clickToTarget(const.COORD_Y_INPUT, sleep_time=0.5)
    adb_cls.input_text(player_info.y_cord)

    # Click label ok
    adb_cls.clickToTarget(const.COORD_LABEL_OK, sleep_time=0.1)

    # Searching animation wait 5s
    adb_cls.clickToTarget(const.COORD_SEARCH_SUBMIT_INPUT, sleep_time=5)


def search_with_shared_coord(player_info):
    adb_cls.clickToTarget(player_info.get_position_coord_pos(), sleep_time=5)


def give_title(target_title):
    # Click mid screen
    adb_cls.clickToTarget(const.CORRD_MID_SCREEN, sleep_time=1.5)
    adb_cls.clickToTarget(const.COORD_TARGET_TITLE)
    adb_cls.clickToTarget(target_title.value, sleep_time=0.5)

    # Click confirm title
    adb_cls.clickToTarget(const.COORD_TARGET_TITLE_CONFIRM)
    

def actionTitle(player_info):
    print("Title action process")
    
    # print(player_info.kingdom_cord)
    # print(player_info.x_cord)
    # print(player_info.y_cord)

    # If player is in kingdom map, can use magnify dude no forge
    if player_info.is_kingdom_map():
        search_with_magnifying(player_info)
    else:
        search_with_shared_coord(player_info)
        

    sleep(3)
    give_title(TitleInfo.DUKE)
    adb_cls.clickToTarget(const.COORD_CHAT_MESSAGE_BOX, sleep_time=1.5)

    # device.input_swipe(player_info.left_avatar_pos, player_info.top_avatar_pos, \
    #                    player_info.left_avatar_pos, player_info.top_avatar_pos, 3500) #Metion user
    sleep(1)
    #adb_cls.game_chat(" On you")

    #detectDone()
    #scrollTopToFindCoord(False)


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



def main():
    title_queue = []
    done_queue = []
    while True:
        queue_thread = threading.Thread(target=title_giver.manage_queue(), daemon=True)
        title_thread = threading.Thread(target=title_giver.action_title(), daemon=True)
        queue_thread.start()
        title_thread.start()
        queue_thread.join()
        title_thread.join()
        #print(title_giver.title_queue)
        print("===============")



if __name__ == "__main__":
    adb_cls = Adb()
    title_giver = TitleGiver()
    if adb_cls.device_status:
        print("Starting...")
        main()
    else:
        print("No Devices Attached")
