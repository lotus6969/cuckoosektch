import pandas as pd
import matplotlib.pyplot as plt
import csv
import matplotlib.ticker as ticker
#from brokenaxes import brokenaxes
#自动出图 内存100kb-1000kb k=100到1000的图
data = pd.read_csv('result.csv')
#keys=["CM","SS","LC","USS","HK","WS","DAS","CS"]
tick_size=9
label_size=10
marker_size=10
keys=["CuckooCounter","CuckooSketch","CuckooSketchPro","heavykeeper","LossyCounting","spacesaving","NI","SAL"]
labels = data.iloc[:, 0:2]
labels={"CC":"CuckooCounter","CS":"CuckooSkeCch","CSP":"CuckooSketchPro","HK":"heavykeeper","LC":"LossyCounting","SS":"spacesaving","NI":"NI","SAL":"SAL"}
default_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",   # 使用颜色编码定义颜色
          "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

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

#funcs = ["CuckooSketchPro", "CuckooSketch", "heavykeeper", "LossyCounting", "spacesaving"]
# topk_range = range(100, 1001, 100)
plt.grid(True, linestyle='--', axis='y')
plt.grid(True, linestyle='--', axis='x')
markers = ['<', '>', '^', 'v', 'x', 'd', 's', '*', 'h', 'H', 'D', 'd', 'P']


#markers={"CM":"<","SS":">","LC":"^","USS":"v","BM":"X","HK":"d","WS":"s","CS":"p"}
for mem in mems:
    plt.figure()
    #plt.subplots_adjust(wspace=0.4,hspace=0.4)
    ax1 = plt.subplot(221)
    topks = list(insertThroughput[mem].keys())
    for index, func in enumerate(funcs):
        throughputs = [insertThroughput[mem][topk][func] for topk in topks]
        ax1.plot(range(len(topks)), throughputs, marker=markers[index],label=func, linestyle='-', alpha=1, linewidth=2, markerfacecolor='none', zorder=105)
        #plt.plot(range(len(topks)), throughputs, marker=markers[index],label=func,markeredgewidth=2, markerfacecolor='none', zorder=105)
    # 设置图表标题和标签
    plt.xticks(range(len(topks)), topks)
    plt.title(f'Insert Throughput ({mem}KB)',fontweight='bold', fontsize=label_size)
    plt.xlabel(u'Memory(KB)', fontweight='bold', fontsize=label_size)
    plt.grid(True, linestyle=':', color='gray')
    plt.ylabel(u'throughput(Mps)', fontweight='bold', fontsize=label_size)   
   
    
   # plt.show()

   # plt.figure()
    ax2= plt.subplot(222)
   # y=[pow(10,i) for i in range(0,10)]
    for index, func in enumerate(funcs):
        aae = [AAE[mem][topk][func] for topk in topks]
        ax2.plot(range(len(topks)), aae, marker=markers[index], label=func, linestyle='-', alpha=1, linewidth=2, markerfacecolor='none', zorder=105)
    # 设置图表标题和标签
    #plt.xticks(range(len(mem)), mem)
    plt.title(f'AAE ({mem}KB)',fontweight='bold', fontsize=label_size)
    plt.xlabel(u'Memory(KB)', fontweight='bold', fontsize=label_size)
    plt.ylabel(u'AAE', fontweight='bold', fontsize=label_size)  
    plt.grid(True, linestyle=':', color='gray')
    #ax2.set_ylim(10**-2, 10**2)
    #ax2.set_yscale('log')
   # plt.yscale('log')#设置纵坐标的缩放
    #plt.ylim(0.05, 5000)
    #plt.legend()
    #plt.show()

    #plt.figure()
    ax3= plt.subplot(223)
    for index, func in enumerate(funcs):
        are = [ARE[mem][topk][func] for topk in topks]
        ax3.plot(range(len(topks)), are, marker=markers[index], label=func, linestyle='-', alpha=1, linewidth=2, markerfacecolor='none', zorder=105)
    # 设置图表标题和标签
    plt.xticks(range(len(topks)), topks)
    plt.title(f'ARE ({mem}KB)',fontweight='bold', fontsize=label_size)
    #plt.xlabel('topk')
    plt.xlabel(u'Memory(KB)', fontweight='bold', fontsize=label_size)
    plt.ylabel(u'ARE', fontweight='bold', fontsize=label_size)    
    plt.grid(True, linestyle=':', color='gray')
    #ax2.set_ylim(10**-2, 10**2)
    #ax2.set_yscale('log')
    #plt.legend()
    #plt.show()

    #plt.figure()
    ax4= plt.subplot(224)
    for index, func in enumerate(funcs):
        precision = [_sum[mem][topk][func] for topk in topks]
        ax4.plot(range(len(topks)), precision, marker=markers[index], linestyle='-', alpha=1, linewidth=2, markerfacecolor='none', zorder=105)
    # 设置图表标题和标签
    plt.xticks(range(len(topks)), topks)
    plt.title(f'precision ({mem}KB)',fontweight='bold', fontsize=label_size)
    plt.xlabel(u'Memory(KB)', fontweight='bold', fontsize=label_size)
    plt.ylabel(u'precision', fontweight='bold', fontsize=label_size)    
    plt.grid(True, linestyle=':', color='gray')
  # plt.legend()
#   plt.ylabel('ARE')
    plt.legend(labels,bbox_to_anchor=(-0.25,2.65),ncol=8, loc='upper center',borderaxespad=0)
    plt.show()
