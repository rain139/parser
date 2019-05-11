import sys
from src.services.db import db
from src.Parsers.EmailParser import EmailParser


class ParseWithBd:

    def run(self):
        if len(sys.argv) > 1 and sys.argv[1].find('--bd') > -1:
            result = self.__get_sites()
            if result:
                for arg in result:
                    config = {}
                    if arg['special_link']:
                        config['special_link'] = arg['special_link']
                    try:
                        EmailParser(arg['site'], arg['tb'], **config).run()
                    except:
                        print('Fail parse')
                        continue
                    self.__set_success_parse(arg['id'])
            else:
                exit('db rows 0')
            exit()

    @staticmethod
    def __get_sites() -> dict:
        cursor = db().connect().cursor(dictionary=True)
        cursor.execute('SELECT * FROM `parser_site` WHERE `parse` = 0')
        result = cursor.fetchall()
        cursor.close()
        return result

    @staticmethod
    def __set_success_parse(id: int) -> None:
        cursor = db().connect().cursor(dictionary=True)
        cursor.execute('UPDATE `parser_site` SET `parse` = 1 WHERE `id` = %s', [id])
        db().connect().commit()
        cursor.close()
