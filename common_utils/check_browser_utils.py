import os
import win32api
import win32con


def check_microsoft_edge():
    # 如下方法可以找到Edge的默认安装
    edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application'
    if os.path.exists(os.path.join(edge_path,'msedge.exe')):
        # print('Microsoft Edge Found!')
        return os.path.join(edge_path,'msedge.exe')
    else:
        print('No Microsoft Edge found!')


def check_google_chrome():
    # 如下方法可以找到Chrome的默认安装，更保险！
    # print(os.path.join(os.environ.get('LOCALAPPDATA'), r'Google\Chrome\Application', 'chrome.exe'))
    chrome_path = os.path.join(os.environ.get('LOCALAPPDATA'), r'Google\Chrome\Application', 'chrome.exe')
    if os.path.exists(chrome_path):
        # print('Found Chrome finally!')
        return chrome_path
    else:
        print('No Chrome found!')


def check_google_chrome_by_reg():
    # 使用查找注册表的方式，定位chrome.exe的路径，最准确！
    # python 获取chrome浏览器的安装目录，即chrome的绝对路径 https://blog.csdn.net/m0_47505062/article/details/129078341
    py_hkey_obj = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
                          r'Software\Microsoft\Windows\CurrentVersion\App paths\chrome.exe',
                          0, win32con.KEY_READ)
    chrome_path = win32api.RegQueryValueEx(py_hkey_obj, '')[0]
    win32api.RegCloseKey(py_hkey_obj) # 微软建议用完了注册表要关闭
    # print(chrome_path)
    if os.path.exists(chrome_path):
        # print('Chrome is realy exist!')
        return chrome_path
    else:
        print('No Chrome found!')


def check_google_chrome_by_reg2():
    # 另外一种查找注册表的方式，注册表位置不一样，见：https://blog.csdn.net/u013314786/article/details/122497226
    py_hkey_obj2 = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
                          r'Software\Clients\StartMenuInternet', 0, win32con.KEY_READ)
    # RegQueryInfoKey()方法返回3个值：项的子项数目、项值数目，以及最后一次修改时间
    sub_key_nums, _, _ = win32api.RegQueryInfoKey(py_hkey_obj2)
    print(r'Software\Clients\StartMenuInternet下共有{}个子项-->'.format(sub_key_nums))
    for n in range(sub_key_nums):
        cur_key_name = win32api.RegEnumKey(py_hkey_obj2, n)
        print('\t子项{}:{}'.format(n+1, cur_key_name))
        if 'Chrome' in cur_key_name:
            key_path = r'Software\Clients\StartMenuInternet' + '\\' + cur_key_name + '\\DefaultIcon'
            py_hkey_obj3 = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
                                                 key_path, 0, win32con.KEY_READ)
            # 这个值是个字符串，由两部分构成用逗号分隔
            chrome_path = win32api.RegQueryValueEx(py_hkey_obj3, '')[0].split(',')[0]
            # print(chrome_path)
            if os.path.exists(chrome_path):
                # print('Chrome is surely exists!')
                return chrome_path
        else:
            print('other Browser exist:{}'.format(cur_key_name))

    print('No Chrome found!')


def check_browser_with_path():
    """
    检查浏览器及其路径。目前的实现：先检查Microsoft Edge, 再检查Google Chrome。
    :return: (浏览器类型，路径) 的元组，如果返回None，则说明没找到。
    """
    browser_path = check_microsoft_edge()
    if browser_path:
        return 'edge', browser_path

    browser_path = check_google_chrome_by_reg()
    if browser_path:
        return 'chrome', browser_path

    return None, None


if __name__ == '__main__':
    # 如下方法可以找到Chrome的默认安装
    # chrome_path = r'C:\Users\mikemelon2021\AppData\Local\Google\Chrome\Application'
    # if os.path.exists(os.path.join(chrome_path, 'chrome.exe')):
    #     print('Google Chrome Found!')
    print(os.environ.get('APPDATA'))
    print(os.environ.get('HOMEDRIVE') + os.environ.get('HOMEPATH'))
    print(os.environ.get('LOCALAPPDATA'))
    print('-'*30)

    # browser_path = check_google_chrome()
    browser_path = check_microsoft_edge()
    # browser_path = check_google_chrome_by_reg()
    # browser_path = check_google_chrome_by_reg2()
    if browser_path:
        print('浏览器程序所在路径：', browser_path)

    print(check_browser_with_path())
