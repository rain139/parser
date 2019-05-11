from src.services.db import db


def get_sites() -> dict:
    cursor = db().connect().cursor(dictionary=True)
    cursor.execute('SELECT * FROM `parser_site` WHERE `parse` = 0')
    result = cursor.fetchall()
    cursor.close()
    return result


def set_result_parse(id: int) -> None:
    cursor = db().connect().cursor(dictionary=True)
    cursor.execute('UPDATE `parser_site` SET `parse` = 1 WHERE `id` = %s', [id])
    db().connect().commit()
    cursor.close()

