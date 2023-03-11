import const
import requests


class Line():
    def __init__(self):
        self.token = const.LINE_TOKEN
        self.notify_api = const.LINE_NOTIFY_API

    def notify_message(self, message):
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Bearer {}".format(self.token)
        }
        params = {
            "message": message
        }

        r = requests.post(self.notify_api, headers=header, params=params)
        if r.status_code == 200:
            print("Notify success")
        else:
            print("Notify fail")