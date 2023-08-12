from socket import socket, AF_INET, SOCK_DGRAM
from PIL import Image
import io

#serverName = '127.0.0.1'  # 将此处改为Server的计算机名，或IP地址
serverName = '192.168.48.130'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input('Input lowercase sentence:')
clientSocket.sendto(message.encode(), (serverName, serverPort))
receivedMessage, serverAddress = clientSocket.recvfrom(1024*1024) # 5M buffer大缓存以便传输截图，UDP不能传这么大，失败！

if message.upper()=='CAPTURE_SCREEN':
    print('picture saved!')
    im_show = Image.open(io.BytesIO(receivedMessage))
    im_show.show()
else:
    print(receivedMessage.decode())

clientSocket.close()
