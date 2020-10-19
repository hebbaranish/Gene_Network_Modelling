import pandas as pd
import numpy as np

filename = "GRHL2"

topo_data = pd.read_csv(filename + ".topo", sep = " ").to_numpy()

try:
    node_id_file = open(filename + ".ids", 'r').read().split("\n")[1:-1]
except:
    raise FileNotFoundError("Please add '{}.ids' file, with a list of genes and IDs.".format(filename))
node_names = []
node_id = []
for i in node_id_file:
    # print(i)
    temp = i.split(" ")
    node_names.append(temp[0])
    node_id.append(int(temp[1]))
#creating a node to id dictionary
node_to_id = dict(zip(node_names, node_id))
# print(node_to_id)
# exit(0)
#checking if node ids are in ascending order starting from 0:
for i in range(len(node_id)):
    if node_id[i] != i:
        # print(node_id, i)
        raise ValueError("Please assign node IDs in an increasing order starting from 0 (i.e. 0,1,2,3...).")

#sorting out topo_data
for i in range(len(topo_data)):
    topo_data[i][0] = node_to_id[topo_data[i][0]]
    topo_data[i][1] = node_to_id[topo_data[i][1]]

n = len(node_names) #number of nodes

#generating link matrix (source,target)
link_matrix = np.zeros((n,n))
for i in topo_data:
    link_matrix[i[0]][i[1]] = 1 if i[2] == 1 else -1

#make a id to node dictionary
id_to_node = dict(zip(node_id, node_names))

print("{", end = "")
for i in link_matrix:
    print("{", end = "")
    for j in i:
        print("{},".format(int(j)), end = "")
    print("},", end = "")
print("}")
print("{", end = "")
for i in id_to_node.values():
    print('"' + i + '",', end = "")
print("}")

print("Number of nodes: {}".format(n))
