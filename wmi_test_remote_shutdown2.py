import time
import wmi
from remote_utils.wmi_remote_exec import execute_cmd_by_wmi

if __name__ == '__main__':
    start_time = time.time()
    my_wmi_obj = wmi.WMI(computer='192.168.68.223', user='ec1', password='tplink')  # Win10专业版物理机，还未连接成功
    # my_wmi_obj = wmi.WMI(computer='192.168.48.130',
    #                      user='lynulyq', password='tplink')  # VMWare里的Win7企业版，连接成功！
    # my_wmi_obj = wmi.WMI(computer='192.168.48.131',
    #                      user='Administrator', password='12345678') # VMWare里的WinXP专业版(关闭Windows防火墙后连接成功）
    # my_wmi_obj = wmi.WMI()

    cmd_call = r'shutdown -r -f -t 20 -c "检测到你没有认真做实验，系统将重启！"'  # 20秒内重启，测试成功
    execute_cmd_by_wmi(my_wmi_obj, cmd_call)

    print('耗时{:.1f}秒'.format(time.time()-start_time))
