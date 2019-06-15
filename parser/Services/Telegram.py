import requests


class Telegram:
    __API_KEY = '740828408:AAHHPyrSCmwy9jBO8uCr76ogd1lW2bWpIyw'

    __CHAT_ID = '406873185'

    __text = None

    __project_name = None

    def __init__(self, project_name: str):
        self.__project_name = project_name

    def error(self, text: str = None):
        self.__text = "Error parser " + self.__project_name + " \n\n" + text + "\n"
        self.send()

    def success(self):
        self.__text = "Success parser " + self.__project_name
        self.send()

    def send(self):
        url = 'https://api.telegram.org/bot' + self.__API_KEY + '/sendMessage?chat_id=' + self.__CHAT_ID + \
              '&text=' + self.__text
        requests.get(url)
