from parser.Services.Db import Db


class Migration:
    __sql_migration = []
    __last_key_migration = 0

    def __init__(self):
        self.__create_settings_table()
        self.__set_last_key_migration()
        self.__set_sql_migration()

    def __create_settings_table(self) -> None:
        cursor = Db().connect().cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS `settings` ( `id`  VARCHAR(255) NOT NULL , `data` TEXT NULL DEFAULT NULL , UNIQUE (`id`)) ENGINE = InnoDB;")
        Db().connect().commit()
        cursor.close()

    def __set_last_key_migration(self) -> None:
        cursor = Db().connect().cursor(dictionary=True)
        cursor.execute("SELECT `data` FROM `settings` WHERE `id` = 'migrations'")
        result = cursor.fetchall()
        if result:
            self.__last_key_migration = int(result[0]['data'])
        else:
            cursor.execute("INSERT INTO `settings` (`id`, `data`) VALUES ('migrations', '0')")
            Db().connect().commit()
        cursor.close()

    def __set_sql_migration(self):
        self.__sql_migration = [
            "CREATE TABLE IF NOT EXISTS `parser_site` ( `id` INT NOT NULL AUTO_INCREMENT , `site` VARCHAR(255) NULL DEFAULT NULL , `tb` VARCHAR(255) NULL DEFAULT NULL , `special_link` VARCHAR(255) NULL DEFAULT NULL , `parse` INT(1) NOT NULL DEFAULT '0' , `process` INT(1) NOT NULL DEFAULT '0' , `links` INT(11) NOT NULL DEFAULT '0' , `start` TIMESTAMP NULL DEFAULT NULL , `end` TIMESTAMP NULL DEFAULT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;",
            "ALTER TABLE `parser_site` ADD `tmp_links` INT(11) NOT NULL DEFAULT '0' AFTER `links`;",
        ]

    def __update_last_key_migration(self, key: int) -> None:
        cursor = Db().connect().cursor()
        cursor.execute("UPDATE `settings` SET `data` = %s WHERE `id` = 'migrations'", [key+1])
        Db().connect().commit()
        cursor.close()

    def run(self) -> None:
        if self.__sql_migration:
            if self.__sql_migration:
                cursor = Db().connect().cursor()
                last_key = 0
                for key, migration in enumerate(self.__sql_migration):
                    if key >= self.__last_key_migration:
                        cursor.execute(migration)
                        last_key = key

                Db().connect().commit()
                cursor.close()
                self.__update_last_key_migration(last_key)
