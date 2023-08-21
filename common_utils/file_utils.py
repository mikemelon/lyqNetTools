import datetime
import os
import socket
from PIL import ImageGrab


def save_screencapture_as_formatted_filename():
    now = datetime.datetime.now()
    # print(now)
    formatted_time = now.strftime('%Y%m%d%H%M%S')  # 2023-01-01 13:00:01 --> 20230101130001
    # print(formatted_time)
    upper_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    im = ImageGrab.grab()
    # socket包获取的本机IP有时不准确，但由于客户端无法安装scapy，暂且用它
    local_ip_address = socket.gethostbyname(socket.gethostname())
    image_abs_path = os.path.join(upper_dir, 'screencaptures', 'screencapture_' + local_ip_address +'_'+formatted_time+'.png')
    im.save(image_abs_path)
    # im.show()
    return im


def save_im_as_formatted_filename(im, ip_address):
    now = datetime.datetime.now()
    formatted_time = now.strftime('%Y%m%d%H%M%S')  # 2023-01-01 13:00:01 --> 20230101130001
    upper_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    image_abs_path = os.path.join(upper_dir, 'screencaptures',
                                  'screencapture_' + ip_address + '_' + formatted_time + '.png')
    im.save(image_abs_path)


if __name__ == '__main__':
    im = save_screencapture_as_formatted_filename()
    im.show()
