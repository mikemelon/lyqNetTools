from pythonping import ping

resp = ping('192.168.68.102')
print(resp)
print(resp.rtt_avg_ms)