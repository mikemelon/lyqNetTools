# RSA算法学习 by lyq
# 参考《计算机网络：自顶向下方法（原书第7版)》第8章中RSA算法相关的内容
import math


# def gcd(a, b): #求最大公约数
#     while b != 0:
#         a, b = b, a % b
#     return a


p, q = 5, 7
# p, q = 13, 29
n = p*q
z = (p-1)*(q-1)

print('p={}, q={}, n=pq={}, z=(p-1)(q-1)={}'.format(p, q, n, z))

print('选择小于n={}的一个数e，使得e和z(={})互质'.format(n, z))
e = n-1
for e_i in range(n-1, 2, -1):
    if math.gcd(e_i, z) == 1:
        e = e_i
        break
print('e={}'.format(e))

print('求一个数d，使得ed-1可以被z(={})整除'.format(z))
d = 1
d_i = 1
while True:
    if (e * d_i - 1) % z == 0 and e != d_i:
        d = d_i
        break
    d_i += 1
print('d={}'.format(d))

print('公钥是一对数(n,e)=({},{}),私钥是一对数(n,d)=({},{})'.format(n, e, n, d))
print('-'*40 + '以下开始加密和解密' + '-'*40)

m = input('输入一个要加密的明文整数m(m<{})：'.format(n))
m = int(m)
c = m**e % n
print('加密中间结果：m**e={}'.format(m**e))
print('加密后的密文c={}'.format(c))

m_decrypt = c**d % n
print('解密中间结果：c**d={}'.format(c**d))
print('解密后的明文m_decrypt={}'.format(m_decrypt))
