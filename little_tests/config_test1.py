import configparser
import os
from common_utils.config_loader import get_config

config = configparser.ConfigParser()
config.read('./test.conf', encoding='utf-8')

sections = config.sections()
print('所有节点名称：', sections)

options = config.options('section1')
print('section1节点的所有key：', options)

tuple_list = config.items('section2')
print('section2的键值对：', tuple_list)

value1 = config.get('section1','path')
print('section1下的path的值是：[{}]'.format(value1))

print('section1下是否有user_name这个key?', config.has_option('section1','user_name'))

config.set('section2','user_name','test888') # 设置key的value，没有key则创建，有key则覆盖
# config.write(open('./test.conf', 'w')) # 加上这句才实际写入

print(config.get('section2', 'user_name'))  # 不用config.write()实际写入，在内存中还是可以读取新值

print('__file__ is ', __file__)
print('os.path.abspath(__file__) is', os.path.abspath(__file__))
print('dir name is', os.path.dirname(os.path.abspath(__file__)))

server_path = get_config('desktop_broadcast','webrtc_streamer_location', trim_double_quote=True)
# server_path =  server_path[1:] if server_path.startswith('"') else server_path
# server_path =  server_path[:-1] if server_path.endswith('"') else server_path
print('[{}]'.format(server_path))
print('webrtc streamer服务文件是否存在？{}'.format(os.path.exists(os.path.join(server_path, 'webrtc-streamer.exe'))))
