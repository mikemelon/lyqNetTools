from socket import socket, AF_INET, SOCK_STREAM
import tkinter
from PIL import ImageGrab
import io
import os
import subprocess
from common_utils.config_loader import get_config
from common_utils.file_utils import save_screencapture_as_formatted_filename
from common_utils.check_browser_utils import check_browser_with_path
from remote_utils.auto_typing import auto_open_notepad_and_type_str
import threading
import remote_desktop.client as rd_client
import pythoncom

# 相比TCPServer.py，本程序改为收到一个命令就启动一个线程，即以多线程方式执行命令。
browser_process = None  # 浏览器进程，用于“桌面广播”功能


def black_screen():
    # 第4种方法，无需使用线程，用户在界面上输入study后退出。（目前推荐使用）
    root = tkinter.Tk()
    root.overrideredirect(True)
    root.config(bg="Black")
    x, y = root.winfo_screenwidth(), root.winfo_screenheight()  # 等于屏幕分辨率（像素）
    x, y = str(x), str(y)  # x = str((x-1000)) 替换为本行及下面行以让黑窗口左侧有1000空隙
    root.geometry((x + "x" + y + '+0+0'))  # root.geometry((x+"x"+y+'+1000+0')) 替换为本行及上面行以让黑窗口左侧有1000空隙
    root.wm_attributes("-topmost", 1)  # 一定要最后测试号再设置为置顶，否则无法操作，只能重启系统！！！
    black_screen_exit_word = get_config('remote_control', 'black_screen_exit_word')

    def get_value():
        input_str = entry.get()
        if input_str == black_screen_exit_word:
            # root.quit() # 在这里用quit()会造成程序无法响应，换用destroy()
            root.destroy()
            # sys.exit()
            return

    entry = tkinter.Entry(root)
    entry.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    notice_text = '请在上面输入框里输入"' + black_screen_exit_word + '"以退出黑屏'
    button = tkinter.Button(root, text=notice_text, command=get_value)
    button.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)
    root.mainloop()


def deal_connection(connection_socket, addr):
    global browser_process  # 浏览器进程，用于“桌面广播”功能
    print('TCPServer收到来自{}的远程地址连接：'.format(addr))
    sentence = connection_socket.recv(5 * 1024 * 1024).decode()
    print('recv:{}, connectionSocket:{}'.format(sentence, connection_socket))
    command_str = sentence.upper()

    if command_str == 'RESTART':
        print('I will restart!')
        restart_notice_message = get_config('remote_control', 'restart_notice_message')
        restart_wait_seconds = get_config('remote_control', 'restart_wait_seconds')
        cmd_call = r'shutdown -r -f -t ' + restart_wait_seconds + ' -c ' + restart_notice_message  # 20秒内重启，测试成功
        os.system(cmd_call)

        connection_socket.send(command_str.encode())

    elif command_str == 'BLACK_SCREEN':
        print('I will black screen')
        black_screen()

        connection_socket.send(command_str.encode())

    elif command_str == 'CAPTURE_SCREEN':
        print('I will capture your screen')
        # im = pyautogui.screenshot()
        # im = ImageGrab.grab()  # 从pyautogui方式抓图，改为PIL的ImageGrab抓图
        # screenshots_file_path = "c:\\screen_shot888.png"  # 可以不存
        # im.save(screenshots_file_path)
        saving_flag = get_config('remote_control', 'screen_saving_on_server', to_bool=True)
        if saving_flag:
            im = save_screencapture_as_formatted_filename()
        else:
            im = ImageGrab.grab()  # 从pyautogui方式抓图，改为PIL的ImageGrab抓图
        bytes_io = io.BytesIO()
        im.save(bytes_io, format='PNG')
        image_bytes = bytes_io.getvalue()

        connection_socket.send(image_bytes)

    elif command_str == 'AUTO_TYPING':
        print('I will let you typing some characters')
        pythoncom.CoInitialize()  # 由于auto_open_notepad_and_type_str()方法里有用到wmi，且在线程中启动，必须初始化和反初始化
        auto_typing_sentence = get_config('remote_control', 'auto_typing_sentence')
        auto_open_notepad_and_type_str(auto_typing_sentence)
        pythoncom.CoUninitialize()
        connection_socket.send(command_str.encode())

    elif 'REMOTE_DESKTOP' in command_str:
        _,  rd_server_host, rd_server_port = command_str.split()
        rd_client.socket_client(rd_server_host, int(rd_server_port))

        connection_socket.send(command_str.encode())

    elif 'OPEN_DESKTOP_BROADCAST' in command_str:
        _,  broadcast_server_host, broadcast_server_port = command_str.split()
        browser_type, browser_path = check_browser_with_path()
        if browser_type:
            broadcast_viewing_address = ('http://' + broadcast_server_host + ':' + broadcast_server_port
                                         + '/lyq_webrtcstreamer.html?video=screen://3')
            if browser_type == 'edge':  # 进入Microsoft Edge的kiosk模式
                browser_process = subprocess.Popen([browser_path, '--kiosk', broadcast_viewing_address,
                                                    '--edge-kiosk-type=fullscreen'], shell=False)
            elif browser_type == 'chrome':  # 进入Google Chrome的kiosk模式
                browser_process = subprocess.Popen([browser_path, '--kiosk', '-fullscreen',
                                                    broadcast_viewing_address], shell=False)

        else:
            print('No suitable Browser Found')  # TODO: 显示一个对话框
    elif command_str == 'CLOSE_DESKTOP_BROADCAST':
        try:
            if browser_process:
                browser_process.terminate()
                browser_process.kill()
        except Exception as ex:
            print('Exception while Stopping browser process:', ex)

    connection_socket.close()


if __name__ == '__main__':
    serverPort = get_config('remote_control', 'server_port', to_int=True)  # default 12000
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    print('The Remote Control TCPServer is ready to receive')
    while True:
        conn_socket, remote_addr = serverSocket.accept()
        t = threading.Thread(target=deal_connection, args=(conn_socket, remote_addr))
        t.start()
