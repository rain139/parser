import sys
from parser.Parsers.EmailParser import EmailParser
from parser.Services.TableParseSite import *
from parser.Commands.CommandAbstract import Command


class ParseWithBd(Command):

    def run(self):
        if len(sys.argv) > 1 and sys.argv[1].find('--bd') > -1:
            result = get_sites()
            if result:
                for arg in result:
                    config = {'id_log': arg['id']}

                    if arg['special_link']:
                        config['special_link'] = arg['special_link']

                    set_process(arg['id'])

                    parser = EmailParser(arg['site'], arg['tb'], **config)
                    parser.run()

            else:
                exit('db rows 0')
            exit('That\'s all')
