from PIL import ImageGrab
import socket
import threading
import time
import struct
import sys
import cv2
import json
import hashlib
import numpy as np
import win32api
import win32con

host = '0.0.0.0'
port = 8001

# lyqnote: 这时一个实现比较"奇怪"的远程桌面。
# 远程桌面由server.py和client.py两个程序组成。
# 有时，还需要一个额外的config.ini文件，注意该config.ini文件只被client.py读取，里面记录了server的IP及端口号。
# 其实现原理：server启动后，client不断在本机截屏（包含鼠标位置动作等，目前并未实现键盘位置和动作）发送给server，server收到后弹窗动态显示。

# 因此要使用它，先在主控端启动server.py，
# 然后将client.py复制到被控端（即需要显示桌面的电脑，在config.ini里写好或直接写在程序中server端IP地址及端口号）并启动。

# server端关闭，会让client直接报错退出。
# client退出或关闭(包括关闭监控窗口)，并不会影响server.


def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # print(host, port)
        s.bind((host, port))
        s.listen(10)  # backlog=10, 它指定系统允许暂未 accept 的连接数，超过后将拒绝新连接。未指定则自动设为合理的默认值。
    except socket.error as e:
        print(e)
        sys.exit(1)
    print('Remote desktop server started, waiting connection...')

    while True:
        conn, addr = s.accept() # accept()方法返回两个参数，第1个是socket类型，第2个是address类型（含远端客户地址，端口号）
        print('conn={}, addr={}'.format(conn, addr))
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()


def deal_data(conn, addr):
    print('Accept new connection from {0}'.format(addr))
    conn.send('Hi, Welcome to the server!'.encode())

    while True:
        try:
            resize_ratio = json.loads(get_msg(conn, 1024).decode())
            if resize_ratio.get('resize_ratio'):
                conn.send("client info confirm".encode())
                break
        except Exception as e:
            print(e)

    param = {
        'resize_ratio': resize_ratio.get('resize_ratio'),
        'conn': conn,
        'pos': (0, 0)
    }
    window_name = addr[0]
    # print(conn.getpeername())
    # window_name = conn.getpeername()
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, OnMouseMove, param=param)

    while True:
        encode_header_len = get_msg(conn, 4)
        if not encode_header_len:
            break
        msg_header_length = struct.unpack('i', encode_header_len)[0]
        encode_header = get_msg(conn, msg_header_length)
        if not encode_header:
            break
        msg_header = json.loads(encode_header.decode())
        img_data = recv_msg(conn, msg_header)
        if not img_data:
            break
        if hashlib.md5(img_data).hexdigest() != msg_header['msg_md5']:
            break
        msg_decode = np.frombuffer(img_data, np.uint8)
        img_decode = cv2.imdecode(msg_decode, cv2.IMREAD_COLOR)

        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) <= 0:
            break
        cv2.imshow(window_name, img_decode)
        key = cv2.waitKey(20)  # cv2.imshow()方法后必须跟着cv2.waitKey()方法，以展示图像20ms
        print(key) if key != -1 else None

    cv2.destroyAllWindows()
    conn.close()


def get_msg(conn, length):
    try:
        return conn.recv(length)
    except socket.error as e:
        print(e)


def recv_msg(conn, msg_header):
    recv_size = 0
    img_data = b''
    while recv_size < msg_header['msg_length']:
        if msg_header['msg_length'] - recv_size > 10240:
            recv_data = get_msg(conn, 10240)
        else:
            recv_data = get_msg(conn, msg_header['msg_length']-recv_size)
        recv_size += len(recv_data)
        img_data += recv_data
    return img_data


def OnMouseMove(event, x, y, flags, param):
    win32api.SetCursor(win32api.LoadCursor(0, win32con.IDC_ARROW ))

    conn = param['conn']
    screen_x = round(x * param['resize_ratio'][0])
    screen_y = round(y * param['resize_ratio'][1])

    if (screen_x, screen_y) == param['pos'] and event == 0 and flags == 0:
        pass
    else:
        param['pos'] = (screen_x, screen_y)
        msg = {'mouse_position': (screen_x, screen_y), 'event': event, 'flags': flags}
        try:
            conn.send(struct.pack('i', len(json.dumps(msg))))  # 先发送消息的长度
            conn.send(json.dumps(msg).encode())
            # event为 MouseEventTypes类型
            #         EVENT_MOUSEMOVE  = 0    #滑动
            #         EVENT_LBUTTONDOWN  = 1  #左键点击
            #         EVENT_RBUTTONDOWN = 2   #右键点击
            #         EVENT_MBUTTONDOWN = 3   #中键点击
            #         EVENT_LBUTTONUP = 4     #左键放开
            #         EVENT_RBUTTONUP = 5     #右键放开
            #         EVENT_MBUTTONUP = 6     #中键放开
            #         EVENT_LBUTTONDBLCLK = 7 #左键双击
            #         EVENT_RBUTTONDBLCLK = 8 #右键双击
            #         EVENT_MBUTTONDBLCLK = 9 #中键双击
            # ————————————————
            # flags为MouseEventFlags类型：
            #         EVENT_FLAG_LBUTTON =1    #左键拖曳
            #         EVENT_FLAG_RBUTTON =2    #右键拖曳
            #         EVENT_FLAG_MBUTTON =4    #中键拖曳
            #         EVENT_FLAG_CTRLKEY =8    #按 Ctrl 不放
            #         EVENT_FLAG_SHIFTKEY =16  #按 Shift 不放
            #         EVENT_FLAG_ALTKEY =32    #按 Alt 不放

            print('event: {},  x: {},  y: {}  flags: {}'.format(event, x, y, flags))
        except socket.error as e:
            print(e)


if __name__ == '__main__':
    socket_service()