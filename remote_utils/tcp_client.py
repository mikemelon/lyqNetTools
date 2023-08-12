from socket import socket, AF_INET, SOCK_STREAM
from PIL import Image
import io


def tcp_send_command(ip_address, cmd_str):
    """
    作为TCP客户端向TCP服务端发送（远程控制）命令
    除了截屏功能（第3个命令）外，其他命令执行完毕后，都将回显该命令。
    截屏命令，将打开远程服务端计算机的截屏图片

    :param ip_address: 远程控制服务端的IP地址
    :param cmd_str: 要发送的远程控制命令，目前支持3种（大小写均可，服务端统一转为大写）
                    (1)RESTART   重新启动服务端计算机
                    (2)BLACK_SCREEN  使得服务端计算机黑屏，输入study退出黑屏
                    (3)CAPTURE_SCREEN  抓取服务端计算机屏幕截图，并返回客户端
    :return: 无
    """
    serve_port = 12000
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((ip_address, serve_port))

    client_socket.send(cmd_str.encode())
    received_message = client_socket.recv(5*1024*1024)

    if cmd_str.upper() == 'CAPTURE_SCREEN':
        print('picture saved!')
        im_show = Image.open(io.BytesIO(received_message))
        # im_show.save('mytest.png')  # 可以存，也可以直接打开
        im_show.show()
    else:
        print('From Server:', received_message.decode())

    client_socket.close()


if __name__ == '__main__':
    # tcp_send_command('192.168.48.130','restart')
    # tcp_send_command('192.168.48.130', 'black_screen')
    tcp_send_command('192.168.48.130', 'capture_screen')
