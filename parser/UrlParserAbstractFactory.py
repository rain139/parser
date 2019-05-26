from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import abc
from parser.Services.Helpers import save_log
from parser.Services.TableParseSite import *


class Parser(object):
    __urls = []
    __urls_tmp = []

    __metaclass__ = abc.ABCMeta

    _site_url_home = None

    _special_link = None

    _table = None

    _id_log = None

    __count_request = 0

    def __init__(self, site_url: str, table: str, **kwargs):
        self._table = table
        self._create_table()
        self._site_url_home = site_url.strip('/')
        self.__set_other_arguments(kwargs)

    def __set_other_arguments(self, kwargs: dict):
        if kwargs.get('special_link', False):
            self._special_link = kwargs.get('special_link', '').strip('/')

        if kwargs.get('id_log', False):
            self._id_log = kwargs.get('id_log', 0)
        else:
            self._id_log = create_log(self._site_url_home, self._table, self._special_link)

    def _create_table(self):
        cursor = Db().connect().cursor()
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS  `{table}`"
                           "( `id` INT NOT NULL AUTO_INCREMENT ,"
                           " `email` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_bin NULL DEFAULT NULL,"
                           " PRIMARY KEY (`id`)) ENGINE = InnoDB;".format(table=self._table))
            Db().connect().commit()
        except Exception as e:
            self._handler_exception(e)
            exit('\n \033[91m Error create table `{table}` \033[0m \n'.format(table=self._table))

    def __open_url(self):
        url = None
        try:
            if self.__urls and self.__urls_tmp:
                url = self.__urls_tmp.pop()
                return urlopen(url)
            elif self._special_link:
                return urlopen(self._site_url_home + '/' + self._special_link)
            else:
                return urlopen(self._site_url_home)

        except Exception as e:
            if url:
                error_url = '\033[91m url error {url}!  \033[0m'.format(url=url)
            else:
                error_url = '\033[91m url error {url}!  \033[0m'.format(url=self._site_url_home)

            return self._handler_exception(e, error_url)

    def __get_all_tag_a(self, soup: BeautifulSoup) -> list:

        if self._special_link:
            return list(set(soup.findAll('a', href=re.compile("^(/{href}/)".format(href=self._special_link)))))
        else:
            return list(set(soup.findAll('a')))

    def __handler_html(self, html) -> bool:

        if type(html) is bool:
            return html

        if html:
            try:
                soup = BeautifulSoup(html, features='html.parser')
            except Exception as e:
                return self._handler_exception(e, '\033[91m html error parse  \033[0m')

            all_tag_a = self.__get_all_tag_a(soup)

            print('tmp_link = {tmp_link} all_link: {all_link}'.format(tmp_link=self.__urls_tmp.__len__(),
                                                                      all_link=self.__urls.__len__()))

            cursor = Db().connect().cursor()

            for tag in all_tag_a:

                href = str(tag.get('href'))

                if re.search('http|wwww', href) and href.find(self._site_url_home) == -1:
                    continue

                if href.find(self._site_url_home) == -1:
                    href = self._site_url_home + '/' + href.strip('/')

                if href not in self.__urls and href != '/' \
                        and not re.search('(jpg|png|pdf|gif|jpeg|svg|txt|#|None)', href, re.IGNORECASE):
                    self.__urls.append(href)
                    self.__urls_tmp.append(href)
                    # For Abstract Fabric
                    self._action(cursor, soup)

            self.__save_count_url_to_bd()

            Db().connect().commit()

        if self.__urls_tmp:
            return True
        return False

    # Зберігти кожні n лінків в бд
    def __save_count_url_to_bd(self):
        self.__count_request += 1
        if self.__count_request % 100 == 0:
            count_links = self.get_count_links()
            count_tmp_links = self.__urls_tmp.__len__()
            save_count_links(self._id_log, count_links, count_tmp_links)

    @abc.abstractmethod
    def _action(self, cursor, soup: BeautifulSoup) -> None:
        """Action for parsing"""
        return

    def run(self) -> None:
        while (True):
            if not self.__handler_html(self.__open_url()):
                break

        print('Success Parsing!! `{table}`'.format(table=self._table))
        set_result_parse(self._id_log, self.__urls.__len__())

    def get_count_links(self) -> int:
        return self.__urls.__len__()

    def _handler_exception(self, e: Exception, text: str = None) -> bool:
        if text:
            print(text)

        save_log(e, self._site_url_home + ' ' + text)

        if self.__urls_tmp:
            return True
        else:
            return False
