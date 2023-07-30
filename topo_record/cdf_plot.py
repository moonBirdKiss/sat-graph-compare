import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import statsmodels.api as sm 
import numpy as np

font = FontProperties(fname=r"./font/times.ttf", size=20)
legendfont = FontProperties(fname=r"./font/times.ttf", size=18)

astra_file = "./topo_record/astra_topo_change.log"
traditional_file = "./topo_record/traditional_topo_change.log"

astraFile = open(astra_file,"r")
traditionalFile = open(traditional_file,"r")

astra_record = []
for line in astraFile:
    if line.__contains__("Query"):
        continue
    else:
        data = int(line.strip())
        astra_record.append(data)

traditional_record = []
for line in traditionalFile:
    if line.__contains__("Query"):
        continue
    else:
        data = int(line.strip())
        traditional_record.append(data)

astra_record.sort()
traditional_record.sort()

minx = min(min(astra_record),min(traditional_record))
maxx = max(max(astra_record),max(traditional_record))

X = np.linspace(minx,maxx,100)

astra_Y = astra_record
traditional_Y = traditional_record

astra_Y_ecdf = sm.distributions.ECDF(astra_Y)
astra_Y = astra_Y_ecdf(X)

traditional_Y_ecdf = sm.distributions.ECDF(traditional_Y)
traditional_Y = traditional_Y_ecdf(X)

plt.figure(figsize=(6,5))
plt.xlabel('Topology Change',fontproperties=font)
plt.ylabel('CDF',fontproperties=font)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.plot(X, traditional_Y, label='traditional', linestyle='--', color='#4292c6', marker = 'o', markersize = 8, markevery = 10, linewidth=2)
plt.plot(X, astra_Y, label='astra', linestyle='-', color='#807dba', marker = 'v', markersize = 8, markevery = 10, linewidth=2)
plt.legend(prop=legendfont,loc=4)

plt.show()