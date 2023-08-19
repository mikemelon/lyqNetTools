with open('../dns.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

ip2comment, comment2ip = {}, {}
for line in lines:
    tmp = line.split(',')
    ip2comment[tmp[0]] = tmp[1].strip()
    comment2ip[tmp[1].strip()] = tmp[0]

print(ip2comment)
print(comment2ip)
print(ip2comment.keys())