import wmi
import time
import datetime
from pprint import pprint

start_time = time.time()
c = wmi.WMI(find_classes=False)
# c = wmi.WMI(computer='192.168.68.223', user='ec1', password='12345678', find_classes=False)  # Win10专业版物理机，连接成功！
# c = wmi.WMI(computer='192.168.48.130', user='lynulyq', password='12345678', find_classes=False)  # VMWare里的Win7企业版，连接成功！
# c = wmi.WMI(computer='192.168.48.131', user='Administrator', password='12345678',find_classes=False)  # VMWare里的WinXP专业版(关闭Windows防火墙后连接成功）

# perf_classes = c.subclasses_of("Win32_PerfRawData")
# pprint(perf_classes)

# for os in c.Win32_OperatingSystem():
#     print(os)

# print(c.Win32_Process.derivation()) # ('CIM_Process', 'CIM_LogicalElement', 'CIM_ManagedSystemElement')

# for extrinsic_event in c.subclasses_of("__ExtrinsicEvent", "[^_].*"):
#   print(extrinsic_event)
#   print("  ", " < ".join(getattr(c, extrinsic_event).derivation()))

# print(c.Win32_OperatingSystem.methods.keys())
#
# os = c.Win32_OperatingSystem
# for method_name in os.methods:
#   method = getattr(os, method_name)
#   print(method)

# print(c.Win32_Process.Create.provenance)  # provenance中文意思“出处”

# WQL查询不是硬盘的磁盘
# wql = "SELECT Caption, Description FROM Win32_LogicalDisk WHERE DriveType <> 3"
# for disk in c.query(wql):
#   print(disk)

# watcher = c.Win32_NTLogEvent.watch_for("creation", 2, Type="error")
# while 1:
#   error = watcher()
#   print("Error in %s log: %s" % (error.Logfile, error.Message))

# 监测进程的创建！
# process_watcher = c.Win32_Process.watch_for("creation")
# while True:
#   new_process = process_watcher()
#   print(new_process.Caption, new_process.ExecutablePath)

# print(c.Win32_PowerManagementEvent.derivation()) # ('__ExtrinsicEvent', '__Event', '__IndicationRelated', '__SystemClass')

# for i in c.subclasses_of("__ExtrinsicEvent"):
#   print(i)

# watcher = c.Win32_PowerManagementEvent.watch_for(EventType=7)
# while True:
#   event = watcher()
#   print("resumed")
#   #
#   # Number of 100-ns intervals since 1st Jan 1601!
#   # TIME_CREATED doesn't seem to be provided on Win2K
#   #
#   if hasattr(event, "TIME_CREATED"):
#     ns100 = int(event.TIME_CREATED)
#     offset = datetime.timedelta(microseconds=ns100 / 10)
#     base = datetime.datetime(1601, 1, 1)
#     print("Resumed at", base  + offset)

# 监测进程变化的事件（更新太频繁了）
# watcher = c.Win32_Process.watch_for("modification")
# while True:
#     event = watcher()
#     print("Modification occurred at", event.timestamp)
#
#     print(event.path())
#     prev = event.previous
#     curr = event
#     for p in prev.properties:
#         pprev = getattr(prev, p)
#         pcurr = getattr(curr, p)
#         if pprev != pcurr:
#             print(p)
#             print("  Previous:", pprev)
#             print("   Current:", pcurr)

# 显示各磁盘的空闲百分比
# for disk in c.Win32_LogicalDisk (DriveType=3):
#     print(disk.Caption, "%0.2f%% free" % (100.0 * int (disk.FreeSpace) / int (disk.Size)))

# 显示各有IP地址的网卡的MAC地址和各IP
# for interface in c.Win32_NetworkAdapterConfiguration (IPEnabled=1):
#     print(interface.Description, interface.MACAddress)
#     for ip_address in interface.IPAddress:
#         print(ip_address)
#     print()

# 显示所有共享文件夹（包含隐藏共享）
# for share in c.Win32_Share ():
#     print(share.Name, share.Path)

# 显示磁盘详细信息
# for physical_disk in c.Win32_DiskDrive():
#     for partition in physical_disk.associators("Win32_DiskDriveToDiskPartition"):
#         for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
#             print(physical_disk.Caption)
#             print(partition.Caption)
#             print(logical_disk.Caption)
#             print()

# 显示类型是AUto但未启动的服务（有的是延迟启动）
# stopped_services = c.Win32_Service (StartMode="Auto", State="Stopped")
# if stopped_services:
#     for s in stopped_services:
#         print(s.Caption, "-->service is not running")
# else:
#     print("No auto services stopped")


# for p in c.Win32_Process(Name="notepad.exe"):
#     for r in p.references():
#         print(r)

# 按照安装时间顺序显示最新安装的“非著名”应用软件（有些应用可能无法显示，只有用Windows Installer安装的才显示，速度很慢，见下面链接）
# https://xkln.net/blog/please-stop-using-win32product-to-find-installed-software-alternatives-inside/
known_name_list = ['microsoft', 'intel', 'oracle', 'python', 'adobe', 'steinberg', 'vmware',
                   'hp inc.', 'ttkn', 'synaptics', 'amd inc.', 'advanced micro devices']
print(len(c.Win32_Product()))
new_app_list = []
for p in c.Win32_Product():
    known_flag = False
    try:
        for name in known_name_list:
            if name in p.Vendor.lower() or name in p.Name.lower():
                known_flag = True
                break
    except Exception as e:
        # print(e)
        # print(p)
        continue
    if not known_flag:
        # print(p.Name, '---', p.Vendor, '--', p.InstallDate)
        new_app_list.append((p.Name, p.Vendor, p.InstallDate))
    # print(p)
pprint(sorted(new_app_list, key=lambda x:x[2], reverse=True))

print('耗时{:.1f}秒'.format(time.time() - start_time))
