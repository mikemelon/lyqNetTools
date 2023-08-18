from pythonping import ping
from concurrent.futures import ThreadPoolExecutor
import gradio as gr

def my_ping(ip):
    # print('pinging '+ip+' start')
    if 'Reply' in str(ping(ip)):
        return ip, True
    else:
        return ip, False


def find_reachable_ip_list(ip_prefix):
    executor = ThreadPoolExecutor(max_workers=100)
    result_list = []
    for n in range(1, 255): # 200改成255，有些进程始终不退出，不知何原因。
        result = executor.submit(my_ping, ip_prefix+str(n))
        result_list.append(result)

    reachable_ip_list = []
    for r in result_list:
        if r.result()[1]:
            reachable_ip_list.append(r.result()[0])

    return '\n'.join(reachable_ip_list)


if __name__ == '__main__':
    with gr.Blocks() as demo:
        gr.Markdown('## IP可达性测试（基于Ping命令）')
        input_ip_prefix = gr.Textbox(label='IP前缀', value='192.168.68.')
        btn = gr.Button('开始搜索')
        output_ip_list = gr.Textbox(label='该范围的可达IP', lines=3)
        btn.click(fn=find_reachable_ip_list, inputs=input_ip_prefix, outputs=output_ip_list)

    demo.launch()

