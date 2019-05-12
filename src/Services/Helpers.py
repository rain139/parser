from src.Services.Db import Db
import os
import datetime


def get_sites(one_row: bool = False) -> dict:
    cursor = Db().connect().cursor(dictionary=True)
    cursor.execute('SELECT * FROM `parser_site` WHERE `parse` = 0 and `process` = 0 ')
    if one_row:
        result = cursor.fetchRow()
    else:
        result = cursor.fetchall()
    cursor.close()
    return result


def set_result_parse(id: int, count_links: int) -> None:
    cursor = Db().connect().cursor()
    cursor.execute('UPDATE `parser_site` SET `parse` = 1,`process` = 0,`end` = NOW(),`links` = %s WHERE `id` = %s',
                   [count_links, id])
    Db().connect().commit()
    cursor.close()


def set_process(id: int) -> None:
    cursor = Db().connect().cursor()
    cursor.execute('UPDATE `parser_site` SET `process` = 1,`start` =  NOW() WHERE `id` = %s', [id])
    Db().connect().commit()
    cursor.close()


def save_log(e: Exception, site: str) -> None:
    log_file = os.path.abspath('src/log/log.txt')
    with open(log_file, "a") as file:
        file.write("{name_site}   {date} :   {str} \n\n".format(name_site=site, date=str(datetime.datetime.now()),
                                                                str=str(e)))
        file.close()
