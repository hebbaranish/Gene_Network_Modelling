import initialise.initialise as initialise
import initialise.parser as parser
import sys
import os

if len(sys.argv) == 2:
    in_file = sys.argv[1]
else:
    in_file = 'init.txt'

max_initlines = 14
params = initialise.initialise(in_file, max_initlines)

for filenum in range(len(params['input_filenames'])):
    if(os.path.exists("{}/{}.ids".format(params['input_folder_name'], params['input_filenames'][filenum]))):
        a = input("{}.ids file exists already, overwrite? (Y/N)  ".format(params['input_filenames'][filenum]))
        # print("{}.".format(a))
        if(a.lower() != 'y' and a.lower() != 'n'):
            raise ValueError("Incorrect format entered, exiting.")
        else:
            if a.lower() == 'y':
                pass
            else:
                exit("Exiting...")

    topo_file = params['input_filenames'][filenum]
    constant_nodes = input("Need {} constant genes for {} file. Please separate gene names by commas: ".format(params['constant_node_count'][filenum], topo_file)).split(",")

    if len(constant_nodes) != params['constant_node_count'][filenum]:
        raise ValueError("Number of constant nodes entered is not valid. Try again.")

    input_foldername = params['input_folder_name']
    a = open("{}/{}.topo".format(input_foldername, topo_file)).read().split("\n")[1:-1]
    # print(a)
    genes = set([])
    for i in a:
        temp = i.split(" ")
        genes.add(temp[0])
        genes.add(temp[1])

    for i in constant_nodes:
        if i not in genes:
            raise ValueError("Node {} is not present in {}.topo, please recheck.".format(i, topo_file))

    id_dict = {}
    id_num = 0
    remove_list = []
    for i in constant_nodes:
        for j in genes:
            if i == j:
                id_dict[i] = id_num
                id_num += 1
                remove_list.append(j)
    for i in remove_list:
        genes.remove(i)

    for i in genes:
        id_dict[i] = id_num
        id_num += 1

    idsfile = open("{}/{}.ids".format(input_foldername, topo_file), 'w')
    idsfile.write("Node ID\n")
    list_genes = list(id_dict.keys())
    for i in list_genes:
        idsfile.write("{} {}\n".format(i, id_dict[i]))
    idsfile.close()

    print("Successfully created {}.ids file.".format(topo_file))
