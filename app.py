from src.Parsers.EmailParser import EmailParser
import sys
from src.services.helpers import *

count = len(sys.argv)

if count > 1:
    domen = sys.argv[1]
    if domen.find('--bd') > -1:
        result = get_sites()
        if result:
            for arg in result:
                config = {}
                if arg['special_link']:
                    config['special_link'] = arg['special_link']
                EmailParser(arg['site'], arg['tb'], **config).run()
                set_success_parse(arg['id'])
        else:
            exit('db rows 0')
        exit()
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
