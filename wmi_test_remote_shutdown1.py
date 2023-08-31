import wmi
import time

start_time = time.time()
my_wmi_obj = wmi.WMI(computer='192.168.68.223', user='ec1', password='123456')  # Win10专业版物理机，还未连接成功
# my_wmi_obj = wmi.WMI(computer='192.168.48.130', user='lynulyq', password='123456')  # VMWare里的Win7企业版，连接成功！
# my_wmi_obj = wmi.WMI(computer='192.168.48.131', user='Administrator', password='12345678') # VMWare里的WinXP专业版(关闭Windows防火墙后连接成功）
# my_wmi_obj = wmi.WMI()

cmd_call = r'shutdown -r -f -t 20 -c "检测到你没有认真做实验，系统将重启！"'  # 20秒内重启，测试成功
# cmd_call = r'c:\mytest.bat'  # 20秒内重启
process_startup = my_wmi_obj.Win32_ProcessStartup.new()
SW_SHOWNORMAL = 1
process_startup.ShowWindow = SW_SHOWNORMAL
process_id, result = my_wmi_obj.Win32_Process.Create(CommandLine=cmd_call,
                                                     ProcessStartupInformation=process_startup)
if result == 0:
    print("Process started successfully: {}".format(process_id))
else:
    raise RuntimeError("Problem creating process: {}".format(result))
print('耗时{:.1f}秒'.format(time.time()-start_time))
