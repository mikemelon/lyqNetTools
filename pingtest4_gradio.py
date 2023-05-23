from pythonping import ping
from multiprocessing import Pool
import gradio as gr


def my_ping(ip):
    # print('pinging '+ip+' start')
    if 'Reply' in str(ping(ip)):
        return ip, True
    else:
        return ip, False


def find_reachable_ip_list(ip_prefix):
    pool = Pool(255)
    result_list = []
    for n in range(1, 255): # 200改成255，有些进程始终不退出，不知何原因。
        result = pool.apply_async(func=my_ping, args=('192.168.68.'+str(n),))
        result_list.append(result)

    pool.close()
    pool.join()

    print('all process over!!!!')

    reachable_ip_list = []
    for r in result_list:
        if r.get()[1]:
            reachable_ip_list.append(r.get()[0])

    return reachable_ip_list


# 多进程方式无法运行，内存溢出报错，原因未知
if __name__ == '__main__':
    demo = gr.Interface(fn=find_reachable_ip_list, inputs=gr.Textbox(label='IP前缀', ), outputs='text')
    demo.launch()
