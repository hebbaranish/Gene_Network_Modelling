import time
import initialise.initialise as initialise
import sys
import datetime
import pandas as pd
import numpy as np
import os.path
from os import path

if __name__ == '__main__':
    if len(sys.argv) == 2:
        in_file = sys.argv[1]
    else:
        in_file = 'init.txt'
    max_initlines = 14
    begin = time.time()
    params = initialise.initialise(in_file, max_initlines)
    q=0
    for i in params['input_filenames']:
        topo_data={}    
        try:
            topo_data = pd.read_csv("{}/{}.topo".format(params['input_folder_name'], i), sep = " ").to_numpy()
        except:
            print("ERROR: Input file {}.topo does not exist.".format(i))
            exit()
        f=0    
        if(path.exists("{}/{}.ids".format(params['input_folder_name'],i))):
            while(f==0):
                confirm = input ("Input file {}.ids already exists. Are you sure you wish to overwrite it? Enter y/n for confirmation.".format(i))
                if(confirm!='y' and confirm!='n'):
                    print("ERROR: Wrong format for confirmation. Try again")
                else:
                    if(confirm=='y'):
                        f=1
                        break
                    else:
                        break
        else:
            f=1
        if(f==0):
            q+=1
            continue
        node_id_file = open("{}/{}.ids".format(params['input_folder_name'],i), 'w')    
        #getting unique node names and assigning ids
        node_names = set([])
        for j in topo_data:
            node_names.add(j[0])
            node_names.add(j[1])    
        constnodes={}
        mark=0
        while(mark==0):
            try:
                if(params['constant_node_count'][q]==0):
                    print("You have specified {} constant nodes for this network.Generating IDs.....".format(params['constant_node_count'][q]))
                    mark=1
                elif(params['constant_node_count'][q]==1): 
                    constnodes=input("You have specified {} constant node for this network. Please enter it.".format(params['constant_node_count'][q])).split(",")
                    if(len(constnodes)!=params['constant_node_count'][q]):
                        print("ERROR: Number of constant nodes doesn't match. Try again")
                        continue
                    mark2=1   
                    for u in range(len(constnodes)):        
                        if constnodes[u] in node_names:
                            f=1
                        else:
                            print("ERROR: {} doesn't exist in the topo file specified. Try again".format(constnodes[u]))
                            mark2=0
                            break
                    mark=mark2
                else:   
                    constnodes=input("You have specified {} constant nodes for this network. Please enter them, comma separated in the order needed. Example:GRHL2,miR200 ".format(params['constant_node_count'][q])).split(",")
                    if(len(constnodes)!=params['constant_node_count'][q]):
                        print("ERROR: Number of constant nodes doesn't match. Try again")
                        continue
                    mark2=1   
                    for u in range(len(constnodes)):        
                       if constnodes[u] in node_names:
                           f=1
                       else:
                           print("ERROR: {} doesn't exist in the topo file specified. Try again".format(constnodes[u]))
                           mark2=0
                           break
                    mark=mark2
            except:
                print("ERROR: Input format was wrong. Try again")
       
        final_node_names = set([])  
        for u in range(len(constnodes)):
            final_node_names.add(constnodes[u])            
       
        node_id_file = open("{}/{}.ids".format(params['input_folder_name'],i), 'w')    
        #getting remaining node names and assigning ids
        for j in topo_data:
            final_node_names.add(j[0])
            final_node_names.add(j[1])
        final_node_names = sorted(list(final_node_names))
     
        n = len(final_node_names)    
             
        node_id_file.write("node id\n")
        for j in range(n):
            node_id_file.write(str(final_node_names[j])+" "+str(j)+"\n")
        node_id_file.close()
        print("Succesfully specified gene IDs in {}.ids".format(i))
        q+=1
        
    print("Finished in {} (h:m:s)".format(datetime.timedelta(seconds = int(time.time() - begin))))
        
        
    
    
    