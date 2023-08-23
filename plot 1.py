import pandas as pd
import matplotlib.pyplot as plt
import csv

data = pd.read_csv('result.csv')

insertThroughput = {}
AAE = {}
ARE = {}
_sum = {}

with open('result.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(reader)
    for row in reader:
        mem = int(row[0])
        func = str(row[1])
        topk = int(row[2])
        aae = float(row[3])
        are = float(row[4])
        mismatch = int(row[5].split('/')[1]) - int(row[5].split('/')[0])
        throughput = float(row[6])

        if mem not in insertThroughput:
            insertThroughput[mem] = {}
            AAE[mem] = {}
            ARE[mem] = {}
            _sum[mem] = {}
    
        if topk not in insertThroughput[mem]:
            insertThroughput[mem][topk] = {}
            AAE[mem][topk] = {}
            ARE[mem][topk] = {}
            _sum[mem][topk] = {}
    
        if func not in insertThroughput[mem][topk]:
            insertThroughput[mem][topk][func] = []
            AAE[mem][topk][func] = []
            ARE[mem][topk][func] = []
            _sum[mem][topk][func] = []

        # print(mem, topk, func, throughput)
        
        insertThroughput[mem][topk][func].append(throughput)
        AAE[mem][topk][func].append(aae)
        ARE[mem][topk][func].append(are)
        _sum[mem][topk][func].append(mismatch)

mems = list(insertThroughput.keys())
funcs = list(insertThroughput[mems[0]][100].keys())
# topk_range = range(100, 1001, 100)

markers = ['o', 'v', '^', '<', '>', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X']
for mem in mems:
    plt.figure()
    topks = list(insertThroughput[mem].keys())
    for index, func in enumerate(funcs):
        throughputs = [insertThroughput[mem][topk][func] for topk in topks]
        plt.plot(range(len(topks)), throughputs, marker=markers[index], label=func)
    # 设置图表标题和标签
    plt.xticks(range(len(topks)), topks)
    plt.title(f'Insert Throughput (mem={mem})')
    plt.xlabel('topk')
    plt.grid(True, linestyle=':', color='gray')
    plt.ylabel('throughput')
    plt.legend()
    plt.show()

    plt.figure()
    for index, func in enumerate(funcs):
        aae = [AAE[mem][topk][func] for topk in topks]
        plt.plot(range(len(topks)), aae, marker=markers[index], label=func)
    # 设置图表标题和标签
    plt.xticks(range(len(topks)), topks)
    plt.title(f'aae (mem={mem})')
    plt.xlabel('topk')
    plt.ylabel('AAE')
    plt.grid(True, linestyle=':', color='gray')
    plt.legend()
    plt.show()

    plt.figure()
    for index, func in enumerate(funcs):
        are = [ARE[mem][topk][func] for topk in topks]
        plt.plot(range(len(topks)), are, marker=markers[index], label=func)
    # 设置图表标题和标签
    plt.xticks(range(len(topks)), topks)
    plt.title(f'are (mem={mem})')
    plt.xlabel('topk')
    plt.ylabel('ARE')
    plt.grid(True, linestyle=':', color='gray')
    plt.legend()
    plt.show()

    plt.figure()
    for index, func in enumerate(funcs):
        precision = [_sum[mem][topk][func] for topk in topks]
        plt.plot(range(len(topks)), precision, marker=markers[index], label=func)
    # 设置图表标题和标签
    plt.xticks(range(len(topks)), topks)
    plt.title(f'precision (mem={mem})')
    plt.xlabel('topk')
    plt.ylabel('precision')
    plt.legend()
    plt.ylabel('ARE')
    plt.grid(True, linestyle=':', color='gray')
    plt.show()
