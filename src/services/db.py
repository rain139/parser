import mysql.connector


class db:
    __instance = None

    def __init__(self):
        if not self.__instance:
            db.__instance = db.__Mysql().connect()

    def connect(self) -> mysql:
        return db.__instance

    class __Mysql:
        def connect(self):
            return mysql.connector.connect(host='localhost', database='parser', user='kek', password='some_pass')
