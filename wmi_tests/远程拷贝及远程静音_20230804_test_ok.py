from remote_utils.wmi_remote_copy import copy_local_file_to_remote, copy_remote_file_to_local, run_local_command_with_output2
from remote_utils.wmi_remote_exec import execute_cmd_by_wmi, execute_cmd_by_schtasks
import wmi

if __name__ == '__main__':
    # my_wmi_obj = wmi.WMI(computer='192.168.68.223', user='ec1', password='tplink')  # Win10专业版物理机，连接成功！
    # my_wmi_obj = wmi.WMI(computer='192.168.48.130',
    #                      user='lynulyq', password='12345678')  # VMWare里的Win7企业版，连接成功！
    # my_wmi_obj = wmi.WMI(computer='192.168.48.131',
    #                      user='Administrator', password='12345678') # VMWare里的WinXP专业版(关闭Windows防火墙后连接成功）

    # Step 1: copy the file to remote computer
    # 该步骤如果出错，有可能的原因是, Win10现在已经默认不支持WinXP/Win7里使用的SMB 1.x协议，需要安装此可选功能功能。
    # 另一种解决方法是，使用WMIHacker提供的命令行工具，它不需要安装SMB 1.x客户端。
    print('将black screen文件复制到远程主机')
    copy_local_file_to_remote(r'..\tools\black_screen_test1.exe', '192.168.48.130', 'lynulyq','12345678', 'wmi_classroom1.exe')

    # Step 2: execute remotely by cmd
    # 执行时注意，WinXP一般是32位的。因此拷贝过去的64位程序运行不了，因此不考虑支持WinXP。
    # 可以执行，进程列表里也有，但是没有效果？ 可能原因：出于安全方面的考虑，wmi不提供远程进程交互式的运行，所以只能看到进程，但看不到界面?
    # 截图也不行？
    # my_wmi_obj = wmi.WMI()
    # 尽管这种方式运行有点慢，但还是运行起来了！ 创建计划任务的方式，可以有界面（例如黑屏功能）！
    # Tips: 有时运行一次不行，可以多运行一次
    # C# 跨PC 远程调用程序并显示UI界面 https://zhuanlan.zhihu.com/p/609995299?utm_id=0
    print('开始使用schtasks方式执行远程命令: 远程静音')
    execute_cmd_by_schtasks(r'c:\wmi_classroom1.exe', '192.168.48.130', 'lynulyq', '12345678', taskname='screen_mute')

    # execute_cmd_by_wmi(my_wmi_obj, r'c:\wmi_classroom_jietu2.exe -f screen001.png')
    #
    # copy_remote_file_to_local('screen001.png', '192.168.48.130', 'lynulyq','tplink', r'D:\PycharmProjects\lyqNetTools\wmi_tests\remote_screen.png')