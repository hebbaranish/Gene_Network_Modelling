import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import math
# import os

def plot_bar(filename, id_to_node, params):
    filename_index = 0
    for i in range(len(params['input_filenames'])):
        if "{}_".format(params['input_filenames'][i]) in filename:
            filename_index = i
            break
    per=100      
    ac=2
    probjsd_file1 = open("{}_jsd_1.txt".format(filename), 'w')        
    length=len(id_to_node) - params['constant_node_count'][filename_index]
    filematrix=[probjsd_file1]*(2**length)    
    for k in range(1,2**length    +1):
        filematrix[k-1]=open("{}_jsd_{}.txt".format(filename,k), 'w')   
    probjsd_file1.close()    
    prob_matrix = np.zeros((params['num_runs'], 2 ** (len(id_to_node) - params['constant_node_count'][filename_index])))
    gene_id_fin = [id_to_node[i] for i in range(params['constant_node_count'][filename_index], len(id_to_node))]
    string_setbin = "{0:0" + str(len(id_to_node) - params['constant_node_count'][filename_index]) + "b}"
    set_bin_fin = [string_setbin.format(i) for i in range(2 ** (len(id_to_node) - params['constant_node_count'][filename_index]))]
    #print(set_bin_fin)
    for cur_run in range(params['num_runs']):
        #print(cur_run)
        data = pd.read_csv("{}/{}_ss_run{}.txt".format(params['output_folder_name'], filename, cur_run+1), sep = " ", index_col = False)
        gene_id = list(data.columns)[1:]
        data = data.to_numpy()[:,1:]
        for i in range(params['constant_node_count'][filename_index]):
            gene_id.remove(id_to_node[i])
        # print(data, params['constant_node_count'][filename_index])
        data = data[:, params['constant_node_count'][filename_index]:]
        # print(data, gene_id)
        # exit(0)
        set_bin = set([])
        for t in range(0,2**length    ):
           k=t
           tempstr=''
           q1=0
           while(q1<length      ):
             if(k%2==0):
                tempstr+='1'
             else:
                tempstr+='0'
             k=k//2 
           
             q1+=1
           set_bin.add(tempstr)  
        set_bin = sorted(set_bin)
        #print(set_bin)
        #for i in data:
        #    tempstr = ""
        #    for j in i:
        #        tempstr += '0' if j < 0 else '1'
        #    set_bin.add(tempstr)
        #set_bin = sorted(set_bin)
        count = np.zeros(len(set_bin))
        for i in data:
            tempstr = ""
            for j in i:
                tempstr += '0' if j < 0 else '1'
            for j in range(len(set_bin)):
                if tempstr == set_bin[j]:
                    count[j] += 1
                    prob_matrix[cur_run][int(tempstr,2)] += 1
        count /= params['num_simulations']
        # print(count)
        # prob_matrix.append(count)
        #print(count)
        prob_file = open("{}/{}_ssprob_run{}.txt".format(params['output_folder_name'], filename, cur_run+1), 'w')
        for i in range(len(set_bin)):
            prob_file.write("{} {}\n".format(set_bin[i], count[i]))
            if(i!=len(set_bin)-1):
                filematrix[ cur_run//(ac*per)  ].write("{} ".format(count[i]))
            else:
                filematrix[ cur_run//(ac*per)  ].write("{}".format(count[i]))  
        if(cur_run+1 %(ac*per) !=0):        
            filematrix[ cur_run//(ac*per)  ].write("\n")        
        prob_file.close()
    for k in range(0,2**length):
        filematrix[k].close()
    # error = np.zeros(len(set_bin_fin))
    # final = np.zeros(len(set_bin_fin))
    error = [0 for i in range(len(set_bin_fin))]
    final = [0 for i in range(len(set_bin_fin))]
    finalin=[i for i in range(len(set_bin_fin))]
    # errortop = [0]*int(len(set_bin_fin))
    # errorbot = [0]*int(len(set_bin_fin))
    yterr=[ [0]*len(final),[0]*len(final) ]
    prob_matrix = np.matrix(prob_matrix)/params['num_simulations']
    
    # print(prob_matrix)
    for i in range(len(set_bin_fin)):
        # print(prob_matrix)
        error[i] = np.std(prob_matrix[:,i])
        final[i] = np.mean(prob_matrix[:,i])
        #print(error[i])
        dev1=0
        dev2=0
        cnt1=0
        cnt2=0
        arr1=prob_matrix[:,i]
        for v in range(params['num_runs']):
            if(arr1[v]>=final[i]):
                dev1+=(arr1[v]-final[i])**2
                cnt1+=1
            else:
                dev2+=(arr1[v]-final[i])**2
                cnt2+=1
        if(cnt1!=0):
            yterr[1][i]=math.sqrt(dev1/cnt1)
        if(cnt2!=0):
            yterr[0][i]=math.sqrt(dev2/cnt2)
        #print(dev1,dev2,cnt1,cnt2)
        #print(prob_matrix[:,i],error[i],final[i])
    # print(final, error, set_bin)
    #print(yterr)p
    #print(final)
    x_label = "States: "
    for i in gene_id:
        x_label += i + " "
    remove_index = []
    for i in range(len(final)):
        if final[i] ==0:
            remove_index.append(i)
    num_cycles = 0
    for temp in remove_index:
        i = temp - num_cycles
        final.remove(final[i])
        finalin.remove(finalin[i])
        error.remove(error[i])
        #errorbot.remove(errorbot[i])
        #errortop.remove(errortop[i])
        yterr[0].remove(yterr[0][i])
        yterr[1].remove(yterr[1][i])
        set_bin_fin.remove(set_bin_fin[i])
        num_cycles += 1

    prob_file = open("{}/{}_ssprob_all.txt".format(params['output_folder_name'], filename), 'w')
    prob_file.write("Node_Config Probability Error\n")
    for i in range(len(set_bin_fin)):
        prob_file.write("{} {:.6f} {:.6f}\n".format(set_bin_fin[i], final[i], error[i]))
    prob_file.close()

    notfinal_index = []
    notfinal= []
    notset_bin_fin= []
    notyterr0= []
    notyterr1= []
    #print(final)
    #print("ooha")
    for i in range(len(final)):
        if final[i] < 0.01:
            notfinal_index.append(i)
            notfinal.append(final[i])
            notset_bin_fin.append( set_bin_fin[i])
            notyterr0.append( yterr[0][i])
            notyterr1.append( yterr[1][i])
    #print(notfinal)
    #print("booga")    
    for i in range(len(notfinal_index)):
            final.remove(notfinal[i])
            set_bin_fin.remove( notset_bin_fin[i])
            yterr[0].remove(notyterr0[i])
            yterr[1].remove(notyterr1[i])
            #finalin.remove( notfinalin[i])
            
    #print(notfinal_index)
    #print("a")    
    #print(final)
    #print("b")    
    argarr = np.argsort(final)[::-1]
    #print(argarr)
    #print("1c")    
    #print(set_bin_fin)
    #print("1d")    
    set_bin_fin = [set_bin_fin[i] for i in argarr]
    #print(set_bin_fin)
    #print("1e")    
    final = [final[i] for i in argarr]
    #print(final)
    #print("1f")    
    # print(yterr, argarr)
    yterr[0] = [yterr[0][i] for i in argarr]
    yterr[1] = [yterr[1][i] for i in argarr]



    rcParams.update({'figure.autolayout':True}) #NOTE!!!!!!!!! properly resizes things :D
    plt.figure(figsize = (20,10))
    plt.subplots_adjust(0.1, 0.5, 0.9, 0.9)
    plt.title("{}_steady_states".format(filename))
    plt.xlabel(x_label)
    #print(x_label)
    plt.xticks(rotation = 'vertical')

    # print(yterr, final)

    #print(yterr)
    #errorbot=(np.array(errorbot)).reshape(1,len(final) )
    #errortop=(np.array(errortop)).reshape(1,len(final) )
    #print(np.array(errorbot))

        #yterr[1][u]=errortop[u][1][1]
    #print(yterr)
    
    plt.bar(set_bin_fin,final,yerr=yterr,capsize = 5)
    # try:
    #     os.chdir('graphs')
    # except:
    #     print("dir graphs exists")
    plt.savefig("{}/{}/{}_ss_barplot.png".format(params['output_folder_name'], 'graphs',filename))
    
