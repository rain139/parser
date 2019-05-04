from src.ParserAbstractFactory import Parser
from bs4 import BeautifulSoup
import re


class EmailParser(Parser):
    __email = []

    def _action(self, cursor, soup: BeautifulSoup):
        tmp_email = self.__search_email(soup.findAll())

        if tmp_email:
            self.__save_bd(tmp_email, cursor)

    def __search_email(self, html):
        tmp_email = []

        for tag in html:
            result = re.findall('([A-Za-z0-9\._-]+@[A-Za-z]+\.(com|ukr|edu|net|ua))+', tag.text)
            if result:
                for email in result:
                    if email[0] not in self.__email:
                        self.__email.append(email[0])
                        tmp_email.append(email[0])
            elif tag.has_attr('href'):
                href = str(tag.get('href'))
                if href.find('mailto:') > -1:
                    email_with_mailto = tag.get('href').strip('mailto:')
                    if email_with_mailto not in self.__email:
                        self.__email.append(email_with_mailto)
                        tmp_email.append(email_with_mailto)
        return tmp_email

    def __save_bd(self, emails, cursor):
        print("save {count} emails".format(count=emails.__len__()))
        sql = "INSERT INTO `{table}` (`email`) VALUES ".format(table=self._table)
        values = ''
        for _ in emails:
            values = '(%s),'

        sql += values.strip(',')
        cursor.execute(sql, emails)
