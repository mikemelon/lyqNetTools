from remote_utils.wmi_remote_copy import copy_local_file_to_remote
from remote_utils.wmi_remote_exec import execute_cmd_by_wmi
import wmi

if __name__ == '__main__':
    # my_wmi_obj = wmi.WMI(computer='192.168.68.223', user='ec1', password='tplink')  # Win10专业版物理机，连接成功！
    my_wmi_obj = wmi.WMI(computer='192.168.48.130',
                         user='lynulyq', password='tplink')  # VMWare里的Win7企业版，连接成功！
    # my_wmi_obj = wmi.WMI(computer='192.168.48.131',
    #                      user='Administrator', password='12345678') # VMWare里的WinXP专业版(关闭Windows防火墙后连接成功）

    # Step 1: copy the file to remote computer
    # 该步骤如果出错，有可能的原因是, Win10现在已经默认不支持WinXP/Win7里使用的SMB 1.x协议，需要安装此可选功能功能。
    # 另一种解决方法是，使用WMIHacker提供的命令行工具，它不需要安装SMB 1.x客户端。
    execute_cmd_by_wmi(my_wmi_obj, r'net use \\192.168.48.130 /user:lynulyq tplink')  # 如果提示用户名密码不正确，则应远程执行这句
    copy_local_file_to_remote(r'D:\PycharmProjects\lyqNetTools\dist\black_screen_test1.exe', '192.168.48.130', 'wmi_classroom2.exe')

    # Step 2: execute remotely by cmd
    # 执行时注意，WinXP一般是32位的。因此拷贝过去的64位程序运行不了
    # 可以执行，进程列表里也有，但是没有效果？ 可能原因：出于安全方面的考虑，wmi不提供远程进程交互式的运行，所以只能看到进程，但看不到界面；
    # my_wmi_obj = wmi.WMI()
    execute_cmd_by_wmi(my_wmi_obj, r'c:\wmi_classroom2.exe')