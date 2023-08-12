import tkinter
from pyautogui import size
import threading
import time
import sys
import keyboard

# 提供4种方法，实现让屏幕黑屏。
# 前3种方法，退出时都需要使用额外的线程），
# 第4种方法，无需使用线程，用户在界面上输入study后退出。（目前推荐使用）


def exit_with_enter1(tk_root):  # 等待3秒退出（第1种方法）
    time.sleep(3)
    tk_root.quit()
    sys.exit()


def exit_with_enter2(tk_root):  # 按下ESC键退出（第2种方法）
    while True:
        if keyboard.is_pressed('esc'):
            tk_root.quit()
            sys.exit()


def exit_with_enter3(tk_root): # 用户在命令行里输入study正确后退出（第3种方法）
    while True:
        input_str = input('please input study to quit:')
        if input_str == 'study':
            print('ok!')
            tk_root.quit()
            sys.exit()
        print('again!')


root = tkinter.Tk()
root.overrideredirect(True)
root.config(bg="Black")
x,y = size()  # 等于屏幕分辨率（像素）
x = str(x) # x = str((x-1000)) 替换为本行及下面行以让黑窗口左侧有1000空隙
y = str(y)
root.geometry((x+"x"+y+'+0+0'))  # root.geometry((x+"x"+y+'+1000+0')) 替换为本行及上面行以让黑窗口左侧有1000空隙
root.wm_attributes("-topmost", 1)  # 一定要最后测试号再设置为置顶，否则无法操作，只能重启系统！！！
# threading.Thread(target=exit_with_enter1, args=(root,)).start()  # 开启线程，提供退出的可能，第1种方法
# threading.Thread(target=exit_with_enter2, args=(root,)).start()  # 开启线程，提供退出的可能，第2种方法
# threading.Thread(target=exit_with_enter3, args=(root,)).start()  # 开启线程，提供退出的可能，第3种方法

########## 第4种方法 begin ###########
def get_value():
    input_str =  entry.get()
    if input_str == 'study':
        root.quit()
        sys.exit()


entry = tkinter.Entry(root)
entry.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
button = tkinter.Button(root, text='请在上面输入框里输入"study"以退出黑屏', command=get_value)
button.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)
########## 第4种方法 end ###########

root.mainloop()
