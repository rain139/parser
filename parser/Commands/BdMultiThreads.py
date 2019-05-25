import sys
from parser.Services.TableParseSite import *
from parser.Parsers.EmailParser import EmailParser
import subprocess
import shlex
import os


class ParseWithBdMultiThreads:

    def run(self) -> None:
        if len(sys.argv) > 1 and sys.argv[1].find('--bdm') > -1:

            result = get_sites()

            if result:
                for key, arg in enumerate(result):
                    set_process(arg['id'])
                    self.__run_parser_site(self.__create_command(arg))
            else:
                exit('db rows 0')

            exit('Run all')

    @staticmethod
    def __run_parser_site(command: str) -> None:
        cmd = shlex.split(command)
        subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @staticmethod
    def __create_command(arg: dict) -> str:
        path_venv_python = os.path.dirname(__file__) + '/../../venv/bin/activate'
        path_app = os.path.dirname(__file__) + '/../../app.py'
        command = '/usr/bin/source {venv_path} && /usr/bin/python3 {app_path} {link} {table} id_log={id_log}'.format(link=arg['site'],
                                                                                 venv_path=path_venv_python,
                                                                                 app_path=path_app,
                                                                                 table=arg['tb'],
                                                                                 id_log=arg['id'],
                                                                                 )
        if arg['special_link']:
            command += ' special_link=' + arg['special_link']
        print(command)
        return command
