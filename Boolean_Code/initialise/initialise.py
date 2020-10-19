import initialise.strictdict as strictdict
import os

def initialise(initfilename, max_initlines):
    #initial conditions dictionary
    params = {}
    params['maxtime'] = 200
    params['input_folder_name'] = 'input'
    params['output_folder_name'] = 'output'
    params['input_filenames'] = ""
    params['num_simulations'] = 1000
    params['asynchronous_run'] = 1
    params['synchronous_run'] = 0
    params['weighted_run'] = 0
    params['unweighted_run'] = 1
    params['file_reqs'] = []
    params['selective_edge_weights'] = 0
    params['randomise_edges_file'] = ""
    params['constant_node_count'] = ""
    params['num_runs'] = 1
    params['num_threads'] = 5
    params = strictdict.StrictDict(params)

    #parse initfile
    initfile = open(initfilename, 'r').read().split("\n")[:-1]
    if len(initfile) != max_initlines:
        raise ValueError("Too many input arguments in init.txt")
    for i in initfile:
        temp = i.split(" ")
        params[temp[0]] = temp[1]
    for i in range(3,len(initfile)-2):
        params[initfile[i].split(" ")[0]] = int(params[initfile[i].split(" ")[0]])
    #params dictionary set properly now
    #next, split all filenames
    params['input_filenames'] = params['input_filenames'].split(",")
    #split all constant_node_count(s)
    params['constant_node_count'] = [int(i) for i in params['constant_node_count'].split(",")]

    if len(params['constant_node_count']) != len(params['input_filenames']):
        raise ValueError("Different number of constant node counts and filenames, please recheck {} file".format(initfilename))
    if (params['num_runs'] < 1) or (params['num_threads'] < 1):
        raise ValueError("{} cannot be less than 1.".format("num_runs" if params['num_threads'] else "num_threads"))
    if params['asynchronous_run'] == 0 and params['synchronous_run'] == 0:
        raise ValueError("Atleast one of sync/async must be 1.")
    elif params['weighted_run'] == 0 and params['unweighted_run'] == 0:
        raise ValueError("Atleast one of weighted/unweighted must be 1.")
    if params['selective_edge_weights'] == 1 and (params['weighted_run'] == 1 or params['unweighted_run'] == 0):
        raise ValueError("selective_edge_weights is usable only when unweighted_run is set to 1 and weighted_run is set to 0")
    return params

def set_file_reqs(params):
    modifiers = [[],[],[]]
    final_combi = []
    if params['asynchronous_run']:
        modifiers[0].append('_async')
    if params['synchronous_run']:
        modifiers[0].append("_sync")
    if params['weighted_run']:
        modifiers[1].append("_weigh")
    if params['unweighted_run']:
        modifiers[1].append("_unweigh")
    for i in modifiers[0]:
        for j in modifiers[1]:
            final_combi.append(i+j)
    if params['selective_edge_weights']:
        for i in range(len(final_combi)):
            final_combi[i] += '_selective'

    # create output folders if they don't exist
    try:
        os.mkdir('{}'.format(params['output_folder_name']))
        print("Made folder {}".format(params['output_folder_name']))
    except:
        print("Folder {} exists already.".format(params['output_folder_name']))
    try:
        os.mkdir('{}/graphs'.format(params['output_folder_name']))
        print("Made folder {}/graphs".format(params['output_folder_name']))
    except:
        print("Folder {}/graphs exists already.".format(params['output_folder_name']))
    return final_combi
