from pythonping import ping
from multiprocessing import Process, Queue


def my_ping(ip, queue):
    # print('pinging '+ip+' start')
    if 'Reply' in str(ping(ip)):
        queue.put(ip+'可达')
    else:
        queue.put(ip+'不可达')
    # print(' -->over!')


if __name__ == '__main__':
    process_list = []
    result_list = []
    queue = Queue()
    for n in range(1, 200): # 200改成255，有些进程始终不退出，不知何原因。
        p = Process(target=my_ping, args=('192.168.68.'+str(n), queue))
        p.start()
        process_list.append(p)

    for p in process_list:
        p.join()

    print('all process over!!!!')
    results = [queue.get() for p in process_list]
    print(results)

    for r in results:
        if '不可达' not in r:
            print(r)



