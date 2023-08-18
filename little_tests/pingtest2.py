from pythonping import ping

for i in range(250, 255):
    ip = '192.168.68.' + str(i)
    result = ping(ip)
    if 'Reply' in str(result):
        print(ip+'可达')
    else:
        print(ip+'不可达')
