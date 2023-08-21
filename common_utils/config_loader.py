import configparser
import os


def get_config(section, option, to_int=False):
    config = configparser.ConfigParser()
    upper_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    conf_abs_path = os.path.join(upper_dir, 'conf','conf.ini')
    config.read(conf_abs_path, encoding='utf-8')
    if to_int:
        return int(config.get(section, option))
    else:
        return config.get(section, option)
