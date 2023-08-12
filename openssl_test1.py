from OpenSSL.crypto import load_privatekey, sign, verify, FILETYPE_PEM, X509
import base64
import os
import rsa
import hashlib

filepath = r'c:\rsatest1'
key = load_privatekey(FILETYPE_PEM, open(os.path.join(filepath, 'private_pkcs1.pem')).read())
# print(key.type())
print('私钥长度：{} bits'.format(key.bits()))

content = b'test_message'
print(content)
print('test_message'.encode('utf8'))
signed_bytes1 = sign(key, content, 'sha256') # 签名=对消息做hash摘要(sha256)，然后用RSA私钥加密
x509 = X509()
x509.set_pubkey(key) # key是PKey类型对象，有可能包含密钥对，也可能只包含公钥（这里是前者）
try:
    verify(x509, signed_bytes1, b'test_message', 'sha256')
    print('verify OK！')
except Exception as e:
    print(e)
    print('Verify failed！')
print('签名的长度：{}'.format(len(signed_bytes1)))
print('签名结果：{}'.format(signed_bytes1))
signed_bytes1_b64 = base64.b64encode(signed_bytes1)
print('签名结果的Base64表示：{}'.format(signed_bytes1_b64))
print(len(signed_bytes1_b64))


print('-'*20 + '下面用另一种方式进行数字签名' + '-'*20)
hash_obj = hashlib.sha256()
hash_obj.update(content)
print('原文的sha256摘要：{}'.format(hash_obj.digest()))
print('原文的sha256摘要的HEX表示：{}'.format(hash_obj.hexdigest()))
private_key = rsa.PrivateKey.load_pkcs1(open(os.path.join(filepath, 'private_pkcs1.pem')).read())
public_key = rsa.PublicKey.load_pkcs1(open(os.path.join(filepath, 'public_pkcs1.pem')).read())
print('私钥内容:{}'.format(private_key))
print('公钥内容:{}'.format(public_key))
# crypt_text = rsa.encrypt(hash_obj.digest(), private_key) # 不能直接调用encrypt，有可能有padding操作等
signed_bytes2 = rsa.sign_hash(hash_obj.digest(), private_key, 'SHA-256')
verify_result = rsa.verify(b'test_message', signed_bytes2, public_key)
print(verify_result)
print('签名结果：{}'.format(signed_bytes2))
signed_bytes2_b64 = base64.b64encode(signed_bytes2)
print('签名结果的Base64表示：{}'.format(signed_bytes2_b64))
print(len(signed_bytes2))
print(signed_bytes2==signed_bytes1)


