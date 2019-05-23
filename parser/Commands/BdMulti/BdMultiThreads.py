import sys
from parser.Services.TableParseSite import *
from parser.Parsers.EmailParser import EmailParser
import threading


class ParseWithBdMultiThreads:

    def run(self):
        if len(sys.argv) > 1 and sys.argv[1].find('--bdm') > -1:
            result = get_sites()
            if result:

                for key, arg in enumerate(result):
                    print(arg['site'])
                    t = threading.Thread(target=self.__run_parser_site, args=(arg,))
                    t.start()

            else:
                exit('db rows 0')

            exit('Run all')

    @staticmethod
    def __run_parser_site(arg):
        config = {}

        print('Run')
        set_process(arg['id'])
        # if arg['special_link']:
        #     config['special_link'] = arg['special_link']
        #
        # parser = EmailParser(arg['site'], arg['tb'], **config)
        # parser.run()
        #
        # set_result_parse(arg['id'], parser.get_count_links())
