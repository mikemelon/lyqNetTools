from pynput.keyboard import Controller, Key
import os
import time
import win32api
import win32gui
import win32process
import subprocess


def get_language():
    """获取当前输入法状态"""
    hwnd = win32gui.GetForegroundWindow()
    thread_id = win32api.GetWindowLong(hwnd, 0)
    klid = win32api.GetKeyboardLayout(thread_id)
    lid = klid & (2 ** 16 - 1)
    lid_hex = hex(lid)
    print(lid_hex)
    if lid_hex == '0x409':
        print('当前的输入法状态是英文输入模式\n\n')
    elif lid_hex == '0x804':
        print('当前的输入法是中文输入模式\n\n')
    else:
        print('当前的输入法既不是英文输入也不是中文输入\n\n')


def get_hwnds_for_pid(pid):
     def callback(hwnd, hwnds):
         if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
             _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
             if found_pid == pid:
                 hwnds.append(hwnd)
             return True
     hwnds=[]
     win32gui.EnumWindows(callback, hwnds)
     return hwnds


notepad_process = subprocess.Popen(['notepad.exe'], shell=False)
time.sleep(3)

_, foreground_pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
print('foreground_pid={}'.format(foreground_pid))
print('notepad_process.pid={}'.format(notepad_process.pid))


for hwnd in get_hwnds_for_pid(notepad_process.pid):
    print(hwnd, "=>", win32gui.GetWindowText(hwnd))
    win32gui.SetForegroundWindow(hwnd)

notepad_process.terminate()
# notepad_process.kill()
# os.system('taskkill /t /f /pid {}'.format(notepad_process.pid)) # /t 选项表示其子进程也关闭

# time.sleep(1)
# # get_language()
#
# keyboard = Controller()
# keyboard.press(Key.alt)  # 切换为英文输入法
# keyboard.press(Key.shift)
# keyboard.release(Key.shift)
# keyboard.release(Key.alt)
#
# # get_language()
# time.sleep(1)
#
# try:
#     keyboard.type('I love this world!')
#     time.sleep(5)
# except keyboard.InvalidCharacterException as e:
#     print(e)
# for n in 'I love this world!':
#     time.sleep(1)
#     print(n)
#     keyboard.press(n)
#     keyboard.release(n)