from src.Parsers.EmailParser import EmailParser
import sys
from src.Commands.Bd import ParseWithBd


class Console:
    __domen = None
    __count_arg = 0
    __config = {}
    __classes_command = {}

    def __init__(self):
        self.__count_arg = len(sys.argv)
        self.__set_list_classes_command()

    def __set_domen(self):
        if self.__count_arg > 1:
            self.__domen = sys.argv[1]
        else:
            exit("Error not find arg DOMEN")

    def parse_command(self):
        self.__commands_before_general()
        self.__set_domen()
        self.__set_table()
        self.__set_config()
        EmailParser(self.__domen, self.__table, **self.__config).run()

    def __set_table(self):
        if self.__count_arg > 2:
            self.__table = sys.argv[2]
        else:
            exit("Error not find arg table")

    def __set_config(self):
        if self.__count_arg > 3:
            for key, item in enumerate(sys.argv):
                if key > 2:
                    key_value = item.split('=')
                    self.__config[key_value.pop()] = key_value.pop()

    def __commands_before_general(self):
        for _class in self.__classes_command['before']:
            _class().run()

    def __set_list_classes_command(self) -> None:
        self.__classes_command = {
            'before': [
                ParseWithBd,
            ],
            'general': [

            ]
        }


Console().parse_command()
