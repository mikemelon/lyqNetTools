import wmi
import pandas as pd
import streamlit as st
import time


@st.cache_resource
def get_processes():
    pc = wmi.WMI()
    processes = pc.Win32_Process()
    return processes


start_time = time.time()
processes = get_processes()
pdata = {}
prop_list = ['name', 'pid', 'thread_count', 'exepath']
for prop in prop_list:
    pdata[prop] = []


for process in processes:
    pdata['name'].append(process.Name)
    pdata['pid'].append(process.ProcessID)
    pdata['thread_count'].append(process.ThreadCount)
    pdata['exepath'].append(process.ExecutablePath)

df = pd.DataFrame(pdata, columns=prop_list)
st.dataframe(df, width=2800)

print('used {} seconds'.format(time.time()-start_time))

# 'children', 'cmdline', 'connections', 'cpu_affinity', 'cpu_percent', 'cpu_times',
# 'create_time', 'cwd', 'environ','exe', 'io_counters', 'ionice','is_running', 'kill',
# 'memory_full_info', 'memory_info','memory_info_ex','memory_maps', 'memory_percent',
# 'name', 'nice', 'num_ctx_switches','num_handles', 'num_threads','oneshot', 'open_files',
# 'parent', 'parents', 'pid', 'ppid', 'resume', 'send_signal', 'status', 'suspend',
# 'terminate', 'threads', 'username', 'wait'
