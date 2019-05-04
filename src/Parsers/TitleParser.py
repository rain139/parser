from src.ParserAbstractFactory import Parser
from bs4 import BeautifulSoup


class TitleParser(Parser):
    def _action(self, cursor, soup: BeautifulSoup):
        all_tag_h1 = list(set(soup.findAll('h1')))
        for h1 in all_tag_h1:
            cursor.execute("INSERT INTO `links` (`name`) VALUES (%s) ", [h1.text])
