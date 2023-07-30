import matplotlib.pyplot as plt

gs_record = []
for i in range(0,120):
    file_path = "./gs_record/sec"+str(i)+".txt"
    file = open(file_path,"r")
    res = []
    for line in file:
        if line.__contains__("deltaT"):
            continue
        else:
            res.append(int(line.strip()))
    file.close()
    gs_record.append(res)

ss_record = []
for i in range(0,120):
    file_path = "./ss_record/sec"+str(i)+".txt"
    file = open(file_path,"r")
    res = []
    for line in file:
        if line.__contains__("deltaT"):
            continue
        else:
            res.append(int(line.strip()))
    file.close()
    ss_record.append(res)

gs_avg_record = []
for deltaT in range(0,30):
    sum = 0
    for start_time in range(0,120):
        sum += gs_record[start_time][deltaT]
    gs_avg_record.append(sum/120)

ss_avg_record = []
for deltaT in range(0,30):
    sum = 0
    for start_time in range(0,120):
        sum += ss_record[start_time][deltaT]
    ss_avg_record.append(sum/120)

X = range(1,31)
gsY = gs_avg_record
ssY = ss_avg_record

gsCY = []
ssCY = []
gs_t1_data = gsY[0]
ss_t1_data = ssY[0]
for i in range(1,30):
    gsCY.append(gs_t1_data-gsY[i])
    ssCY.append(ss_t1_data-ssY[i])
CX = range(2,31)

delta_symbol = '\u0394'
xticks = [0,5,10,15,20,25,30]

plt.figure(figsize=(10, 8))
plt.subplot(2, 1, 1)
#plt.xlabel(delta_symbol+'T(min)',fontproperties=font)
plt.ylabel('Edges Number',fontsize=18)
plt.xticks(fontsize=12)
plt.xlim(0,30)
plt.yticks(fontsize=12)
plt.ylim(300,700)
plt.locator_params(axis='y', nbins=5)
plt.plot(X, gsY, label='GS', linestyle='--', color='#4292c6', marker = 'o', markersize = 5, markevery = 3)
plt.plot(X, ssY, label='SS', linestyle='-', color='#807dba', marker = 'v', markersize = 5, markevery = 3)
plt.legend(fontsize=16,loc=1)

plt.subplot(2, 1, 2)
plt.xlabel(delta_symbol+'T(min)',fontsize=18)
plt.ylabel('Edges Number Change',fontsize=18)
plt.xticks(fontsize=12)
plt.xlim(0,30)
plt.yticks(fontsize=12)
plt.ylim(0,300)
plt.plot(CX, gsCY, label='GS', linestyle='--', color='#4292c6', marker = 'o', markersize = 5, markevery = 3)
plt.plot(CX, ssCY, label='SS', linestyle='-', color='#807dba', marker = 'v', markersize = 5, markevery = 3)
plt.legend(fontsize=16,loc=4)

plt.show()