from src.Parsers.EmailParser import EmailParser
from src.services.db import db
import sys

sys.setrecursionlimit(100000)

count = len(sys.argv)

if count > 1:
    domen = sys.argv[1]
else:
    exit("Error not find arg DOMEN")

if count > 2:
    table = sys.argv[2]
else:
    exit("Error not find arg table")

config = {}

if count > 3:
    for key, item in enumerate(sys.argv):
        if key > 2:
            key_value = item.split('=')
            config[key_value.pop()] = key_value.pop()

EmailParser(domen, table, **config).run()
