import wmi

wmi_obj = wmi.WMI()

plist = wmi_obj.Win32_Process(Caption='Notepad.exe')
pid_list = [p.ProcessId for p in plist]
print(pid_list)