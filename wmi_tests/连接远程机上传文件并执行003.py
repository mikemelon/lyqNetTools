from remote_utils.wmi_remote_copy import copy_local_file_to_remote, copy_remote_file_to_local, run_local_command_with_output2
from remote_utils.wmi_remote_exec import execute_cmd_by_wmi
import wmi

if __name__ == '__main__':
    # result = run_local_command_with_output(r'cscript ../tools/wmihacker.vbs  /upload  192.168.48.130  lynulyq  12345678  ../tools/capture_screen1.exe c:\capture_screen1.exe')
    # print(result)
    run_local_command_with_output2(r'cscript ../tools/wmihacker.vbs  /upload  192.168.48.130  lynulyq  12345678  ../tools/capture_screen1.exe c:\capture_screen1.exe')
