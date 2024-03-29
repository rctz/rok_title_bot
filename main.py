# -*- coding: utf-8 -*-

import threading
import re
from class_data.data_info import Adb, PlayerData
from time import sleep, time
import schedule
import utils
from queue import Queue
from pytesseract import pytesseract
import const
import subprocess

pytesseract.tesseract_cmd = const.TESSERACT_PATH

class TitleGiver():
    def __init__(self):
        self.manage_queue_flg = True
        self.action_title_flg = False
        self.wait_finish_flg = False
        self.previous_player_list = []
        self.title_queue = Queue()
        # Convert min -> sec
        self.title_period = config_cls.title_period * 60
        self.title_time_counter = 0
        self.count_empty_queue = 0


    def manage_queue(self):
        while self.action_title_flg:
            print("Waiting action title")
            sleep(4)

        if config_cls.q_mode == const.Mode.ONLY_ONE_Q:
            if self.title_queue.qsize() != 0 or self.wait_finish_flg:
                return 
            else:
                adb_cls.clickToTarget(const.COORD_CHAT_MESSAGE_BOX, sleep_time=1.5)

        self.manage_queue_flg = True

        self.actual_player, image_data = get_player_list()
        if self.actual_player == self.previous_player_list or not self.actual_player:
            if config_cls.q_mode == const.Mode.ONLY_ONE_Q:
                adb_cls.chat_scoll_down()
        else:
            self.count_empty_queue = 0
            dup_input = utils.find_first_dup(self.previous_player_list, self.actual_player)
            if dup_input:
                for item in dup_input:
                    self.title_queue.put(item)

        # if actual player is not empty list
        if self.actual_player:
            self.previous_player_list = self.actual_player

        if self.title_queue.qsize() == 0:
            self.count_empty_queue += 1

        if self.count_empty_queue >= 5:
            print("Checking connection lost..")
            if utils.is_connection_lost(image_data["text"]):
                print("Found connection lost popup!")
                adb_cls.clickToTarget(const.COORD_CONFIRM_NETWORK_LOST, sleep_time=5)
                adb_cls.clickToTarget(const.COORD_CHAT_MESSAGE_BOX, sleep_time=1.5)
            else:
                print("Connection is ok!")
                self.count_empty_queue = 0
                if config_cls.q_mode == const.Mode.KEEP_ALL_Q:
                    adb_cls.chat_scoll_down()

        self.manage_queue_flg = False


    def action_title(self):
        print("Queue: ", title_giver.title_queue.queue)
        while self.manage_queue_flg:
            print("Waiting manage queue")
            sleep(2)

        time_now = time()
        if time_now - self.title_time_counter >= self.title_period:
            self.wait_finish_flg = False
            search_option = const.SearchOption.SHARED_COORD
            
            # If have player
            if not self.title_queue.empty():
                self.title_time_counter = time_now
                self.action_title_flg = True
                print("Title giving process")

                # Get player from queue
                player_info = self.title_queue.get()

                if config_cls.q_mode == const.Mode.KEEP_ALL_Q:
                    # Close chat box 
                    adb_cls.clickToTarget(const.COORD_CLOSE_CHAT, sleep_time=1.5)
        
                    # If player is in kingdom map, can use magnify dude no forge
                    if player_info.is_kingdom_map():
                        search_with_magnifying(player_info)
                        search_option = const.SearchOption.MAGNIFY
                    else:
                        bot_screen_location = current_bot_location()

                        if bot_screen_location == const.BotLocation.KVK:
                            search_with_magnifying(player_info)
                            search_option = const.SearchOption.MAGNIFY
                        else:
                            # Need to open chat to click location link
                            adb_cls.clickToTarget(const.COORD_CHAT_MESSAGE_BOX, sleep_time=1.5)
                            search_with_shared_coord(player_info, sleep_time=7)
                            search_option = const.SearchOption.SHARED_COORD

                    sleep(2.5)
                    give_title(const.TitleInfo.DUKE, search_option)
                    adb_cls.clickToTarget(const.COORD_CHAT_MESSAGE_BOX, sleep_time=1.5)
                    # Scoll down to lasted message in chat room
                    adb_cls.chat_scoll_down()
                    sleep(1)
                else:
                    adb_cls.clickToTarget(const.COORD_CHAT_MESSAGE_BOX, sleep_time=1.5)
                    search_with_shared_coord(player_info, sleep_time=7)
                    search_option = const.SearchOption.SHARED_COORD
                    sleep(2.5)
                    give_title(const.TitleInfo.DUKE, search_option)
                    self.wait_finish_flg = True          

                self.action_title_flg = False
        else:
            print("Waiting queue finish")


def get_coord_info(data_left, data_top, data_text):
    player_info = PlayerData()
    try:
        data_text = list(filter(lambda data: data!="", data_text))
        for i in range(len(data_text)):
            if data_text[i] == "Shared":
                if data_text[i+1] == "a" or data_text[i+2] == "coordinate." or data_text[i+2] == "coordinate":
                    found_x_flg = False
                    found_y_flg = False
                    player_info.left_image = data_left[i]
                    player_info.top_image = data_top[i]
                    player_info.pos_img = i

                    for j in range(i+1, len(data_text)):
                        #TODO Investigate why this case error
                        if "xCHPA" in data_text[j]:
                            pass

                        elif "(#" in data_text[j]:
                            # 0 is problem of ocr
                            if "C" in data_text[j] or "0" in data_text[j]:
                                player_info.kingdom_cord = const.KVK_NUMBER
                            else:
                                player_info.kingdom_cord = const.KINGDOM_NUMBER

                        # Error from orc
                        elif data_text[j][0] == "X" or data_text[j][0] == "x":
                            x_cord_list = re.findall(r'\d+', data_text[j])
                            if x_cord_list:
                                player_info.x_cord = int(x_cord_list[0])
                            else:
                                x_cord_list = re.findall(r'\d+', data_text[j+1])
                            player_info.x_cord = int(x_cord_list[0])
                            found_x_flg = True

                        # Error from orc
                        elif data_text[j][0] == "Y" or data_text[j][0] == "y":
                            y_cord = re.findall(r'\d+', data_text[j])
                            if y_cord:
                                y_cord = int(y_cord[0])
                            else:
                                y_cord = int(re.findall(r'\d+', data_text[j+1])[0])

                            player_info.y_cord = y_cord
                            found_y_flg = True
                        
                        else:
                            pass

                        if found_x_flg and found_y_flg is True:
                            break
                    break
            else:
                continue

    except Exception as e:
       print(str(e))

    return player_info


def get_player_list():
    player_list = []
    count_shared = 0
    image_data = adb_cls.get_text_image(opt=const.OptionImage.CHAT)
    num_shared_player = image_data["text"].count("Shared")
    if num_shared_player:
        for idx, value in enumerate(image_data["text"]):
            if "Shared" in value:
                count_shared += 1
                image_data_left = image_data["left"][idx:]
                image_data_top = image_data["top"][idx:]
                image_data_text = image_data["text"][idx:]

                player_data = get_coord_info(image_data_left, image_data_top, image_data_text)
                if player_data.is_valid():
                    # If valid do nothing 
                    pass
                else:
                    if config_cls.q_mode == const.Mode.KEEP_ALL_Q:
                        print("User is not valid, Searching with shared coord")
                        search_with_shared_coord(player_data, 7)
                        error_flg, x_location, y_location, map_location = get_location_from_tab()
                        
                        # Open chat box to find another
                        if count_shared != num_shared_player:
                            adb_cls.clickToTarget(const.COORD_CHAT_MESSAGE_BOX, sleep_time=1)

                        if not error_flg:
                            player_data.x_cord = x_location
                            player_data.y_cord = y_location
                            player_data.kingdom_cord = map_location
                        else:
                            print("Cannot get location of this user, Skip!")
                            continue

                    else:
                        pass

                # all player list
                if player_list:
                    if player_list[-1] != player_data:
                        player_list.append(player_data)
                else:
                    player_list.append(player_data)

    return player_list, image_data


def get_location_from_tab():
    x_location = 0
    y_location = 0
    kingdom_location = config_cls.kingdom_number
    error_flg = True
    image_data = adb_cls.get_text_image(opt=const.OptionImage.LOCATION)
    for _, data in enumerate(image_data["text"]):
        if "X:" in data or "X" in data:
            lo_x_list = re.findall(r'\d+', data)
            if lo_x_list:
                x_location = int(lo_x_list[0])
            else:
                error_flg = True
                break
            
        elif "Y:" in data or "Y" in data:
            lo_y_list = re.findall(r'\d+', data)
            if lo_y_list:
                y_location = int(lo_y_list[0])
            else:
                error_flg = True
                break
        elif "#" in data:
            if "C" in data:
                kingdom_location = config_cls.kvk_number
            else:
                kingdom_location = config_cls.kingdom_number
        else:
            pass

    if x_location and y_location:
        error_flg = False

    return error_flg, x_location, y_location, kingdom_location


def search_with_magnifying(player_info):
    # Click mafi icon
    adb_cls.clickToTarget(const.COORD_SEARCH)

    # Click kingdom input textbox
    adb_cls.clickToTarget(const.COORD_KINGDOM_INPUT, sleep_time=0.5)

    # Backspace 10 time
    for _ in range(10):
        adb_cls.device.input_keyevent(67)
    sleep(0.2)
    adb_cls.device.input_text(player_info.kingdom_cord)
    sleep(0.5)

    # Click label ok
    adb_cls.clickToTarget(const.COORD_LABEL_OK, sleep_time=0.1)

    # Click x input textbox
    adb_cls.clickToTarget(const.COORD_X_INPUT, sleep_time=0.5)
    adb_cls.device.input_text(player_info.x_cord)

    # Click label ok
    adb_cls.clickToTarget(const.COORD_LABEL_OK, sleep_time=0.1)

    # Click y input textbox
    adb_cls.clickToTarget(const.COORD_Y_INPUT, sleep_time=0.5)
    adb_cls.device.input_text(player_info.y_cord)

    # Click label ok
    adb_cls.clickToTarget(const.COORD_LABEL_OK, sleep_time=0.1)

    # Searching animation wait 5s
    adb_cls.clickToTarget(const.COORD_SEARCH_SUBMIT_INPUT, sleep_time=5)


def search_with_shared_coord(player_info, sleep_time=5):
    adb_cls.clickToTarget(player_info.get_position_coord_pos(), sleep_time=sleep_time)


def give_title(target_title, search_opt):
    if search_opt == const.SearchOption.SHARED_COORD:
        # Click mid screen
        adb_cls.clickToTarget(const.COORD_MID_SCREEN, sleep_time=1.5)
        adb_cls.clickToTarget(const.COORD_TARGET_TITLE)

        adb_cls.clickToTarget(target_title.value, sleep_time=1.5)

        # Click confirm title
        adb_cls.clickToTarget(const.COORD_TARGET_TITLE_CONFIRM)


    else:
        print(const.USER_POPUP_CLICK_LIST)
        for click_coord in const.USER_POPUP_CLICK_LIST:
            print("Click cord:", click_coord)
            adb_cls.clickToTarget(click_coord, sleep_time=3)
            title_page = adb_cls.find_cv_title_icon()
            print("Title page: ", title_page)
            if title_page is not None:
                
                adb_cls.clickToTarget(title_page)
                
                adb_cls.clickToTarget(target_title.value, sleep_time=0.5)

                # Click confirm title
                adb_cls.clickToTarget(const.COORD_TARGET_TITLE_CONFIRM)
                break


def run_thread_queue():
    queue_thread = threading.Thread(target=title_giver.manage_queue(), daemon=True)
    queue_thread.start()
    queue_thread.join()


def run_thread_title():
    title_thread = threading.Thread(target=title_giver.action_title(), daemon=True)
    title_thread.start()
    title_thread.join()


def current_bot_location():
    bot_location = const.BotLocation.KINGDOM
    image_data = adb_cls.get_text_image(opt=const.OptionImage.LOCATION)
    
    for _, value in enumerate(image_data["text"]):
        #TODO Check again maybe can remove #C
        if "#C" in value or "C" in value:
            bot_location = const.BotLocation.KVK
            break
    
    print("Bot screen location: ", bot_location)

    return bot_location


def run_adb_console():
    adb_process = subprocess.Popen([const.ADB_PATH, "start-server"])
    adb_process.wait()
    print("Adb connected!")


def main():
    while True:
        run_thread_queue()
        schedule.run_pending()


if __name__ == "__main__":
    run_adb_console()
    config_cls = utils.read_config_file()
    schedule.every(3).seconds.do(run_thread_title)
    adb_cls = Adb(config_cls)
    title_giver = TitleGiver()
    
    if adb_cls.device_status:
        print("Starting...")
        main()
    else:
        print("No Devices Attached")
