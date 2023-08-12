from OpenSSL.crypto import load_certificate, FILETYPE_PEM, FILETYPE_ASN1, X509Name, dump_certificate
import os
import textwrap
from datetime import datetime


def format_hex_result(hex_str, add_return=True, chars_per_line=45):
    hex_str = hex_str[2:]  # 去掉前面的'0x'
    if len(hex_str) % 2 == 1:
        hex_str = '0' + hex_str
    format_str = ':'.join(textwrap.wrap(hex_str, 2))
    if not add_return:
        return format_str
    else:
        return '\n'.join(textwrap.wrap(format_str, chars_per_line))


def format_asn1_date(d):
    return datetime.strptime(d.decode('ascii'), '%Y%m%d%H%M%SZ').strftime("%Y-%m-%d %H:%M:%S GMT")


def format_subject_issuer(x509name: X509Name):
    items = []
    for item in x509name.get_components():
        items.append('%s=%s' % (item[0].decode(), item[1].decode()))
    return "\t" + "\n\t".join(items)


def add_tabs_for_line(content: str, tabs_num=1):
    if '\n' in content:
        return '\n' + '\t' * tabs_num + content.replace('\n', '\n' + '\t' * tabs_num)
    else:
        return content


filepath = r'c:\rsatest1'
print('-' * 20 + '提取cer证书中的信息' + '-' * 20)
# 可以用openssl x509 -in lyqlyq.cer -pubkey -noout|openssl rsa -pubin -text -noout 命令验证是否一致 '
x509_obj = load_certificate(FILETYPE_PEM, open(os.path.join(filepath, 'baidu000.cer')).read().encode())  # 这是一个X509类型对象

print('版本:{}'.format(x509_obj.get_version() + 1))
print('序列号：{}'.format(format_hex_result(hex(x509_obj.get_serial_number()), add_return=False)))
print('签名算法:{}'.format(x509_obj.get_signature_algorithm().decode()))
issuer_obj = x509_obj.get_issuer()
print('Issuer：{}'.format(issuer_obj))
# print('\tC={}\n\tO={}\n\tOU={}\n\tCN={}'.format(issuer_obj.C, issuer_obj.O, issuer_obj.OU, issuer_obj.CN))
print('{}'.format(format_subject_issuer(issuer_obj)))
print('有效期：\n\t不早于：{}\n\t不晚于：{}\n\t已过期：{}'.format(format_asn1_date(x509_obj.get_notBefore()),
                                        format_asn1_date(x509_obj.get_notAfter()), x509_obj.has_expired()))

subject_obj = x509_obj.get_subject()
print('Subject：{}'.format(subject_obj))
# print('\tC={}\n\tST={}\n\tL={}\n\tOU={}\n\tO={}\n\tCN={}'.format(subject_obj.C, subject_obj.ST, subject_obj.L,
#                                                                  subject_obj.OU, subject_obj.O, subject_obj.CN))
print('{}'.format(format_subject_issuer(subject_obj)))

public_key_in_cert = x509_obj.get_pubkey()  # 这是一个PKey类型对象
print('公钥信息：{}位'.format(public_key_in_cert.bits()))
public_numbers_cert = public_key_in_cert.to_cryptography_key().public_numbers()
modulus_cert = public_numbers_cert.n
public_exponent_cert = public_numbers_cert.e
print('\t16进制格式化打印modulus:{}'.format(add_tabs_for_line(format_hex_result(hex(modulus_cert)), tabs_num=2)))
# print(format_hex_result(hex(modulus_cert)))
print('\tpublic exponent：{}, 十进制：{}'.format(hex(public_exponent_cert), public_exponent_cert))

extension_cnt = x509_obj.get_extension_count()
print('扩展程序{}个：'.format(extension_cnt))  # 扩展程序
for n in range(extension_cnt):
    extension = x509_obj.get_extension(n)
    print('\t{}：{}{}'.format(extension.get_short_name().decode(), '（关键）' if extension.get_critical() else '', add_tabs_for_line(str(extension), 2)))

print('hash:{}'.format(x509_obj.subject_name_hash()))  # TODO: 这时什么的hash ?
print('指纹：MD5：{}'.format(x509_obj.digest('MD5').decode()))  # 指纹：SHA1
print('指纹：SHA1：{}'.format(x509_obj.digest('SHA1').decode()))  # 指纹：SHA1
print('指纹：SHA256：{}'.format(x509_obj.digest('SHA256').decode()))  # 指纹：SHA256

import hashlib
cert_bytes_der = dump_certificate(FILETYPE_ASN1, x509_obj)
hash_obj = hashlib.sha1()
hash_obj.update(cert_bytes_der)
print(hash_obj.hexdigest())

import binascii
from Crypto.Util.asn1 import (DerSequence, DerObject)

def get_signature_bytes(x509):
    der = DerSequence()
    der.decode(dump_certificate(FILETYPE_ASN1, x509))
    der_tbs = der[0]
    der_algo = der[1]
    der_sig = der[2]
    der_sig_in = DerObject()
    der_sig_in.decode(der_sig)
    sig = der_sig_in.payload[1:]  # skip leading zeros
    print('sig type:{}'.format(type(sig)))
    return sig.hex() #sig.encode('hex')

sig_bytes = get_signature_bytes(x509_obj)
print(sig_bytes)
print('len:{}'.format(len(sig_bytes)))

# for s in bytes.fromhex(sig_bytes):
#     print('{}---{}'.format(s,type(s)))

print(binascii.b2a_hex(b'\x01\x34\x5e'))

