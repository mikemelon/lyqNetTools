import time
import os


def run_local_command_with_output(cmd_str) -> str:
    """
    本地执行命令，并返回结果字符串
    :param cmd_str: 要执行的命令
    :return: 返回的结果字符串
    """
    p = os.popen(cmd_str, 'r')
    result_lines = p.readlines()
    return '\n'.join(result_lines)


def copy_local_file_to_remote(local_file_path, remote_ip, remote_file_name=None):
    """
    将本地文件复制到远程，要求远程具有C$共享目录（使用执行copy命令到远程UNC路径的方法）。2023-08-02测试通过
    :param local_file_path: 本地文件的完整路径名
    :param remote_ip: 远程IP地址或机器名
    :param remote_file_name: 远程文件名，如果为None（默认）则不改名
    :return: 无（直接打印结果）
    """
    cmd_copy = r'copy {} \\{}\c$\{}'.format(local_file_path, remote_ip,
                                            remote_file_name if remote_file_name else os.path.basename(local_file_path))
    result = run_local_command_with_output(cmd_copy)
    print(cmd_copy+'\t将本地文件复制到远程，执行结果如下:\n', result)


def copy_remote_file_to_local(remote_file_name, remote_ip, local_file_path=None):
    """
    将远程文件复制到本地，要求远程具有C$共享目录（使用执行copy命令到远程UNC路径的方法）,该文件必须在远程机的C:盘根目录。2023-08-02测试通过
    :param remote_file_name: 本地文件的完整路径名
    :param remote_ip: 远程IP地址或机器名
    :param local_file_path: 本地文件名，如果为None（默认）则不改名
    :return:
    """
    cmd_copy = r'copy \\{}\c$\{} {}'.format(remote_ip, remote_file_name,
                                            local_file_path if local_file_path else 'c:\\' + remote_file_name)
    result = run_local_command_with_output(cmd_copy)
    print(cmd_copy+'\t该教师机命令的执行结果如下:\n', result)


if __name__ == '__main__':
    # cmd_copy = r'copy c:\test.txt \\192.168.68.223\c$\wocaocao.txt'
    # p = os.popen(cmd_copy, 'r')
    # lines = p.readlines()
    # print(cmd_copy+'\t该教师机命令的执行结果如下:\n', '\n'.join(lines))

    start_time = time.time()
    copy_local_file_to_remote(r'c:\test.txt', '192.168.68.223')
    # copy_remote_file_to_local('test.txt', '192.168.68.223', r'd:\mytest.txt')
    print('{:.1f} seconds elapsed'.format(time.time()-start_time))
