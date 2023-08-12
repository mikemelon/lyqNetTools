from OpenSSL.crypto import load_certificate, FILETYPE_PEM, load_publickey, dump_publickey, X509
import os
import rsa
import re


def format_hex_result(hex_str):
    hex_str = hex_str[2:]  # 去掉前面的'0x'
    if len(hex_str)%2 == 1:
        hex_str = '0' + hex_str
    format_str_list = re.findall('.{2}',hex_str) # 按步长为2分割字符串
    format_str = ':'.join(format_str_list)
    remainder = len(format_str) % 45
    format_str_list = re.findall('.{45}', format_str) # 一行45个字符
    format_str_list.append(format_str[-remainder:])
    return '\n'.join(format_str_list)


filepath = r'c:\rsatest1'
public_key_obj = load_publickey(FILETYPE_PEM, open(os.path.join(filepath, 'public_pkcs1.pem')).read()) # 这是一个PKey类型对象
public_key_pem = dump_publickey(FILETYPE_PEM, public_key_obj)
print('public_key_pem:{}'.format(public_key_pem))

print('-'*20 + '第1种方式打印公钥数字modulus(n)和public_exponent(e)' + '-'*20)
public_numbers = public_key_obj.to_cryptography_key().public_numbers()
modulus1 = public_numbers.n
public_exponent1 = public_numbers.e
print('modulus={}'.format(modulus1))
print('publicExponent={}'.format(public_exponent1))

print('-'*20 + '第2种方式打印公钥数字modulus(n)和public_exponent(e)' + '-'*20)
public_key = rsa.PublicKey.load_pkcs1(open(os.path.join(filepath, 'public_pkcs1.pem')).read().encode())
modulus2 = public_key.n
public_exponent2 = public_key.e
print('modulus={}'.format(modulus2))
print('publicExponent={}'.format(public_exponent2))
print(modulus1 == modulus2)
print(len(str(modulus1)))

print('-'*20 + '提取cer证书中的公钥' + '-'*20)
print('可以用openssl x509 -in lyqlyq.cer -pubkey -noout|openssl rsa -pubin -text -noout 命令验证是否一致')
x509_obj = load_certificate(FILETYPE_PEM, open(os.path.join(filepath, 'lyqlyq.cer')).read().encode()) # 这是一个X509类型对象
public_key_in_cert = x509_obj.get_pubkey() # 这是一个PKey类型对象
public_numbers_cert = public_key_in_cert.to_cryptography_key().public_numbers()
modulus_cert = public_numbers_cert.n
public_exponent_cert = public_numbers_cert.e
print('modulus_cert={}'.format(modulus_cert))
print('public_exponent_cert={}'.format(public_exponent_cert))
print('16进制格式化打印公钥')
print(format_hex_result(hex(modulus_cert)))
print(hex(public_exponent_cert))

