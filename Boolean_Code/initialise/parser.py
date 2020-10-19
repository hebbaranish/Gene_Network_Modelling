import pandas as pd
import numpy as np

def parse_topo(params, filename, weighted, process_seed):
    # reading topo data
    topo_data = pd.read_csv("{}/{}.topo".format(params['input_folder_name'], filename), sep = " ").to_numpy()
    np.random.seed(process_seed)
    #getting unique node names and assigning ids
    # node_names = set([])
    # for i in topo_data:
    #     node_names.add(i[0])
    #     node_names.add(i[1])
    # node_names = sorted(list(node_names))
    # node_id = [i for i in range(len(node_names))]
    try:
        node_id_file = open("{}/{}.ids".format(params['input_folder_name'], filename), 'r').read().split("\n")[1:-1]
    except:
        raise FileNotFoundError("Please add '{}.ids' file in the '{}' directory, with a list of genes and IDs.".format(filename, params['input_folder_name']))
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
    if weighted == 0: # 1,0,-1
        for i in topo_data:
            link_matrix[i[0]][i[1]] = 1 if i[2] == 1 else -1
    elif weighted == 1: # rand, 0, -rand, where rand is sampled from gaussian distribution [0,1)
        for i in topo_data:
            # temp_rand = np.random.normal(0,1)
            temp_rand = np.random.rand()
            link_matrix[i[0]][i[1]] = temp_rand if i[2] == 1 else -temp_rand

    # adding random weights for selected nodes, if needed:
    if params['selective_edge_weights']:
        node_data = open("{}/{}".format(params['input_folder_name'], params['randomise_edges_file']), 'r').read().split('\n')[1:-1]
        for temp in node_data:
            temp_rand = np.random.rand()
            i = temp.split(" ")
            i[0] = node_to_id[i[0]]
            i[1] = node_to_id[i[1]]
            link_matrix[i[0]][i[1]] = temp_rand if link_matrix[i[0]][i[1]] == 1 else -temp_rand
    #make a id to node dictionary
    id_to_node = dict(zip(node_id, node_names))
    #return statements
    return link_matrix, id_to_node
