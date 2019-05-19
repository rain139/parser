import sys
from parser.Parsers.EmailParser import EmailParser
from parser.Services.TableParseSite import *


class ParseWithBdMulti:

    def run(self):
        if len(sys.argv) > 1 and sys.argv[1].find('--bdm') > -1:
            result = get_sites()
            if result:
                for arg in result:
                    config = {}

                    if arg['special_link']:
                        config['special_link'] = arg['special_link']

                    set_process(arg['id'])

                    parser = EmailParser(arg['site'], arg['tb'], **config)

            else:
                exit('db rows 0')
            exit('That\'s all')