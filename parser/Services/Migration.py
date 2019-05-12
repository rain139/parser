from parser.Services.Db import Db


class Migration:
    __sql_migration = []

    def __init__(self):
        self.__set_sql_migration()

    def __set_sql_migration(self):
        self.__sql_migration = [
            "CREATE TABLE IF NOT EXISTS `parser_site` ( `id` INT NOT NULL AUTO_INCREMENT , `site` VARCHAR(255) NULL DEFAULT NULL , `tb` VARCHAR(255) NULL DEFAULT NULL , `special_link` VARCHAR(255) NULL DEFAULT NULL , `parse` INT(1) NOT NULL DEFAULT '0' , `process` INT(1) NOT NULL DEFAULT '0' , `links` INT(11) NOT NULL DEFAULT '0' , `start` TIMESTAMP NULL DEFAULT NULL , `end` TIMESTAMP NULL DEFAULT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;"
        ]

    def run(self):
        if self.__sql_migration:
            cursor = Db().connect().cursor()
            for migration in self.__sql_migration:
                cursor.execute(migration)
            Db().connect().commit()
            cursor.close()
