import wmi
import time
from remote_utils.wmi_remote_copy import run_local_command_with_output2, run_local_command_without_output, run_local_command_with_output


def execute_cmd_by_wmi(wmi_obj, cmd_str):
    """
    通过WMI（远程）执行命令
    :param wmi_obj: WMI对象，可以是本机，也可以是远程机（需有用户名密码）
    :param cmd_str: 需要在WMI指定的（远程）主机机上执行的命令
    :return:
    经测试，这种方法可以运行的shutdown等命令来关机或重启。
    但是，对于自己编写的程序，不能进行交互（例如，让屏幕静音，截图等都无法成功）。
    """
    process_startup = wmi_obj.Win32_ProcessStartup.new()
    SW_SHOWNORMAL = 1
    process_startup.ShowWindow = SW_SHOWNORMAL
    process_id, result = wmi_obj.Win32_Process.Create(CommandLine=cmd_str,
                                                      ProcessStartupInformation=process_startup)
    if result == 0:
        print("Process started successfully: [process_id:{}]".format(process_id))
    else:
        raise RuntimeError("Problem creating process: {}".format(result))


def execute_cmd_by_schtasks(cmd_str, remote_ip, remote_user, remote_password, taskname='mytest_task'):
    """
    通过schtasks命令，即计划任务，（远程）执行命令
    :param cmd_str: 要在远程主机上执行的命令
    :param remote_ip: 远程主机IP
    :param remote_user: 远程主机的用户名
    :param remote_password: 远程主机的密码
    :param taskname: 默认mytest_task
    :return: 无
    经测试，这种方式，可以出现用户界面UI，但是延迟时间稍慢一点。
    # Tips: 有时运行一次不行，可以多运行一次（原因暂未知）
    """
    remote_option_str = '/s {} /u {} /p {} /tn {}'.format(remote_ip, remote_user, remote_password, taskname)
    # 貌似只有不显示输出时，执行正常（虽然有点慢）。
    run_local_command_without_output('schtasks /delete {}'.format(remote_option_str))  # 先删除该名的task，以便下面创建
    run_local_command_without_output('schtasks /create {} /sc once /st 23:11 /tr "{}"'.format(remote_option_str, cmd_str))
    run_local_command_without_output('schtasks /run {} /i'.format(remote_option_str))


if __name__ == '__main__':
    start_time = time.time()
    my_wmi_obj = wmi.WMI(computer='192.168.68.223', user='ec1', password='12345678')  # Win10专业版物理机，还未连接成功
    # my_wmi_obj = wmi.WMI(computer='192.168.48.130',
    #                      user='lynulyq', password='12345678')  # VMWare里的Win7企业版，连接成功！
    # my_wmi_obj = wmi.WMI(computer='192.168.48.131',
    #                      user='Administrator', password='12345678') # VMWare里的WinXP专业版(关闭Windows防火墙后连接成功）
    # my_wmi_obj = wmi.WMI()

    cmd_call = r'shutdown -r -f -t 20 -c "检测到你没有认真做实验，系统将重启！"'  # 20秒内重启，测试成功
    execute_cmd_by_wmi(my_wmi_obj, cmd_call)
    # execute_cmd_by_wmi(my_wmi_obj, 'notepad') # 命令可以执行，但会在后台，无界面(win10物理机)？2023-08-02

    print('耗时{:.1f}秒'.format(time.time()-start_time))
