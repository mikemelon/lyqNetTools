from pythonping import ping
from concurrent.futures import ThreadPoolExecutor


def my_ping(ip):
    # print('pinging '+ip+' start')
    if 'Reply' in str(ping(ip)):
        return ip, True
    else:
        return ip, False


if __name__ == '__main__':
    executor = ThreadPoolExecutor(max_workers=100)
    result_list = []
    for n in range(1, 255): # 200改成255，有些进程始终不退出，不知何原因。
        result = executor.submit(my_ping, '192.168.68.'+str(n))
        result_list.append(result)

    reachable_ip_list = []
    for r in result_list:
        if r.result()[1]:
            reachable_ip_list.append(r.result()[0])

    print(reachable_ip_list)



