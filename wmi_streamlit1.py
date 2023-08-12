import psutil
import pandas as pd
import streamlit as st

pids = psutil.pids()

pdata = {}
prop_list = ['name', 'pid', 'username']
for prop in prop_list:
    pdata[prop] = []


for pid in pids:
    try:
        dict1 = psutil.Process(pid).as_dict()
    except Exception as e:
        st.text(e)
        continue
    else:
        for prop in prop_list:
            pdata[prop].append(dict1[prop])


# print(len(dict1.keys()))
# for key,value in dict1.items():
#     print('{}={}'.format(key,value))

df = pd.DataFrame(pdata, columns=prop_list)
st.dataframe(df)
# 'children', 'cmdline', 'connections', 'cpu_affinity', 'cpu_percent', 'cpu_times',
# 'create_time', 'cwd', 'environ','exe', 'io_counters', 'ionice','is_running', 'kill',
# 'memory_full_info', 'memory_info','memory_info_ex','memory_maps', 'memory_percent',
# 'name', 'nice', 'num_ctx_switches','num_handles', 'num_threads','oneshot', 'open_files',
# 'parent', 'parents', 'pid', 'ppid', 'resume', 'send_signal', 'status', 'suspend',
# 'terminate', 'threads', 'username', 'wait'
