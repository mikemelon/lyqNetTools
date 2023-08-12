from remote_utils.wmi_remote_copy import copy_local_file_to_remote, copy_remote_file_to_local, run_local_command_with_output2
from remote_utils.wmi_remote_exec import execute_cmd_by_wmi, execute_cmd_by_schtasks
import time
from PIL import Image

if __name__ == '__main__':

    print('将screen shot所用的可执行文件复制到远程主机')
    copy_local_file_to_remote(r'..\tools\capture_screen1.exe', '192.168.48.130', 'lynulyq','12345678', 'wmi_classroom2.exe', with_output=True)

    print('开始使用schtasks方式执行远程命令：截图')
    execute_cmd_by_schtasks(r'if exist c:\screen_shot.png (del c:\screen_shot.png) & c:\wmi_classroom2.exe', '192.168.48.130', 'lynulyq', '12345678', taskname='task_screen_shot')

    time.sleep(10)

    print('将截图回传本地')  # 这一步不知为何总是截图不是最新的，如黑屏
    copy_remote_file_to_local('screen_shot.png', '192.168.48.130', 'lynulyq', '12345678', r'd:\PycharmProjects\lyqNetTools\wmi_tests\remote_screen_shott001.png')

    img = Image.open(r'd:\PycharmProjects\lyqNetTools\wmi_tests\remote_screen_shott001.png')
    img.show()

