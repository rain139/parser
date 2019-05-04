from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from src.services.db import db
import abc


class Parser(object):
    __url = []
    __url_tmp = []

    _save_link = False

    __metaclass__ = abc.ABCMeta

    site_url = None

    _special_link = ''

    _table = None

    def __init__(self, site_url: str, table: str, **kwargs):
        self._table = table
        self._create_table()
        self.site_url = site_url.strip('/')

        if kwargs.get('savve_link', False):
            self._save_link = kwargs.get('savve_link', False)
        if kwargs.get('special_link', False):
            self._special_link = kwargs.get('special_link', '').strip('/')

    def _create_table(self):
        cursor = db().connect().cursor()
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS  `{table}`"
                           "( `id` INT NOT NULL AUTO_INCREMENT ,"
                           " `email` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_bin NULL DEFAULT NULL,"
                           " PRIMARY KEY (`id`)) ENGINE = InnoDB;".format(table=self._table))
            db().connect().commit()
        except Exception:
            exit('\n \033[91m Error create table `{table}` \033[0m \n'.format(table=self._table))

    def __open_href_and_set(self) -> None:
        html = None
        try:
            if self.__url and self.__url_tmp:
                html = urlopen(self.__url_tmp.pop())
            else:
                html = urlopen(self.site_url)
        except:
            if self.__url_tmp:
                self.__open_href_and_set()
            else:
                print('\033[91m Base url error!  \033[0m')

        if html:
            soup = BeautifulSoup(html, features='html.parser')
            if self._special_link:
                all_tag_a = list(set(soup.findAll('a', href=re.compile("^(/{href}/)".format(href=self._special_link)))))
            else:
                all_tag_a = list(set(soup.findAll('a')))

            print('tmp_link = {tmp_link} all_link: {all_link}'.format(tmp_link=self.__url_tmp.__len__(),
                                                                      all_link=self.__url.__len__()))

            cursor = db().connect().cursor()

            for tag in all_tag_a:
                href = str(tag.get('href'))

                if re.search('http|wwww', href) and href.find(self.site_url) == -1:
                    continue

                if href.find(self.site_url) == -1:
                    href = self.site_url + '/' + href.strip('/')

                if href not in self.__url and href != '/' \
                        and not re.search('(jpg|png|pdf|gif|jpeg|svg|txt|#|None)', href, re.IGNORECASE):
                    self.__url.append(href)
                    self.__url_tmp.append(href)
                    self._action(cursor, soup)

                    if self._save_link:
                        try:
                            cursor.execute("INSERT INTO `links` (`name`) VALUES (%s)", [href])
                        except:
                            print('Error insert links')
            db().connect().commit()

        if self.__url_tmp:
            self.__open_href_and_set()

    @abc.abstractmethod
    def _action(self, cursor, soup: BeautifulSoup) -> None:
        """Action for parsing"""
        return

    def run(self) -> None:
        self.__open_href_and_set()
        print('Success Parsing!! `{table}`'.format(table=self._table))

