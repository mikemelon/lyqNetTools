from socket import socket, AF_INET, SOCK_STREAM
from PIL import Image
import io

serverName = '192.168.48.130' # Win7 remote computer
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
sentence = input('Input lowercase sentence:')
clientSocket.send(sentence.encode())
receivedMessage = clientSocket.recv(5*1024*1024)


if sentence.upper() == 'CAPTURE_SCREEN':
    print('picture saved!')
    im_show = Image.open(io.BytesIO(receivedMessage))
    # im_show.save('mytest.png')  # 可以存，也可以直接打开
    im_show.show()
else:
    print('From Server:', receivedMessage.decode())

clientSocket.close()
