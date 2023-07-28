import pandas as pd
import matplotlib.pyplot as plt

# 读取数据文件
data = pd.read_csv('0-recvPkt.log', sep='\s+', header=None, names=['time', 'latency', 'int1', 'int2'])

# 创建图表
plt.figure(figsize=(10,6))

# 绘制折线图
plt.plot(data['time'], data['latency'], marker='o')

# 设置图表标题和标签
plt.title('Latency over Time')
plt.xlabel('Time')
plt.ylabel('Latency')

# 显示图表
plt.show()
