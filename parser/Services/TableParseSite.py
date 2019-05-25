from parser.Services.Db import Db


def get_sites(one_row: bool = False) -> dict:
    cursor = Db().connect().cursor(dictionary=True)
    cursor.execute('SELECT * FROM `parser_site` WHERE `parse` = 0 and `process` = 0 ')
    if one_row:
        result = cursor.fetchone()
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


def save_count_links(table: str, count_links: int,count_tmp_links: int) -> None:
    cursor = Db().connect().cursor()
    cursor.execute('UPDATE `parser_site` SET `links` = %s,`tmp_links` = %s WHERE `tb` = %s',
                   [count_links,count_tmp_links, table])
    Db().connect().commit()
    cursor.close()


def set_process(id: int) -> None:
    cursor = Db().connect().cursor()
    cursor.execute('UPDATE `parser_site` SET `process` = 1,`start` =  NOW() WHERE `id` = %s', [id])
    Db().connect().commit()


def create_log(link: str, table: str, special_links: str = None):
    cursor = Db().connect().cursor()
    cursor.execute(
        "INSERT INTO `parser_site` (`id`, `site`, `tb`, `special_link`, `parse`, `process`, `links`, `tmp_links`, `start`, `end`) VALUES (NULL, %s,%s, %s, '0', '1', '0', '0',  NOW(), NULL)",
        [link, table, special_links])
    Db().connect().commit()
    cursor.close()

