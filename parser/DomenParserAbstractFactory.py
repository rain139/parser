from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from parser.Services.Db import Db
import abc
from parser.Services.Helpers import save_log
from parser.Services.TableParseSite import *


class Parser(object):
    __url = []
    __url_tmp = []

    __metaclass__ = abc.ABCMeta

    _site_url = None

    _special_link = None

    _table = None

    __limit_save_count_link = 0

    _id_log = None

    # Перемінна де йде запис кожних n тис лінків для їх зберігання в бд
    __count_request = 0

    def __init__(self, site_url: str, table: str, **kwargs):
        self._table = table
        self._create_table()
        self._site_url = site_url.strip('/')

        if kwargs.get('special_link', False):
            self._special_link = kwargs.get('special_link', '').strip('/')

        if kwargs.get('id_log', False):
            self._id_log = kwargs.get('id_log', 0)
        else:
            self._id_log = create_log(self._site_url, table, self._special_link)

    def _create_table(self):
        cursor = Db().connect().cursor()
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS  `{table}`"
                           "( `id` INT NOT NULL AUTO_INCREMENT ,"
                           " `email` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_bin NULL DEFAULT NULL,"
                           " PRIMARY KEY (`id`)) ENGINE = InnoDB;".format(table=self._table))
            Db().connect().commit()
        except Exception as e:
            self._exception_handler(e)
            exit('\n \033[91m Error create table `{table}` \033[0m \n'.format(table=self._table))

    def __open_url(self):
        try:
            if self.__url and self.__url_tmp:
                url_open_now = self.__url_tmp.pop()
                return urlopen(url_open_now)
            elif self._special_link:
                return urlopen(self._site_url + '/' + self._special_link)
            else:
                return urlopen(self._site_url)

        except Exception as e:
            if 'url_open_now' in locals():
                error_url = '\033[91m url error {url}!  \033[0m'.format(url=url_open_now)
            else:
                error_url = '\033[91m url error {url}!  \033[0m'.format(url=self._site_url)

            return self._exception_handler(e, error_url)

    def __open_href_and_set(self) -> bool:

        html = self.__open_url()

        if type(html) is bool:
            return html

        if html:

            try:
                soup = BeautifulSoup(html, features='html.parser')
            except Exception as e:
                return self._exception_handler(e, '\033[91m html error parse  \033[0m')

            if self._special_link:
                all_tag_a = list(set(soup.findAll('a', href=re.compile("^(/{href}/)".format(href=self._special_link)))))
            else:
                all_tag_a = list(set(soup.findAll('a')))

            print('tmp_link = {tmp_link} all_link: {all_link}'.format(tmp_link=self.__url_tmp.__len__(),
                                                                      all_link=self.__url.__len__()))

            cursor = Db().connect().cursor()

            for tag in all_tag_a:

                href = str(tag.get('href'))

                if re.search('http|wwww', href) and href.find(self._site_url) == -1:
                    continue

                if href.find(self._site_url) == -1:
                    href = self._site_url + '/' + href.strip('/')

                if href not in self.__url and href != '/' \
                        and not re.search('(jpg|png|pdf|gif|jpeg|svg|txt|#|None)', href, re.IGNORECASE):
                    self.__url.append(href)
                    self.__url_tmp.append(href)

                    self._action(cursor, soup)

            self.__save_count_url_to_bd()

            Db().connect().commit()

        if self.__url_tmp:
            return True
        return False

    # Зберігти кожні n лінків в бд
    def __save_count_url_to_bd(self):
        self.__count_request += 1
        if self.__count_request % 100 == 0:
            count_links = self.get_count_links()
            count_tmp_links = self.__url_tmp.__len__()
            save_count_links(self._id_log, count_links, count_tmp_links)

    @abc.abstractmethod
    def _action(self, cursor, soup: BeautifulSoup) -> None:
        """Action for parsing"""
        return

    def run(self) -> None:
        while (True):
            if not self.__open_href_and_set():
                break

        print('Success Parsing!! `{table}`'.format(table=self._table))
        set_result_parse(self._id_log, self.__url.__len__())

    def get_count_links(self) -> int:
        return self.__url.__len__()

    def _exception_handler(self, e: Exception, text: str = None) -> bool:
        if text:
            print(text)

        save_log(e, self._site_url + ' ' + text)

        if self.__url_tmp:
            return True
        else:
            return False
