from src.Parsers.EmailParser import EmailParser
from src.services.db import db
import sys


sys.setrecursionlimit(100000)


EmailParser('https://anje.com.ua','anje').run()
