import wmi
from win32com.client import GetObject
from pprint import pprint
pc = wmi.WMI()
# print('WMI可供查询类的数量：{}'.format(len(list(pc.classes))))
# for cls_1 in pc.classes:
#     print(cls_1)


# os_info = pc.Win32_OperatingSystem()[0]
# processor = pc.Win32_Processor()[0]
# gpus = pc.Win32_VideoController()
#
# print('*'*40)
# print('操作系统：{}, CodeSet：{}, CountryCode: {}, CSName: {}, CreationClassName:{}, CSCreationClassName: {}, SerialNumber:{}, Manufacturer:{}'
#       .format(os_info.Caption, os_info.CodeSet, os_info.CountryCode, os_info.CSName, os_info.CreationClassName,
#               os_info.CSCreationClassName, os_info.SerialNumber, os_info.Manufacturer))
# print('CPU：{}，\n\t 内核：{}，逻辑处理器：{}，L2 Cache：{}M，L3 Cache：{}M'
#       .format(processor.Name, processor.NumberOfCores, processor.NumberOfLogicalProcessors,
#               float(processor.L2CacheSize)/1024, float(processor.L3CacheSize)/1024))
#
# wmi = GetObject('winmgmts:/root/cimv2')

for item in pc.Win32_OperatingSystem():
    print(item)
    # print(type(item.wmi_property()))
    print(len(list(item.properties.keys())))
    print(dir(item))

    for key in list(item.properties.keys()):  # 比直接打印多出7个属性，但值都为None
        # print(dir(item.wmi_property(key)))
        print('{}==={}'.format(key, item.wmi_property(key).value))



