from parser.Services.Db import Db


class Migration:
    __sql_migration = []
    __last_key_migration = 0

    def __init__(self):
        self.__create_settings_table()
        self.__set_last_key_migration()
        self.__set_sql_migration()

    def __create_settings_table(self):
        cursor = Db().connect().cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS `settings` ( `id`  VARCHAR(255) NOT NULL , `data` TEXT NULL DEFAULT NULL , UNIQUE (`id`)) ENGINE = InnoDB;")
        Db().connect().commit()
        cursor.close()

    def __set_last_key_migration(self):
        cursor = Db().connect().cursor(dictionary=True)
        cursor.execute("SELECT `data` FROM `settings` WHERE `id` = 'migrations'");
        result = cursor.fetchRow()
        if result:
            self.__last_key_migration = result['data']
        else:
           pass
        cursor.close()
        exit()

    def __set_sql_migration(self):
        self.__sql_migration = [
            "",
            "CREATE TABLE IF NOT EXISTS `parser_site` ( `id` INT NOT NULL AUTO_INCREMENT , `site` VARCHAR(255) NULL DEFAULT NULL , `tb` VARCHAR(255) NULL DEFAULT NULL , `special_link` VARCHAR(255) NULL DEFAULT NULL , `parse` INT(1) NOT NULL DEFAULT '0' , `process` INT(1) NOT NULL DEFAULT '0' , `links` INT(11) NOT NULL DEFAULT '0' , `start` TIMESTAMP NULL DEFAULT NULL , `end` TIMESTAMP NULL DEFAULT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;",
            "ALTER TABLE `parser_site` ADD `tmp_links` INT(11) NOT NULL DEFAULT '0' AFTER `links`;",
        ]

    def run(self):
        if self.__sql_migration:
            cursor = Db().connect().cursor()
            for key, migration in enumerate(self.__sql_migration):
                cursor.execute(migration)
            Db().connect().commit()
            cursor.close()
