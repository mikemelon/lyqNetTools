from pythonping import ping
from multiprocessing import Pool


def my_ping(ip):
    # print('pinging '+ip+' start')
    resp = ping(ip)
    # print('-->',resp)
    if 'Reply' in str(resp):
        return ip, True, resp.rtt_avg_ms
    else:
        return ip, False, 999.9


def read_dns():
    with open('dns.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    ip2comment, comment2ip = {}, {}
    for line in lines:
        tmp = line.split(',')
        ip2comment[tmp[0]] = tmp[1].strip()
        comment2ip[tmp[1].strip()] = tmp[0]
    return ip2comment, comment2ip


if __name__ == '__main__':
    pool = Pool(255)
    result_list = []
    ip2comment, comment2ip = read_dns()
    for ip in ip2comment.keys():
        result = pool.apply_async(func=my_ping, args=(ip,))
        result_list.append(result)

    pool.close()
    pool.join()

    print('all process over!!!!')
    # print(result_list)

    reachable_ip_list = []
    for r in result_list:
        if r.get()[1]:
            reachable_ip_list.append((r.get()[0], r.get()[2]))

    print(('{:30}{:20}{}\n'+'-'*70).format('名称','IPv4地址','往返时间'))
    # print(reachable_ip_list)
    for item in sorted(reachable_ip_list, key=lambda x:x[1]):
        print('{:30}{:20}{}'.format(ip2comment[item[0]], item[0], str(item[1])+' ms'))
