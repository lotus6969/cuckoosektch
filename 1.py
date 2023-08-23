from cProfile import label
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.ticker as ticker
#from brokenaxes import brokenaxes

keys=["CM","BM","AS","DHS","PCU","EL","NI","SAL"]


labels={"CM":"CM","AS":"AS","DHS":"DHS","PCU":"PCU","BM":"BM","EL":"EL","NI":"NI","SAL":"SAL"}

colors={"CM":"#30A9DE","AS":"#EFDC05","CU":"#E53A40","PCU":"#a5dff9","Multi":"#ef5285","BM":"#FFB353"}

markers={"CM":"<","AS":">","DHS":"^","PCU":"v","BM":"X","EL":"d","NI":"s","SAL":"p"}
tick_size=19
label_size=24
marker_size={"CM":"10","AS":"10","DHS":"10","PCU":"10","BM":"11","EL":"10","NI":"8","SAL":"10"}
legend_args={"bbox_to_anchor":(0.48,1),"loc":"lower center","ncol":2,"handlelength":2,"prop":{"size":23,"weight":"bold"},"frameon":False,"columnspacing":0.5,"handletextpad":0.3,"borderpad":0}
legend_args_tmp={"bbox_to_anchor":(0.48,1),"loc":"lower center","ncol":3,"handlelength":1.3,"prop":{"size":23,"weight":"bold"},"frameon":False,"columnspacing":0.4,"handletextpad":0.2,"borderpad":0}
savefig_args={"bbox_inches":"tight","pad_inches":0}


default_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",   # 使用颜色编码定义颜色
          "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

zipf=0

def paint_AAE():
    #data={}
    xtick=[]
    data={}
    data["CM"]=[]
    data["AS"]=[]
    data["DHS"]=[]
    data["PCU"]=[]
    data["BM"]=[]
    data["EL"]=[]
    data["NI"]=[]
    data["SAL"]=[]
    cnt=-1
    with open("hh-aae-vs-memory-imc.txt","r") as file_in:
        while True:
            memory=file_in.readline()[:]
            if memory=="":
                break
            
            #ARE=float(file_in.readline()[:])
            Mem, CM_itp, AS_itp, DHS_itp, PCU_itp, BM_itp, EL_itp, NI_itp, SAL_itp = map(float,memory.split())

            xtick.append(Mem)
            data["CM"].append(CM_itp)
            data["AS"].append(AS_itp)
            data["DHS"].append(DHS_itp)
            data["PCU"].append(PCU_itp)
            data["BM"].append(BM_itp)
            data["EL"].append(EL_itp)
            data["NI"].append(NI_itp)
            data["SAL"].append(SAL_itp)
            
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.rc('font', family='Arial')

    plt.figure(figsize=(6, 4.5))
    #plt.xscale('log')
    plt.yscale('log')
    plt.tick_params(labelsize=tick_size)

    plt.xlabel(u'Memory (MB)', fontweight='bold', fontsize=label_size)
    plt.ylabel(u'AAE', fontweight='bold', fontsize=label_size)
    plt.xticks([0.1,0.4,0.7,1.0])
    plt.xlim(0.05,1.05)
    plt.ylim(0.05, 5000)

    for key in keys:
        if key=='BM':
            plt.plot(xtick,data[key],label=labels[key], linestyle='-', alpha=1, linewidth=2,marker=markers[key],markersize=marker_size[key],markeredgewidth=2, markerfacecolor='none', zorder=105)
        else:
            plt.plot(xtick,data[key],label=labels[key], linestyle='-', alpha=1, linewidth=2,marker=markers[key],markersize=marker_size[key],markeredgewidth=2, markerfacecolor='none')
    
    #plt.fill_between(xtick, 0, data["BM"], alpha=0.2, color=default_colors[1])
    #plt.legend(loc = 'lower center', ncol=8, handlelength=3, bbox_to_anchor=(0.5,1.1))
    #leg = plt.gca().get_legend() #或leg=ax.get_legend()
    #ltext = leg.get_texts()
    #plt.setp(ltext,fontweight='bold',fontsize = 15)

    plt.grid(True, linestyle='--', axis='y')
    plt.grid(True, linestyle='--', axis='x')
    plt.tight_layout()
    #plt.savefig("insert_zipf.pdf", bbox_inches='tight') #用来截取图标标题
   # plt.savefig("hh-aae-vs-memory-imc.pdf")
    plt.show()
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################

def paint_ARE():
    #data={}
    xtick=[]
    data={}
    data["CM"]=[]
    data["AS"]=[]
    data["DHS"]=[]
    data["PCU"]=[]
    data["BM"]=[]
    data["EL"]=[]
    data["NI"]=[]
    data["SAL"]=[]
    cnt=-1
    with open("hh-are-vs-memory-imc.txt","r") as file_in:
        while True:
            memory=file_in.readline()[:]
            if memory=="":
                break
            
            #ARE=float(file_in.readline()[:])
            Mem, CM_itp, AS_itp, DHS_itp, PCU_itp, BM_itp, EL_itp, NI_itp, SAL_itp = map(float,memory.split())

            xtick.append(Mem)
            data["CM"].append(CM_itp)
            data["AS"].append(AS_itp)
            data["DHS"].append(DHS_itp)
            data["PCU"].append(PCU_itp)
            data["BM"].append(BM_itp)
            data["EL"].append(EL_itp)
            data["NI"].append(NI_itp)
            data["SAL"].append(SAL_itp)
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.rc('font', family='Arial')

    plt.figure(figsize=(6, 4.5))
    
    #plt.xscale('log')
    plt.yscale('log')
    plt.tick_params(labelsize=tick_size)

    plt.xlabel(u'Memory (MB)', fontweight='bold', fontsize=label_size)
    plt.ylabel(u'ARE', fontweight='bold', fontsize=label_size)
    plt.xticks([0.1,0.4,0.7,1.0])
    plt.xlim(0.05,1.05)
    plt.ylim(0.0002, 5)

    for key in keys:
        if key=='BM':
            plt.plot(xtick,data[key],label=labels[key], linestyle='-', alpha=1, linewidth=2,marker=markers[key],markersize=marker_size[key],markeredgewidth=2, markerfacecolor='none', zorder=105)
        else:
            plt.plot(xtick,data[key],label=labels[key], linestyle='-', alpha=1, linewidth=2,marker=markers[key],markersize=marker_size[key],markeredgewidth=2, markerfacecolor='none')
    
    #plt.fill_between(xtick, 0, data["BM"], alpha=0.2, color=default_colors[1])
    #plt.legend(loc = 'lower center', ncol=8, handlelength=3, bbox_to_anchor=(0.5,1.1))
    #leg = plt.gca().get_legend() #或leg=ax.get_legend()
    #ltext = leg.get_texts()
    #plt.setp(ltext,fontweight='bold',fontsize = 15)
    plt.grid(True, linestyle='--', axis='y')
    plt.grid(True, linestyle='--', axis='x')
    plt.tight_layout()
    #plt.savefig("insert_zipf.pdf", bbox_inches='tight') #用来截取图标标题
  #  plt.savefig("hh-are-vs-memory-imc.pdf")
    plt.show()
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################

def paint_F1():
    #data={}
    xtick=[]
    data={}
    data["CM"]=[]
    data["AS"]=[]
    data["DHS"]=[]
    data["PCU"]=[]
    data["BM"]=[]
    data["EL"]=[]
    data["NI"]=[]
    data["SAL"]=[]
    cnt=-1
    with open("hh-f1-vs-memory-imc.txt","r") as file_in:
        while True:
            memory=file_in.readline()[:]
            if memory=="":
                break
            
            #ARE=float(file_in.readline()[:])
            Mem, CM_itp, AS_itp, DHS_itp, PCU_itp, BM_itp, EL_itp, NI_itp, SAL_itp = map(float,memory.split())

            xtick.append(Mem)
            data["CM"].append(CM_itp)
            data["AS"].append(AS_itp)
            data["DHS"].append(DHS_itp)
            data["PCU"].append(PCU_itp)
            data["BM"].append(BM_itp)
            data["EL"].append(EL_itp)
            data["NI"].append(NI_itp)
            data["SAL"].append(SAL_itp)
            
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.rc('font', family='Arial')

    plt.figure(figsize=(6, 4.5))
    #plt.xscale('log')
    #plt.yscale('log')
    plt.tick_params(labelsize=tick_size)
    plt.xlabel(u'Memory (MB)', fontweight='bold', fontsize=label_size)
    plt.ylabel(u'$F_1$ Score', fontweight='bold', fontsize=label_size)


    plt.xticks([0.1,0.4,0.7,1.0])
    plt.xlim(0.05,1.05)
    plt.ylim(0, 1.05)

    for key in keys:
        if key=='BM':
            plt.plot(xtick,data[key],label=labels[key], linestyle='-', alpha=1, linewidth=2,marker=markers[key],markersize=marker_size[key],markeredgewidth=2, markerfacecolor='none', zorder=105)
        else:
            plt.plot(xtick,data[key],label=labels[key], linestyle='-', alpha=1, linewidth=2,marker=markers[key],markersize=marker_size[key],markeredgewidth=2, markerfacecolor='none')
    
    #plt.fill_between(xtick, 0, data["BM"], alpha=0.2, color=default_colors[1])
    #plt.legend(loc = 'lower center', ncol=8, handlelength=3, bbox_to_anchor=(0.5,1.1))
    #leg = plt.gca().get_legend() #或leg=ax.get_legend()
    #ltext = leg.get_texts()
    #plt.setp(ltext,fontweight='bold',fontsize = 15)

    plt.grid(True, linestyle='--', axis='y')
    plt.grid(True, linestyle='--', axis='x')
    plt.tight_layout()
    #plt.savefig("insert_zipf.pdf", bbox_inches='tight') #用来截取图标标题
    #plt.savefig("hh-f1-vs-memory-imc.pdf")
    plt.show()
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
if __name__=="__main__":
#    if (zipf == 1):
#        xtick = [x/100+0.3 for x in xtick]
#    paint_Insert()
#    paint_Query()
   paint_AAE()
   paint_ARE()
   paint_F1()