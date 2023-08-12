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
        return '{:.1f} GB'.format(int(item.TotalPhysicalMemory) / 1024 / 1024 / 1024)  # 单位G


def get_disk_capacity(wmi_obj):
    disk_list = []
    for idx, item in enumerate(wmi_obj.Win32_DiskDrive()):
        disk_list.append('[{}]{}:{:.0f} GB'.format(idx + 1, item.Model, int(item.Size) / 1000 / 1000 / 1000))  # 单位G
    return '\t'.join(disk_list)


def get_video_controllers(wmi_obj):
    video_controller_list = []
    for idx, item in enumerate(wmi_obj.Win32_VideoController()):
        video_controller_list.append('[{}]{}'.format(idx + 1, item.Name))
    return '\t'.join(video_controller_list)


def get_sound_devices(wmi_obj):
    sound_devices_list = []
    for idx, item in enumerate(wmi_obj.Win32_SoundDevice()):
        sound_devices_list.append('[{}]{}'.format(idx + 1, item.Name))
    return '\t'.join(sound_devices_list)


def get_summary_info(wmi_obj):
    info_str = 'CPU:\t\t\t{}'.format(get_cpu_name(wmi_obj)) + '\n'
    info_str += '操作系统:\t\t\t{}'.format(get_os_name(wmi_obj)) + '\n'
    info_str += '内存:\t\t\t{}'.format(get_mem_capacity(wmi_obj)) + '\n'
    info_str += '磁盘:\t\t\t{}'.format(get_disk_capacity(wmi_obj)) + '\n'
    info_str += '显卡:\t\t\t{}'.format(get_video_controllers(wmi_obj)) + '\n'
    info_str += '声卡:\t\t\t{}'.format(get_sound_devices(wmi_obj))
    return info_str


def get_app_installed(wmi_obj):
    # 按照安装时间顺序显示最新安装的“非著名”应用软件（有些应用可能无法显示，只有用Windows Installer安装的才显示，速度很慢，见下面链接）
    # https://xkln.net/blog/please-stop-using-win32product-to-find-installed-software-alternatives-inside/
    known_name_list = ['microsoft', 'intel', 'oracle', 'python', 'adobe', 'steinberg', 'vmware',
                       'hp inc.', 'ttkn', 'synaptics', 'amd inc.', 'advanced micro devices']
    app_list = wmi_obj.Win32_Product()
    print('查询到的全部软件共有{}个'.format(len(app_list)))
    new_app_list = []
    for p in app_list:
        known_flag = False
        try:
            for name in known_name_list:
                if name in p.Vendor.lower() or name in p.Name.lower():
                    known_flag = True
                    break
        except Exception as e:
            continue
        if not known_flag:
            new_app_list.append((p.Name, p.Vendor, p.InstallDate))
        # print(p)
    app_sorted = sorted(new_app_list, key=lambda x: x[2], reverse=True)  # 按照安装顺序，新安装的在前
    app_list_str = ''
    for app in app_sorted:
        app_list_str = app_list_str + str(app) + '\n'
    return app_list_str


# 显示所有共享文件夹（包含隐藏共享）
def get_share_folders(wmi_obj):
    share_list = []
    for idx, share in enumerate(wmi_obj.Win32_Share()):
        share_list.append('[{}]{}-->\t{}'.format(idx + 1, share.Name, share.Path))
    return '\n'.join(share_list)


# 显示磁盘详细信息
def get_disk_detail_info(wmi_obj):
    disk_info_list = []
    for idx, physical_disk in enumerate(wmi_obj.Win32_DiskDrive()):
        for partition in physical_disk.associators("Win32_DiskDriveToDiskPartition"):
            for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                disk_info_list.append('[{}]物理磁盘名：{}\n   分区名：{}\n   逻辑磁盘名：{}  {:.2f}% 空闲'
                                      .format(idx + 1, physical_disk.Caption, partition.Caption, logical_disk.Caption,
                                             (100.0 * int(logical_disk.FreeSpace) / int(logical_disk.Size))))
    return '\n'.join(disk_info_list)


# 显示各有IP地址的网卡的MAC地址和各IP
def get_network_devices(wmi_obj):
    network_info_list = []
    for idx, interface in enumerate(wmi_obj.Win32_NetworkAdapterConfiguration(IPEnabled=1)):
        ip_address_list = []
        for ip_address in interface.IPAddress:
            ip_address_list.append(ip_address)
        network_info_list.append('[{}]{}\nMAC地址：{}\nIP地址：{}'
                                 .format(idx + 1, interface.Description,
                                         interface.MACAddress, '\t\t'.join(ip_address_list)))
    return '\n\n'.join(network_info_list)


if __name__ == '__main__':
    start_time = time.time()

    # my_wmi_obj = wmi.WMI(computer='192.168.68.223', user='ec1', password='tplink')  # Win10专业版物理机，连接成功！
    my_wmi_obj = wmi.WMI(computer='192.168.48.130',
                         user='lynulyq', password='12345678')  # VMWare里的Win7企业版，连接成功！
    # my_wmi_obj = wmi.WMI(computer='192.168.48.131',
    #                      user='Administrator', password='12345678') # VMWare里的WinXP专业版(关闭Windows防火墙后连接成功）
    # my_wmi_obj = wmi.WMI()
    # loc = win32com.client.Dispatch("WbemScripting.SWbemLocator")
    # svc = loc.ConnectServer(...)
    # my_wmi_obj = wmi.WMI(wmi=svc)
    # print(type(my_wmi_obj))

    print(('系统信息汇总：\n' + '-' * 40 + '\n{}').format(get_summary_info(my_wmi_obj)))
    print(('\n共享文件夹信息：\n' + '-' * 40 + '\n{}').format(get_share_folders(my_wmi_obj)))
    print(('\n磁盘详细信息：\n' + '-' * 40 + '\n{}').format(get_disk_detail_info(my_wmi_obj)))
    print(('\n网络设备详细信息：\n' + '-' * 40 + '\n{}').format(get_network_devices(my_wmi_obj)))
    # print('\n除了常用软件外的非著名软件有：\n' + '-'*40 + '\n', get_app_installed(my_wmi_obj))

    print('耗时{:.1f}秒'.format(time.time() - start_time))
