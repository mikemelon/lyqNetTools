from socket import socket, AF_INET, SOCK_DGRAM
import os
import tkinter
import pyautogui
import io


def black_screen():
    # 第4种方法，无需使用线程，用户在界面上输入study后退出。（目前推荐使用）
    root = tkinter.Tk()
    root.overrideredirect(True)
    root.config(bg="Black")
    x, y = root.winfo_screenwidth(), root.winfo_screenheight()  # 等于屏幕分辨率（像素）
    x, y = str(x), str(y)  # x = str((x-1000)) 替换为本行及下面行以让黑窗口左侧有1000空隙
    root.geometry((x + "x" + y + '+0+0'))  # root.geometry((x+"x"+y+'+1000+0')) 替换为本行及上面行以让黑窗口左侧有1000空隙
    root.wm_attributes("-topmost", 1)  # 一定要最后测试号再设置为置顶，否则无法操作，只能重启系统！！！

    ########## 第4种方法 begin ###########
    def get_value():
        input_str = entry.get()
        if input_str == 'study':
            # root.quit() # 在这里用quit()会造成程序无法响应，换用destroy()
            root.destroy()
            # sys.exit()
            return

    entry = tkinter.Entry(root)
    entry.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    button = tkinter.Button(root, text='请在上面输入框里输入"study"以退出黑屏', command=get_value)
    button.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)
    ########## 第4种方法 end ###########

    root.mainloop()


serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('The server is ready to receive')

while True:
    message, clientAddress = serverSocket.recvfrom(1024*1024)
    print('recv:{}, clientAddress:{}'.format(message, clientAddress))

    command_str = message.decode().upper()

    if command_str == 'RESTART':
        print('I will restart!')
        cmd_call = r'shutdown -r -f -t 5 -c "检测到你没有认真做实验，系统将重启！"'  # 20秒内重启，测试成功
        os.system(cmd_call)

        serverSocket.sendto(command_str.encode(), clientAddress)

    elif command_str == 'BLACK_SCREEN':
        print('I will black screen')
        black_screen()

        serverSocket.sendto(command_str.encode(), clientAddress)

    elif command_str == 'CAPTURE_SCREEN':
        print('I will capture your screen')
        im = pyautogui.screenshot()

        screenshots_file_path = r'c:\screen_shot888.png'
        im.save(screenshots_file_path)

        bytes_io = io.BytesIO()
        im.save(bytes_io, format='PNG')
        image_bytes = bytes_io.getvalue()

        serverSocket.sendto(image_bytes, clientAddress)
