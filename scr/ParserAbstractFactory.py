from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from scr.db import db
import abc


class Parser(object):
    __url = []
    __url_tmp = []

    __metaclass__ = abc.ABCMeta

    site_url = None

    _save_link = False

    def __init__(self, site_url: str):
        self.site_url = site_url.strip('/')

    def __open_href_and_set(self) -> None:
        if self.__url and self.__url_tmp:
            html = urlopen(self.__url_tmp.pop())
        else:
            html = urlopen(self.site_url)

        soup = BeautifulSoup(html, features='html.parser')
        all_tag_a = list(set(soup.findAll('a')))

        print('tmp_link = ' + str(self.__url_tmp.__len__()) + ' all_link: ' + str(self.__url.__len__()))

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
                    cursor.execute("INSERT INTO `links` (`name`) VALUES (%s)", [href])

        db().connect().commit()

        if all_tag_a:
            self.__open_href_and_set()

    @abc.abstractmethod
    def _action(self, cursor, soup: BeautifulSoup) -> None:
        """Action for parsing"""
        return

    def run(self) -> None:
        self.__open_href_and_set()
