import wmi
from pprint import pprint
pc = wmi.WMI()
print('WMI可供查询类的数量：{}'.format(len(list(pc.classes))))
# for cls_1 in pc.classes:
#     print(cls_1)

os_info = pc.Win32_OperatingSystem()[0]
processor = pc.Win32_Processor()[0]
gpus = pc.Win32_VideoController()

print('*'*40)
print('操作系统：{}'.format(os_info.Caption))
print('CPU：{}，\n\t 内核：{}，逻辑处理器：{}，L2 Cache：{}M，L3 Cache：{}M'
      .format(processor.Name, processor.NumberOfCores, processor.NumberOfLogicalProcessors,
              float(processor.L2CacheSize)/1024, float(processor.L3CacheSize)/1024))
print('显卡：')
if len(gpus) > 1:
    for gpu in gpus:
        print(gpu.Name)
else:
    print(gpus[0].Name)

# fans = pc.Win32_Fan()
# for fan in fans:
#     print(fan)
# print(fans)

fans = pc.CIM_Fan()
for fan in fans:
    print(fan)
print(fans)

# print('声音设备：')
# sound_devices = pc.Win32_SoundDevice()
# for sound_device in sound_devices:
#     print(sound_device.Name)

# computer_systems = pc.Win32_ComputerSystem()
# for computer_system in computer_systems:
#     print(computer_system)

# print('---------列出所有进程---------')
# for process in pc.Win32_Process():
#     print('进程ID：{}，进程名：{}，进程路径：{}'.format(process.ProcessID, process.Name, process.ExecutablePath))

print('*'*40)

from pyspectator.computer import Computer
computer = Computer()
print('*'*40)
print(computer.os)
print(computer.python_version)
print(computer.uptime)
print(computer.processor.name)
print()
print('*'*40)

import platform
print('*'*40)
print('CPU名：{}'.format(platform.processor()))
print('机器类型：{}'.format(platform.machine()))
print('操作系统：{}'.format(platform.system()))
print('Python版本:{}'.format(platform.python_version()))
print('*'*40)

import os
# print(os.uname())

import sys
from pprint import pprint
print('sys.platform={}'.format(sys.platform))
print('sys.path={}'.format(sys.path))
print(sys.modules.keys())

from netifaces import interfaces, gateways, ifaddresses
print(interfaces())
print(gateways())
# for iface in interfaces():
#     print(ifaddresses(iface))