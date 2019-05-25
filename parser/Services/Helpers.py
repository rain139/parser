import os
import datetime
from environs import Env, EnvError


def save_log(e: Exception, site: str) -> None:
    log_file = os.path.abspath('log.txt')
    with open(log_file, "a") as file:
        file.write("{name_site}   {date} :   {str} \n\n".format(name_site=site, date=str(datetime.datetime.now()),
                                                                str=str(e)))
        file.close()


def env(key: str, default: str = None) -> str:
    env = Env()
    env.read_env()
    try:
        return env(key)
    except EnvError:
        if default:
            return default
        else:
            exit('Not find {key} in .env'.format(key=key))
