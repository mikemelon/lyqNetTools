from common_utils.config_loader import get_config

server_port = get_config('remote_control','server_port')
print('server_port={}, type={}'.format(server_port, type(server_port)))

server_port2 = get_config('remote_control','server_port', to_int=True)
print('server_port2={}, type={}'.format(server_port2, type(server_port2)))