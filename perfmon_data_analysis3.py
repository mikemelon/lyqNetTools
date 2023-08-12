import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.spatial.distance as dist
from datetime import datetime

def time_delay_embedding(ts, delay):
    data = np.array(ts)
    x = data[:-delay]
    y = data[delay:]
    return x, y


def RP(ts, threshold=None):
    D = dist.squareform(dist.pdist(ts.reshape(-1, 1)))  # 距离矩阵（默认欧氏距离）
    mean_dist = np.sum(D)/(len(ts)*len(ts)-len(ts))  # 距离均值（不考虑对角线）
    if threshold is None:
        threshold = 0.1*mean_dist  # 计算RP图的阈值
    print('threshold=', threshold)
    R = (D > threshold).astype('int8')  # 生成RP图方阵
    return R


perf_file_path = r'C:\PerfLogs\Admin\新的数据收集器集2'
perf_data_file = os.path.join(perf_file_path, '系统监视器日志.csv')

df = pd.read_csv(perf_data_file)  # DataFrame
df.rename(columns={df.columns[0]: 'time', df.columns[1]: 'processor'}, inplace=True)
df['processor'].replace(r'\s+', np.nan, regex=True, inplace=True)  # 替换空值为np.nan
df['processor'] = df['processor'].astype(float)  # 修改数据类型，str --> flot
df.dropna(inplace=True)  # 删除空值

df['time']= pd.to_datetime(df['time'], format='%m/%d/%Y %H:%M:%S.%f')
ts = pd.Series(np.array(df['processor']), index=df['time'])
ts2 = ts.resample('10S').mean()

x2, y2 = time_delay_embedding(ts2, 1)
# print(len(x), len(y))

fig = plt.figure(figsize=(30, 10))
ax1 = fig.add_subplot(131)
ax1.plot(ts2)

ax2 = fig.add_subplot(132)
ax2.imshow(RP(np.array(ts)), cmap='gray', origin='lower')

# ax3 = fig.add_subplot(133)
# x_step2, y_step2 = [], []
#
# for n in range(len(x2)):
#     x_step2.append(x2[n])
#     y_step2.append(y2[n])
#     ax3.plot(x_step2, y_step2)
#     plt.pause(.1)

plt.show()