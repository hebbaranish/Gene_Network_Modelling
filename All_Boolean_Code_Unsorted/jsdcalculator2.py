import numpy as np
from scipy.spatial.distance import jensenshannon
from math import pow
import os
from scipy.stats import norm, zscore
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm

# NECESSARY INPUTS
network='GRHL2'
dict={
  "GRHL2": 7,
  "GRHL2wa": 8,
  "OVOL2": 9,
  "OVOLsi": 8,
  "NRF2": 16,
  "OCT4": 10,
  "GRHL2f": 7
}
dict1={
  "GRHL2": 4,
  "GRHL2wa": 4,
  "OVOL2": 4,
  "OVOLsi": 4,
  "NRF2": 8,
  "OCT4": 5,
  "GRHL2f": 7
}
dict2={
  "GRHL2": 1,
  "GRHL2wa": 1,
  "OVOL2": 1,
  "OVOLsi": 1,
  "NRF2": 2,
  "OCT4": 1,
  "GRHL2f": 1
}


num_links = dict[network]
num_nodes = dict1[network]
num_const = dict2[network]


boolean_dir = "Output"

# NECESSARY INPUTS ENDS HERE


boolean_jsd = open("{}_boolean_jsd.txt".format(network), "w")


boolean_jsd.write("cur_topo ")
for i in range(num_links - 1):
    boolean_jsd.write("missing{} ".format(i + 1))
boolean_jsd.write("missing{}\n".format(num_links))

def boolean_probability_counter(boolean_dir, filename, num_nodes, num_const,run_num):
    ssfile = open("{}/{}_async_unweigh_ss_run{}.txt".format(boolean_dir, filename,run_num), "r")
    ssfile = ssfile.read().split("\n")[1:]

    probability = {}

    for i in ssfile:
        temp = i.split(" ")[1 + num_const:]
        bin_value = 0
        for j in range(len(temp)):
            temp[j] = 1 if temp[j] == '1' else 0
            bin_value += (2 ** (len(temp) - j - 1)) * int(temp[j])
        # print(bin_value)
        try:
            probability[bin_value] += 1
        except:
            probability[bin_value] = 1

        # exit(0)
    for i in range(0, 2 ** (num_nodes - num_const)):
        try:
            probability[i]
        except:
            # print("meow")
            probability[i] = 0
    # print(probability)
    return probability
    # exit(0)

def racipe_probability_counter(racipe_dir, filename, num_nodes, num_const):
    # mow = 1
    # mew = 1
    # #give column range of genes you want to classify, 0 indexed
    # #NOTE ANISH MODIFICATION: if you have 4 genes, and you want the last three, set left to 1 and right to 3 yeah?
    left=1
    right=3
    length=right-left+1
    plot_plotterdata = 1
    #
    # filename = "{}{}".format(mow+1, mew+1)
    # print(filename)
    classify = open("classify.txt", 'a')


    #give input as new solution file created by racipe

    # data=np.loadtxt("RACIPE/{}_solution.dat".format(filename))[:,2:]
    data=np.loadtxt("{}/{}_solution.dat".format(racipe_dir, filename))[:,2:]

    # datacol=[data[:,0]]*(length)
    # for u in range(left,right+1):
    #     datacol[u-left]=data[:,u]
    datacol = [data[:,u] for u in range(left,right + 1)]
    # print("dataloaded")
    # zscoredx=[datacol[0]]*(length)
    # for u in range(0,length):
    #     zscoredx[u]=stats.zscore(datacol[u])

    zscoredx = [zscore(datacol[u]) for u in range(0,length)]
    # print("zscore done")
    #
    # kdefitx=[sm.nonparametric.KDEUnivariate(zscoredx[0])]*(length)
    # for u in range(0,length):
    #     kdefitx[u]=sm.nonparametric.KDEUnivariate(zscoredx[u])
    #     kdefitx[u].fit(bw=0.1)
    kdefitx = [sm.nonparametric.KDEUnivariate(zscoredx[u]) for u in range(0,length)]
    for u in range(0,length):
        kdefitx[u].fit(bw = 0.1)
    # print("kdefit done")

    pivot=[0]*length
    pivotpos=[0]*length
    n=len(kdefitx[0].support)
    for u in range(length):
        arr=kdefitx[u].support
        arrdensity=kdefitx[u].density
        max1=-100000000000
        max2=-100000000000
        max3=-100000000000
        max1pos=0
        max2pos=0
        max3pos=0
        f=0
        for j in range(n):
            if(arr[j]<=0):
                if(arrdensity[j]>max1):
                    max1=arrdensity[j]
                    max1pos=j
            else:
                if(arrdensity[j]>max2):
                    max2=arrdensity[j]
                    max2pos=j
        min1=1000000000
        min1pos=0
        for j in range(max1pos,max2pos+1):
             if(arrdensity[j]<min1):
                min1=arrdensity[j]
                min1pos=j

        if(min1pos - max1pos<=10 or max2pos-min1pos <=10):
            f=1
            max3=max(max1,max2)
            finalpivotdensity=max3
            if(max3-max1<1e-10):
                max3pos=max1pos
            else:
                max3pos=max2pos
            finalpivotpos=max3pos
        else:
            f=2
        count=0
        minarr=[0]*100
        if(f==0):
            count=0
            minarr=[0]*100
        elif(f==2):
            finalpivotdensity=min1
            finalpivotpos=min1pos
        else:
            for j in range(max1pos+20,max2pos-19):
                f=0
                left1=max(j-100,max1pos)
                right1=min(j+100,max2pos)
                help1=j
                for q in range(left1,right1+1):
                      if(arrdensity[j]>arrdensity[q]):
                        f=1
                        help1=0
                        break
                if(f==0):
                    minarr[count]=help1
                    count=count+1
            if(count>1):
                max3=-10000000000
                max3pos=0
                for j in range(minarr[0],minarr[count-1]):
                    if(arrdensity[j]>max3):
                        max3=arrdensity[j]
                        max3pos=j
            finalpivotdensity=max3
            finalpivotpos=max3pos
        pivotpos[u]=finalpivotpos
        pivot[u]=arr[finalpivotpos]
    # print("big boi pivot part done")
    racipe_datapoint_dict = {}

    # racipeclassify=np.zeros(2**length)


    for i in range(len(zscoredx[0])):
        zarr=[0]*length
        power=int(2**(length-1) +1e-9)
        index=int(0)
        for u in range(length):
            zarr[u]=int(zscoredx[u][i]>0) # pivot[u]
            index+=power*zarr[u]
            power=power/2
        # racipeclassify[int(index)]+=1
        try:
            racipe_datapoint_dict[int(index)] += 1
        except:
            racipe_datapoint_dict[int(index)] = 1
    # print("dict loaded")
    for i in range(0, 2 ** (num_nodes - num_const)):
        try:
            racipe_datapoint_dict[i]
        except:
            # print("meow")
            racipe_datapoint_dict[i] = 0
    return racipe_datapoint_dict





for i in range(dict[network]):
    for j in range(i+1, dict[network]):
        for run_num in range(1,4):
            print("processing {}{}".format(i+1, j+1))
            # BOOLEAN PART
            boolean_jsd.write("{}{} ".format(i+1, j+1))
            dict_list = []
            for k in range(0,dict[network]+1):
                list_k = []
        
                dict_k = boolean_probability_counter(boolean_dir,"{}{}_{}".format(i+1, j+1, k), num_nodes, num_const,run_num)
                for l in range(0, 2 ** (num_nodes - num_const)):
                    list_k.append(dict_k[l])
                dict_list.append(list_k)
            for k in range(1,dict[network]):
                val = jensenshannon(dict_list[0], dict_list[k], 2)
                boolean_jsd.write("{:.6f} ".format(val))

            val = jensenshannon(dict_list[0], dict_list[dict[network]], 2)
            boolean_jsd.write("{:.6f}\n".format(val))





boolean_jsd.close()
