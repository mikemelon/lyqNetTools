# 为了申报软件著作权，需要将所有本地的代码进行遍历和打印
import os

my_top_dir = r'D:\PycharmProjects\lyqNetTools'
file_cnt_nums = 0
file_line_cnts = 0

with open('all_codes_result.txt', 'w', encoding='utf-8') as wf:

    for root, dirs, files in os.walk(my_top_dir):
        # print(root, dirs, files)
        for file in files:

            if (not root.startswith(r'D:\PycharmProjects\lyqNetTools\venv') and
                    not root.startswith(r'D:\PycharmProjects\lyqNetTools\little_tests') and
                    not root.startswith(r'D:\PycharmProjects\lyqNetTools\ssl_and_cert') and
                    not root.startswith(r'D:\PycharmProjects\lyqNetTools\wmi_tests') and
                    not root.startswith(r'D:\PycharmProjects\lyqNetTools\perfmon_data_analysis') and
                    (file.endswith('.py') or file.endswith('.ui') or file.endswith('.ini')) ):
                print(file)
                file_cnt_nums += 1
                with open(root + '\\' + file,'r',encoding='utf-8' ) as f:
                    # do something with f
                    lines = f.readlines()
                    file_line_cnts += len(lines)
                wf.write('--------------------'+file+'--------------------\n')
                wf.writelines(lines)
                wf.write('\n--------------------------------------------------------\n\n')

print('共有{}个文件，共有{}行'.format(file_cnt_nums, file_line_cnts))
