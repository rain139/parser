import mysql.connector


class Db:
    __instance = None

    def __init__(self):
        if not self.__instance:
            Db.__instance = Db.__Mysql().connect()

    def connect(self) -> mysql:
        return Db.__instance

    class __Mysql:
        def connect(self):
            return mysql.connector.connect(host='localhost', database='parser', user='kek', password='some_pass')
