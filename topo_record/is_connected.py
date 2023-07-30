astra_file = "./topo_record/astra_topo_is_connected.log"
traditional_file = "./topo_record/traditional_topo_is_connected.log"

astraFile = open(astra_file,"r")
traditionalFile = open(traditional_file,"r")

astra_record = []
sum1 = 0
for line in astraFile:
    if line.__contains__("Query"):
        continue
    else:
        data = line.strip()
        if data == "True":
            sum1 += 1
        astra_record.append(data)

traditional_record = []
sum2 = 0
for line in traditionalFile:
    if line.__contains__("Query"):
        continue
    else:
        data = line.strip()
        if data == "True":
            sum2 += 1
        traditional_record.append(data)

print(len(astra_record))
print(sum1)
print(len(traditional_record))
print(sum2)
