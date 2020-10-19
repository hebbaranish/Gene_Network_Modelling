import numpy as np
import matplotlib.pyplot as plt
from math import pow
import os
from scipy.stats import norm, zscore
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
from scipy.spatial.distance import jensenshannon
from initialise.initialise import initialise, set_file_reqs
from initialise.parser import parse_topo
#from scipy.stats import kde
# from scipy import stats

classify = open("classify.txt", 'w')
plot_plotterdata = 1

#give input as new solution file created by racipe

data=np.loadtxt("RACIPE/OCT4_solution.dat")[:,2:]

#give column range of genes you want to classify, 0 indexed
# print(data)
# exit(0)
#NOTE ANISH MODIFICATION: if you have 4 genes, and you want the last three, set left to 1 and right to 3 yeah?
left=1
right=4
length=right-left+1

# datacol=[data[:,0]]*(length)
# for u in range(left,right+1):
#     datacol[u-left]=data[:,u]
datacol = [data[:,u] for u in range(left,right + 1)]
print("dataloaded")
# zscoredx=[datacol[0]]*(length)
# for u in range(0,length):
#     zscoredx[u]=stats.zscore(datacol[u])

zscoredx = [zscore(datacol[u]) for u in range(0,length)]
print("zscore done")
#
# kdefitx=[sm.nonparametric.KDEUnivariate(zscoredx[0])]*(length)
# for u in range(0,length):
#     kdefitx[u]=sm.nonparametric.KDEUnivariate(zscoredx[u])
#     kdefitx[u].fit(bw=0.1)
kdefitx = [sm.nonparametric.KDEUnivariate(zscoredx[u]) for u in range(0,length)]
for u in range(0,length):
    kdefitx[u].fit(bw = 0.1)
print("kdefit done")

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


racipeclassify=np.zeros(2**length)


for i in range(len(zscoredx[0])):
    zarr=[0]*length
    power=int(2**(length-1) +1e-9)
    index=int(0)
    for u in range(length):
        zarr[u]=int(zscoredx[u][i]>pivot[u])
        index+=power*zarr[u]
        power=power/2
    racipeclassify[int(index)]+=1

yaxis=[0]*(2**length)
xaxislabel=[str("")]*(2**length)



for u in range(2**length):
    q=u
    k=0
    while(k<length):
        xaxislabel[u]+=str(int(q%2) )
        q=q/2
        k+=1
    xaxislabel[u] = "".join(reversed(xaxislabel[u]))
    yaxis[u]=racipeclassify[u]/len(zscoredx[0])

racipe_probfile = open("racipe_prob.txt", 'w')
for i in range(len(yaxis)):
    racipe_probfile.write("{} {:.6f}\n".format(xaxislabel[i], yaxis[i]))

final_index = []
for i in range(len(yaxis)):
    if yaxis[i] >= 0.01:
        final_index.append(i)
# print(np.array([yaxis[i] for i in final_index]), np.array([yaxis[i] for i in final_index]).argsort())
final_yaxis = [yaxis[i] for i in final_index]
final_xaxislabel = [xaxislabel[i] for i in final_index]
argarr = np.argsort(np.array(final_yaxis))[::-1]
# print(argarr)
final_yaxis = [final_yaxis[i] for i in argarr]
final_xaxislabel = [final_xaxislabel[i] for i in argarr]
final_xaxis=np.array([i for i in range(1,len(final_yaxis)+1)])
plt.figure(figsize=(20,12))
if(not(plot_plotterdata) ):
    plt.bar(final_xaxis,final_yaxis, width = 0.3, color = 'r')
    plt.xticks(final_xaxis, final_xaxislabel, rotation = 'vertical')

# print(argarr)
# print(yaxis)




if plot_plotterdata:
    dataplotter = open("output/{}_ssprob_all.txt".format("OCT4_async_unweigh"),'r').read().split("\n")[1:-1]
    x_labels = []
    y_data = []
    # print(dataplotter)
    for temp in dataplotter:
        # print(i)
        i = temp.split(" ")
        x_labels.append(i[0])
        y_data.append(float(i[1]))
    final_yaxislist=list(final_yaxis)
    list_labels=[]
    dict_yaxis={}
    for i in range(len(final_xaxis)):
        list_labels.append(final_xaxislabel[i])
        dict_yaxis.update( {final_xaxislabel[i] : i })
    cnt=0
    for i in range(len(y_data)):
        if (y_data[i] >= 0.01 and (str(x_labels[i]) not in final_xaxislabel) ):
            list_labels.append(x_labels[i])
            final_yaxislist.append(yaxis[ int(x_labels[i],2) ])
            dict_yaxis.update( {x_labels[i] : len(final_xaxis)+cnt} )
            cnt+=1

    final_ydata = np.zeros(len(list_labels))
    for i in range(len(y_data)):
        if(x_labels[i] in dict_yaxis):
            index=dict_yaxis[x_labels[i]]
            final_ydata[index]=y_data[i]

    weight = 0.35
    final_xaxis=[i for i in range(len(list_labels)) ]
    plt.bar(final_xaxis,np.array(final_yaxislist) , width = 0.3, color = 'r')
    plt.bar(np.array(final_xaxis)+weight, final_ydata, width = 0.3, color = 'b')
    plt.xticks(final_xaxis,list_labels, rotation = 'vertical')
    plt.title( "JSD = {:.6f}".format(jensenshannon(final_ydata,np.array(final_yaxislist) )))

    # print(final_ydata)
# print(xaxislabel)



plt.savefig("racipeVbool.png")



for u in range(length):
    print(pivot[u])
    classify.write(str(pivot[u])+" ")
classify.write("\n")
classify.close()

#final calculation for %deviation and sigma activation*state
filename = "GRHL2"


params = initialise("init.txt", 14)
params['file_reqs'] = set_file_reqs(params)
link_matrix, id_to_node = parse_topo(params, filename, 0, 0) #seed doesnt matter for unweighted

# vars you need to take care of: list_labels, final_ydata, final_yaxislist
# print(list_labels, final_ydata, final_yaxislist)

#get list of all stable states with state as 0 in bool thing.
final_indices = []
for i in range(len(final_ydata)):
    if final_ydata[i] != 0:
        final_indices.append(i)
list_labels_modified = [list_labels[i] for i in final_indices]
final_ydata = np.array([final_ydata[i] for i in final_indices])
final_yaxislist = np.array([final_yaxislist[i] for i in final_indices])

percent_difference = np.zeros(len(final_ydata))
for i in range(len(final_ydata)):
    percent_difference[i] = np.absolute(final_ydata[i] - final_yaxislist[i])/final_ydata[i] * 100
print(final_ydata, final_yaxislist, percent_difference)

file_count = -1
for i in range(len(params['input_filenames'])):
    if filename == params['input_filenames'][i]:
        file_count = i
        break
if file_count == -1:
    raise ValueError("Filename {} not found in init.txt".format(filename))

sigma_activation = []

for i in list_labels:
    constnodes = params['constant_node_count'][file_count]
    curstate = [1] * constnodes
    for j in range(constnodes, len(id_to_node)):
        curstate.append(1 if int(i[j-constnodes]) != 0 else -1)
    print(np.matmul(curstate, link_matrix))
    sigma_activation.append(np.dot(curstate, np.matmul(curstate, link_matrix)))

print(sigma_activation)
activationfile = open("activation.txt", 'a')
for i in range(len(sigma_activation)):
    activationfile.write("{} {}\n".format(list_labels[i], sigma_activation[i]))
activationfile.write("Plotted: ")
for i in final_indices:
    activationfile.write("{} ".format(i))
activationfile.write("\n")
activationfile.close()

sigma_activation = [sigma_activation[i] for i in final_indices]

activationperc = open("percentvact.txt", 'a')
for i in range(len(sigma_activation)):
    activationperc.write("{:.6f} {}\n".format(percent_difference[i], sigma_activation[i]))
activationperc.close()
