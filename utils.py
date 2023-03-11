import const
import re
from class_data.data_info import PlayerData
from pytesseract import pytesseract, Output
import numpy as np
import cv2 as cv

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