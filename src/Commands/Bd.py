import sys
from src.Parsers.EmailParser import EmailParser
from src.Models.parse_site import *


class ParseWithBd:

    def run(self):
        if len(sys.argv) > 1 and sys.argv[1].find('--bd') > -1:
            result = get_sites()
            if result:
                for arg in result:
                    config = {}
                    if arg['special_link']:
                        config['special_link'] = arg['special_link']
                    set_process(arg['id'])
                    EmailParser(arg['site'], arg['tb'], **config).run()
                    set_result_parse(arg['id'])
            else:
                exit('db rows 0')
            exit('That\'s all')
