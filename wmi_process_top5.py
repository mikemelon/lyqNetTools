import wmi
import time

start_time = time.time()
my_wmi_obj = wmi.WMI()
# my_wmi_obj = wmi.WMI(computer='192.168.68.223', user='ec1', password='12345678') # Win10专业版物理机，还未连接成功
# my_wmi_obj = wmi.WMI(computer='192.168.48.130',
#                      user='lynulyq', password='12345678')  # VMWare里的Win7企业版，连接成功！
# my_wmi_obj = wmi.WMI(computer='192.168.48.131',
#                      user='Administrator', password='12345678') # VMWare里的WinXP专业版(关闭Windows防火墙后连接成功）

process_list = my_wmi_obj.Win32_Process()
# print('process数量：{}'.format(len(process_list)))
# print('{:.1f} seconds elapsed'.format(time.time()-start_time))
process_dict = dict((e.Handle, e.ExecutablePath) for e in process_list if e.Handle != '0')  # 排除pid=0即System Idle Process
perf_item_list = my_wmi_obj.Win32_PerfFormattedData_PerfProc_Process()
# print('perf process数量：{}'.format(len(perf_item_list)))
# print('{:.1f} seconds elapsed'.format(time.time()-start_time))

perf_dict = dict((str(e.IDProcess), (e.Name, e.PercentProcessorTime, e.PercentUserTime, e.WorkingSetPrivate)) for e in perf_item_list if e.Name != '_Total' and e.IDProcess != 0)

# print('PercentProcessorTime top 5: ',sorted(perf_dict.items(), key=lambda x:int(x[1][1]), reverse=True)[:5])
# print('PercentUserTime top 5: ',sorted(perf_dict.items(), key=lambda x:int(x[1][2]), reverse=True)[:5])
print('占用CPU最多的5个进程及其程序位置：')
cpu_item_list = sorted(perf_dict.items(), key=lambda x:int(x[1][1]), reverse=True)[:5]
print('{:<10}{:<30}{:<20}{}'.format('Order', 'Proess Name', 'CPU Percent', '可执行程序完整路径'))
print('-'*120)
for idx, item in enumerate(cpu_item_list):
    try:
        exe_path = process_dict[item[0]]
    except KeyError:
        exe_path = ''
    print('{:<10}{:<30}{:<20}{}'.format(idx+1, item[1][0], item[1][1], exe_path))


# print('WorkingSetPrivate top 5: ',sorted(perf_dict.items(), key=lambda x:int(x[1][3]), reverse=True)[:5])
print('\n占用内存最多的5个进程及其程序位置：')
mem_item_list = sorted(perf_dict.items(), key=lambda x:int(x[1][3]), reverse=True)[:5]
print('{:<10}{:<30}{:<20}{}'.format('Order', 'Proess Name', 'Memory size', '可执行程序完整路径'))
print('-'*120)
for idx, item in enumerate(mem_item_list):
    try:
        exe_path = process_dict[item[0]]
    except KeyError:
        exe_path = ''
    print('{:<10}{:<30}{:<20}{}'.format(idx+1, item[1][0], str(int(int(item[1][3])/1024/1024))+"M", exe_path))


print('-----')
print('{:.1f} seconds elapsed'.format(time.time()-start_time))
