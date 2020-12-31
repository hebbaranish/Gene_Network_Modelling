import numpy as np
import matplotlib.pyplot as plt
from math import pow
import os
from scipy.stats import norm, zscore
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
from scipy.spatial.distance import jensenshannon
from matplotlib import rcParams
#from scipy.stats import kde
# from scipy import stats

from matplotlib import rcParams
version='cont'
####
import initialise.initialise as initialise
import initialise.parser as parser
in_file = 'init.txt'
max_initlines = 14
begin=1
process_count=1
params = initialise.initialise(in_file, max_initlines)
params['file_reqs'] = initialise.set_file_reqs(params)
id_to_node=[]

for i in params['file_reqs']:
        for j in params['input_filenames']:
                random_seed = int(begin) + process_count
                weighted_tick = 1 if "_weigh" in i else 0
                async_tick = 1 if "_async" in i else 0
                link_matrix, id_to_node = parser.parse_topo(params,j,weighted_tick, random_seed)
 #####               





network_name =  params['input_filenames'][0] # name_solution.dat and name_async_unweigh_ssprob_all.txt files
plot_plotterdata = 0 # if boolean plot values are included or not

left= params['constant_node_count'][0]   
right=len(id_to_node)-1

#give column range of genes you want to classify, 0 indexed
# print(data)
# exit(0)
length=right-left+1



binlabelformat = "{0:0" + str(length) +  "b}"


rac_probfile=open("Datafiles/{}_racipe_probfull.txt".format(network_name))

rac_probdata = rac_probfile.read().split("\n")[0:]

if "" in rac_probdata:
    rac_probdata.remove("")
rac_probfile.close()

xaxislabel= []
final_xaxislabel=[]
yaxis = []
final_yaxis =[]
xaxis=[]
final_xaxis=[]
final_index=[]
racipeclassify = {}

for k in rac_probdata:
    temp = k.split(" ")
    xaxislabel.append(temp[0])
    yaxis.append(float(temp[1]))
    if(float(temp[1]) >=0.01):
        final_xaxislabel.append(temp[0])
        final_index.append(int(temp[0],2))
        
    racipeclassify[ int(temp[0],2) ]  = float(temp[1])


final_yaxis = [racipeclassify[i] for i in final_index]
final_xaxislabel = [binlabelformat.format(i) for i in final_index]
argarr = np.argsort(np.array(final_yaxis))[::-1]

final_yaxis = [final_yaxis[i] for i in argarr]
final_xaxislabel = [final_xaxislabel[i] for i in argarr]
final_xaxis = np.linspace(0, len(final_yaxis), len(final_yaxis))
plt.figure(figsize=(20,12))

#print(final_yaxis)
#print(final_xaxislabel)

if(not(plot_plotterdata)):
    rcParams.update({'figure.autolayout':True})
    plt.bar(final_xaxis,final_yaxis, width = 0.3, color = 'r')
    plt.xticks(final_xaxis, final_xaxislabel, rotation = 'vertical')
    # plt.show()
    plt.savefig("{}_racipeVbool.png".format(network_name))

# print(argarr)
# print(yaxis)


if plot_plotterdata:
    dataplotter = open("output/{}_ssprob_all.txt".format("{}_async_unweigh".format(network_name)),'r').read().split("\n")[1:-1]
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
            dict_yaxis.update( {x_labels[i] : len(final_xaxis)+cnt} )
            final_yaxislist.append(0)
            cnt+=1

    final_ydata = np.zeros(len(list_labels))
    for i in range(len(y_data)):
        if(x_labels[i] in dict_yaxis):
            index=dict_yaxis[x_labels[i]]
            if(y_data[i] >=0.01):
                final_ydata[index]=y_data[i]
            else:    
                final_ydata[index]=0

    weight = 0.35
    final_xaxis=[i for i in range(len(list_labels)) ]
    rcParams.update({'figure.autolayout':True})
    final_yaxislist=np.array(final_yaxislist)
    rac_sum=0
    for q in range(len( final_yaxislist )):
        rac_sum+=final_yaxislist[q]
        
    final_yaxislist=  final_yaxislist / rac_sum  
    
    bool_sum=0
    for q in range(len( final_ydata )):
        bool_sum+=final_ydata[q]
        
    final_ydata=  final_ydata / bool_sum 
    #plt.figure(figsize = (20,10))       
    fig, ax = plt.subplots(1,1)
    plt.bar(final_xaxis,np.array(final_yaxislist) , width = 0.3, color = 'r')
    plt.bar(np.array(final_xaxis)+weight, final_ydata, width = 0.3, color = 'b')
    plt.xticks(final_xaxis,list_labels, rotation = 'vertical')
    jsd=jensenshannon(final_ydata,np.array(final_yaxislist),2 )
    plt.title( "JSD = {}".format(jsd))
    plt.tight_layout()
    # plt.show()
    plt.savefig("Boolvsracipegraphs/{}_racipeV{}.png".format(network_name,version))
    #try:
    #    jsdfile=open("cont_jsd.txt","a")
    #except:
    #    jsdfile=open("cont_jsd.txt","w+")
    jsdfile=open("{}_jsd.txt".format(version),"a")
    jsdfile.write("{} {}\n".format(network_name,jsd))
    jsdfile.close()
    # print(final_ydata)

# print(xaxislabel)



