import configparser
import os


def get_config(section, option, to_int=False, to_bool=False, trim_double_quote=False):
    # to_int, to_bool转为相应类型（只能有一个是True），否则转为str
    # trim_double_quote: 对于str类型，若trim_double_quote为True，则，则去掉前后的双引号
    config = configparser.ConfigParser()
    upper_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    conf_abs_path = os.path.join(upper_dir, 'conf', 'conf.ini')
    try:
        config.read(conf_abs_path, encoding='utf-8') # UTF-8 without BOM
    except Exception as ex:
        print('Exception occured in get_config:{}, \nSo we try another format'.format(ex))
        config.read(conf_abs_path, encoding='utf-8-sig')  # UTF-8 with BOM, Win记事本有时会保存为此格式
    if to_int:
        return config.getint(section, option)
    elif to_bool:
        return config.getboolean(section, option)
    elif trim_double_quote:
        str_value = config.get(section, option)
        str_value = str_value[1:] if str_value.startswith('"') else str_value
        str_value = str_value[:-1] if str_value.endswith('"') else str_value
        return str_value
    else:
        return config.get(section, option)


if __name__ == '__main__':
    remote_capture_screen_saving = get_config('remote_control', 'remote_capture_screen_saving',
                                              to_bool=True)
    print('remote_capture_screen_saving={}, type={}'.format(remote_capture_screen_saving,
                                                            type(remote_capture_screen_saving)))
    server_port = get_config('remote_control', 'server_port', to_int=True)
    print('server_port={}, type={}'.format(server_port, type(server_port)))
