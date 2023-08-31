import wmi
import time


def get_cpu_name(wmi_obj):
    for item in wmi_obj.Win32_Processor():
        return item.Name


def get_os_name(wmi_obj):
    info_list = []
    for item in wmi_obj.Win32_OperatingSystem():
        info_list.append(item.Caption)
        # info_list.append(item.OSArchitecture) # WinXP不支持
    return ', '.join(info_list)


def get_mem_capacity(wmi_obj):
    for item in wmi_obj.Win32_ComputerSystem():
        return '{:.1f} GB'.format(int(item.TotalPhysicalMemory)/1024/1024/1024)  # 单位G


def get_disk_capacity(wmi_obj):
    disk_list = []
    for idx, item in enumerate(wmi_obj.Win32_DiskDrive()):
        disk_list.append('[{}]{}:{:.0f} GB'.format(idx+1, item.Model, int(item.Size)/1000/1000/1000))  # 单位G
    return '\t'.join(disk_list)


def get_video_controllers(wmi_obj):
    video_controller_list = []
    for idx, item in enumerate(wmi_obj.Win32_VideoController()):
        video_controller_list.append('[{}]{}'.format(idx+1, item.Name))
    return '\t'.join(video_controller_list)


def get_sound_devices(wmi_obj):
    sound_devices_list = []
    for idx, item in enumerate(wmi_obj.Win32_SoundDevice()):
        sound_devices_list.append('[{}]{}'.format(idx+1, item.Name))
    return '\t'.join(sound_devices_list)


start_time = time.time()
my_wmi_obj = wmi.WMI(computer='192.168.68.223', user='ec1', password='12345678', find_classes=False)  # Win10专业版物理机，连接成功！
# my_wmi_obj = wmi.WMI(computer='192.168.48.130', user='lynulyq', password='123455678', find_classes=False)  # VMWare里的Win7企业版，连接成功！
# my_wmi_obj = wmi.WMI(computer='192.168.48.131', user='Administrator', password='12345678', find_classes=False) # VMWare里的WinXP专业版(关闭Windows防火墙后连接成功）
# my_wmi_obj = wmi.WMI(find_classes=False)
# loc = win32com.client.Dispatch("WbemScripting.SWbemLocator")
# svc = loc.ConnectServer(...)
# my_wmi_obj = wmi.WMI(wmi=svc)
# print(type(my_wmi_obj))

print('CPU:\t\t\t{}'.format(get_cpu_name(my_wmi_obj)))
print('操作系统:\t\t\t{}'.format(get_os_name(my_wmi_obj)))
print('内存:\t\t\t{}'.format(get_mem_capacity(my_wmi_obj)))
print('磁盘:\t\t\t{}'.format(get_disk_capacity(my_wmi_obj)))
print('显卡:\t\t\t{}'.format(get_video_controllers(my_wmi_obj)))
print('声卡:\t\t\t{}'.format(get_sound_devices(my_wmi_obj)))
print('耗时{:.1f}秒'.format(time.time()-start_time))
