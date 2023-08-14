import time
import os
import win32con
import win32api
import win32gui
import win32process
import ctypes
import subprocess
import psutil
import wmi
from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Controller as MouseController, Button


def get_language():
    """获取当前输入法状态"""
    hwnd = win32gui.GetForegroundWindow()
    thread_id = win32api.GetWindowLong(hwnd, 0)
    klid = win32api.GetKeyboardLayout(thread_id)
    lid = klid & (2 ** 16 - 1)
    lid_hex = hex(lid)
    # print(lid_hex)
    if lid_hex == '0x409':
        print('当前的输入法状态是英文输入模式\n\n')
        return 'en'
    elif lid_hex == '0x804':
        print('当前的输入法是中文输入模式\n\n')
        return 'cn'
    else:
        print('当前的输入法既不是英文输入也不是中文输入\n\n')
        return 'other'


def change_ime_to_en(keyboard):
    if get_language() == 'cn':
        keyboard.press(Key.alt)  # 切换为英文输入法
        keyboard.press(Key.shift)
        keyboard.release(Key.shift)
        keyboard.release(Key.alt)
        time.sleep(1)
        # get_language()


def key_type_string(keyboard, str, delay=1.0):
    for s in str:
        if s==' ':
            keyboard.press(Key.space)
            keyboard.release(Key.space)
        else:
            keyboard.press(s)
            keyboard.release(s)
        time.sleep(delay)


def get_all_pids_by_name(name):
    wmi_obj = wmi.WMI()
    process_list = wmi_obj.Win32_Process()
    pids = [int(p.Handle) for p in process_list if p.Name.lower() == name.lower()]
    return pids


def get_hwnds_for_pid(pid):
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                hwnds.append(hwnd)
            return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds


def get_process_and_children(pid):
    process = psutil.Process(pid)
    process_list = []
    process_list.append(pid)
    process_list.extend([p.pid for p in process.children(recursive=True)])
    return process_list


def get_process_and_parent(pid):
    process = psutil.Process(pid)
    plist = []
    plist.append(pid)
    plist.append(process.ppid())
    return plist


# 获取真实的窗口 POS
# Python 桌面程序开发 解决 win32gui 获取的位置不准的问题
# https://blog.csdn.net/qq_15071263/article/details/122243711
def get_window_rect(hwnd):
    try:
        f = ctypes.windll.dwmapi.DwmGetWindowAttribute
    except WindowsError:
        f = None
    if f:
        rect = ctypes.wintypes.RECT()
        f(ctypes.wintypes.HWND(hwnd), ctypes.wintypes.DWORD(9), ctypes.byref(rect), ctypes.sizeof(rect))
        return rect.left, rect.top, rect.right, rect.bottom


def get_win10_scale_factor():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
    except:
        print('exception occur when getting scale factor!')
        pass

    user32 = ctypes.windll.user32
    dpi_scaling = user32.GetDpiForWindow(user32.GetDesktopWindow())
    return dpi_scaling/96.0


# 未测试，#TODO: 在Win7下获取scale_factor，并测试
def get_win7_scale_factor():
    user32 = win32api.GetModuleHandle("user32")
    dpi_scaling = win32api.GetDpiForWindow(user32)
    print("Win7系统的缩放大小为：{}".format(dpi_scaling))


def auto_open_notepad_and_type_str(english_str, wait_before_close_in_seconds=5):
    notepad_process = subprocess.Popen(['notepad'], shell=False)
    time.sleep(1)

    pids_list = get_all_pids_by_name('notepad.exe') # 名称用小写，便于比较
    print('pids_list(with name "Notepad.exe")={}'.format(pids_list))

    # _, foreground_pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    foreground_hwnd = win32gui.GetForegroundWindow()
    print('foreground_hwnd={}'.format(foreground_hwnd))
    # print('foreground_pid={}'.format(foreground_pid))
    print('notepad_process.pid={}'.format(notepad_process.pid))
    resolution = (win32api.GetSystemMetrics(win32con.SM_CXSCREEN), win32api.GetSystemMetrics(win32con.SM_CYSCREEN))
    print('resolution={}'.format(resolution))
    if notepad_process.pid in pids_list:
        # win32gui.SetWindowPos(foreground_hwnd, win32con.HWND_NOTOPMOST,
        #                       int(resolution[0]/2) - 400, int(resolution[1]/2)-300, 800, 600,
        #                       win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)

        left, top, right, bottom = get_window_rect(foreground_hwnd)
        print(left, top, right, bottom)
        center_x = (right - left)/2
        center_y = (bottom - top)/2
        mouse = MouseController()

        # scale_factor = get_win10_scale_factor()
        mouse.position = (int(center_x), int(center_y)) # 仍不能移动鼠标到窗口中心点  #TODO: 移动鼠标到屏幕中心点
        # mouse.position  = resolution
        mouse.click(Button.left)

        keyboard = KeyboardController()
        change_ime_to_en(keyboard) # 我自己的Win11上可以用, Win10上失效
        # 如下方式切换输入法，Win10上仍然失效
        # TODO: Win10上也能切换输入法
        result = win32api.SendMessage(foreground_hwnd, win32con.WM_INPUTLANGCHANGEREQUEST, 0, 0x0409)
        if result == 0:
            print('设置英文键盘成功！')
        time.sleep(1)

        # print('hwnd={}, hwnd rect={}'.format(hwnd, get_window_rect(hwnd)))
        # left, top, right, bottom = get_window_rect(win32gui.GetForegroundWindow())

        mouse.move(5,5)
        time.sleep(1)
        key_type_string(keyboard, english_str, delay=0.1)

        time.sleep(wait_before_close_in_seconds)
        os.system('taskkill /t /f /pid {}'.format(notepad_process.pid))
        # notepad_process.terminate()


if __name__ == '__main__':
    get_win7_scale_factor()
    auto_open_notepad_and_type_str('Do you have finished the task?')
