from src.services.db import db


def get_sites(one_row: bool = False) -> dict:
    cursor = db().connect().cursor(dictionary=True)
    cursor.execute('SELECT * FROM `parser_site` WHERE `parse` = 0 and `process` = 0 ')
    if one_row:
        result = cursor.fetchRow()
    else:
        result = cursor.fetchall()
    cursor.close()
    return result


def set_result_parse(id: int) -> None:
    cursor = db().connect().cursor(dictionary=True)
    cursor.execute('UPDATE `parser_site` SET `parse` = 1,`process` = 0 WHERE `id` = %s', [id])
    db().connect().commit()
    cursor.close()


def set_process(id:int) -> None:
    cursor = db().connect().cursor(dictionary=True)
    cursor.execute('UPDATE `parser_site` SET `process` = 1 WHERE `id` = %s',[id])
    db().connect().commit()
    cursor.close()
