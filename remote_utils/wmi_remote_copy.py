import time
import os

# TODO: WMI 远程进程复制文件 :https://www.51c51.com/baike/xinxi/5/536586.html
# TODO: 域渗透-横向移动命令总结 https://blog.csdn.net/m0_60571990/article/details/128154657  提到了certutil, bitsadmin等方法


def run_local_command_without_output(cmd_str):
    """
    本地执行命令，并返回结果字符串
    :param cmd_str: 要执行的命令
    :return: nothing
    """
    p = os.popen(cmd_str, 'r')


def run_local_command_with_output(cmd_str) -> str:
    """
    本地执行命令，并返回结果字符串
    :param cmd_str: 要执行的命令
    :return: 返回的结果字符串
    """
    p = os.popen(cmd_str, 'r')
    result_lines = p.readlines()

    return '\n'.join(result_lines)


# 作用同run_local_command_with_output，但实时打印输出执行结果
def run_local_command_with_output2(cmd_str):
    p = os.popen(cmd_str, 'r')
    while True:
        result_line = p.readline()
        if result_line:
            print(result_line, end='')
        else:
            break


def copy_local_file_to_remote(local_file_path, remote_ip, remote_user, remote_password, remote_file_name=None,
                              with_output=True):
    """
    将本地文件复制到远程，要求远程具有C$共享目录（使用执行copy命令到远程UNC路径的方法）。2023-08-02测试通过
    :param local_file_path: 本地文件的完整路径名
    :param remote_ip: 远程IP地址或机器名
    :param remote_user: 远程用户名（管理员）
    :param remote_password: 远程密码
    :param remote_file_name: 远程文件名，如果为None（默认）则不改名
    :param with_output: 是否输出命令行的返回结果
    :return: 无（直接打印结果）
    """
    cmd_net = r'net use \\{} /del & net use \\{} /user:{} {}'.format(remote_ip, remote_ip, remote_user, remote_password)
    # copy命令不支持强制覆盖，因而改为xcopy /y
    cmd_copy = r'xcopy /y /-i {} \\{}\c$\{}'.format(local_file_path, remote_ip,
                                            remote_file_name if remote_file_name else os.path.basename(local_file_path))
    # print(cmd_copy)
    if with_output:
        result = run_local_command_with_output(cmd_net + ' & ' + cmd_copy)
        print(cmd_copy+'\t将本地文件复制到远程，执行结果如下:\n', result)
    else:
        run_local_command_without_output(cmd_net + ' & ' + cmd_copy)


def copy_remote_file_to_local(remote_file_name, remote_ip, remote_user, remote_password, local_file_path=None):
    """
    将远程文件复制到本地，要求远程具有C$共享目录（使用执行copy命令到远程UNC路径的方法）,该文件必须在远程机的C:盘根目录。2023-08-02测试通过
    :param remote_file_name: 本地文件的完整路径名
    :param remote_ip: 远程IP地址或机器名
    :param remote_user: 远程用户名（管理员）
    :param remote_password: 远程密码
    :param local_file_path: 本地文件名，如果为None（默认）则不改名
    :return:
    """
    cmd_net = r'net use \\{} /del & net use \\{} /user:{} {}'.format(remote_ip, remote_ip, remote_user, remote_password)
    cmd_copy = r'xcopy /y /-i \\{}\c$\{} {}'.format(remote_ip, remote_file_name,
                                            local_file_path if local_file_path else 'c:\\' + remote_file_name)
    result = run_local_command_with_output(cmd_net + ' & ' + cmd_copy)
    print(cmd_copy+'\t将远程文件复制到本地，执行结果如下:\n', result)


if __name__ == '__main__':
    # cmd_copy = r'copy c:\test.txt \\192.168.68.223\c$\wocaocao.txt'
    # p = os.popen(cmd_copy, 'r')
    # lines = p.readlines()
    # print(cmd_copy+'\t该教师机命令的执行结果如下:\n', '\n'.join(lines))

    start_time = time.time()
    copy_local_file_to_remote(r'c:\test.txt', '192.168.68.223')
    # copy_remote_file_to_local('test.txt', '192.168.68.223', r'd:\mytest.txt')
    print('{:.1f} seconds elapsed'.format(time.time()-start_time))
