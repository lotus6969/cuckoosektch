import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
#import random
#data = pd.read_csv('topk1000.csv')
data = pd.read_csv('result.csv')
#固定k=1000，内存从100-1000 的性能
# x = data.iloc[:,0:1]
# print(set(x))
keys=["CM","BM","AS","DHS","PCU","EL","NI","SAL"]
labels={"CM":"CM","AS":"AS","DHS":"DHS","PCU":"PCU","BM":"BM","EL":"EL","NI":"NI","SAL":"SAL"}
colors={"CM":"#30A9DE","AS":"#EFDC05","CU":"#E53A40","PCU":"#a5dff9","Multi":"#ef5285","BM":"#FFB353"}
markers={"CM":"<","AS":">","DHS":"^","PCU":"v","BM":"X","EL":"d","NI":"s","SAL":"p"}
tick_size=9
label_size=10

default_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",   # 使用颜色编码定义颜色
          "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

zipf=0
labels = data.iloc[:, 0:2]
AAE = {}
ARE = {}
throughput = {}
Precsion = {}
plt.subplots_adjust(wspace=0.4,hspace=0.4)
for index, row in data.iterrows():
    key = str(row[1])
    if key not in AAE:
        AAE[key] = []
        ARE[key] = []
        throughput[key] = []
        Precsion[key] = []
    AAE[key].append(row[3])
    ARE[key].append(row[4])
    throughput[key].append(row[6])
    Precsion[key].append(int(row[5].split('/')[1]) - int(row[5].split('/')[0]))

offset = 0.2  # 定义标记之间的偏移量
markers = ['o', 's', '^', 'v', 'D', 'p', '*', 'h', 'x', '+']

plt.figure()
plt.subplots_adjust(wspace=0.4,hspace=0.4)
##子图间距
ax1 = plt.subplot(221)
plt.grid(True, linestyle='--', axis='y')
plt.grid(True, linestyle='--', axis='x')
i = 0
xtick=[]
data={}
data["CuckooCounter"]=[]
data["CuckooSketch"]=[]
data["CuckooSketchPro"]=[]
data["heavykeeper"]=[]
data["LossyCounting"]=[]
data["spacesaving"]=[]
ms=5
#mem = ["10","20","30","40","50","60","70","80","90","100"]
mem = ["100","200","300","400","500","600","700","800","900","1000"]
for i, (key, value) in enumerate(AAE.items()):
    if key in ['CuckooCounter','CuckooSketch','CuckooSketchPro','heavykeeper','LossyCounting','spacesaving']:      
        x = np.arange(len(value)) + i * offset  # 计算当前折线的横坐标点
        ax1.plot(x,value, '-o', label=key, marker=markers[i], markersize=ms, linewidth=2, markerfacecolor='white')
    else:
        continue
plt.title('AAE（100KB）', fontweight='bold', fontsize=label_size)
plt.xticks(range(len(mem)), mem)
plt.ylabel('AAE', fontweight='bold', fontsize=label_size)
plt.grid(True, linestyle=':', color='gray')
plt.legend(bbox_to_anchor=(1,1.2),ncol=10, loc='lower center',borderaxespad=0.5)
plt.xlabel(u'Memory(KB)', fontweight='bold', fontsize=label_size)
ax1.set_ylim(10**-3, 10**3)
ax1.set_yscale('log')
#plt.tight_layout()

i = 0
ax2 = plt.subplot(222)
plt.grid(True, linestyle='--', axis='y')
plt.grid(True, linestyle='--', axis='x')
for i, (key, value) in enumerate(ARE.items()):
    if key in ['CuckooCounter','CuckooSketch','CuckooSketchPro','heavykeeper','LossyCounting','spacesaving']:      
        x = np.arange(len(value)) + i * offset  # 计算当前折线的横坐标点
        ax2.plot(x,value, '-o', label=key, marker=markers[i], markersize=ms, linewidth=2, markerfacecolor='white')
    else:
        continue
plt.title('(ARE（100KB)',fontweight='bold', fontsize=label_size)
plt.tight_layout()
plt.xlabel(u'Memory(KB)', fontweight='bold', fontsize=label_size)
plt.ylabel('ARE', fontweight='bold', fontsize=label_size)
plt.xticks(range(len(mem)), mem)
plt.grid(True, linestyle=':', color='gray')
ax2.set_ylim(10**-5, 10**3)
ax2.set_yscale('log')

ax3 = plt.subplot(223)
plt.grid(True, linestyle='--', axis='y')
plt.grid(True, linestyle='--', axis='x')
i = 0
for i, (key, value) in enumerate(throughput.items()):
    if key in ['CuckooCounter','CuckooSketch','CuckooSketchPro','heavykeeper','LossyCounting','spacesaving']:      
        x = np.arange(len(value)) + i * offset  # 计算当前折线的横坐标点
        ax3.plot(x,value, '-o', label=key, marker=markers[i], markersize=ms, linewidth=2, markerfacecolor='white')
    else:
        continue
plt.ylabel(u'throughput(Mps)', fontweight='bold', fontsize=label_size)   
plt.title(u'Top-k=1000', fontweight='bold', fontsize=label_size)   
plt.xticks(range(len(mem)), mem)
plt.xlabel(u'Memory(KB)', fontweight='bold', fontsize=label_size)
plt.grid(True, linestyle=':', color='gray')

ax4 = plt.subplot(224)
plt.grid(True, linestyle='--', axis='y')
plt.grid(True, linestyle='--', axis='x')
i = 0
for i, (key, value) in enumerate(Precsion.items()):
    if key in ['CuckooCounter','CuckooSketch','CuckooSketchPro','heavykeeper','LossyCounting','spacesaving']:      
        x = np.arange(len(value)) + i * offset  # 计算当前折线的横坐标点
        ax4.plot(x,value, '-o', label=key, marker=markers[i], markersize=ms, linewidth=2,markerfacecolor='white')
    else:
        continue

plt.xticks(range(len(mem)), mem)
plt.ylabel(u'precision', fontweight='bold', fontsize=label_size)    
plt.title(u'Top-k=1000', fontweight='bold', fontsize=label_size)    
plt.xlabel(u'Memory(KB)', fontweight='bold', fontsize=label_size)
plt.grid(True, linestyle=':', color='gray')

plt.show()
