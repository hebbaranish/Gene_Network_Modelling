import multiprocessing
import os
import time
import initialise.initialise as initialise
import initialise.parser as parser
from modules.control import control_function
import modules.plotter as plotter
import sys
import datetime
import psutil

# import parser
# import sync
# import async

if __name__ == '__main__':
    if len(sys.argv) == 2:
        in_file = sys.argv[1]
    else:
        in_file = 'init.txt'
    per=100
    begin = time.time()
    max_initlines = 14
    params = initialise.initialise(in_file, max_initlines)
    params['file_reqs'] = initialise.set_file_reqs(params)

    # print(params)
    # exit(0)
    # id_to_node_list = []
    # link_matrix_list = []
    # for i in params['input_filenames']:
    #     a,b = parser.parse_topo(params['input_folder_name'],i)
    #     link_matrix_list.append(a)
    #     id_to_node_list.append(b)

    #initialise process
    # async_tick = []
    p=[]
    process_count = 0
    ac=2
    # async_tick = []
    for i in params['file_reqs']:
        for j in params['input_filenames']:
            for cur_run in range(params['num_runs']):
                random_seed = int(begin) + process_count
                weighted_tick = 1 if "_weigh" in i else 0
                async_tick = 1 if "_async" in i else 0
                link_matrix, id_to_node = parser.parse_topo(params,j,weighted_tick, random_seed)
                q1=0
                
                #for u in range(0,4):
                #    for v in range(0,4):
                #        if(link_matrix[u][v]!=0):
                #            q1+=1
                #        if(q1== ((cur_run))//(ac*per) +1 ):
                #                if(link_matrix[u][v]>0):
                #                   link_matrix[u][v]=(cur_run%(ac*per) )/per
                #                elif(link_matrix[u][v]<0):
                #                    link_matrix[u][v]=-(cur_run%(ac*per)  )/per
                #                break
                                
                #if(cur_run%100==0):
                #    print(link_matrix)
                # link_matrix_list.append(link_matrix)
                # id_to_node_list.append(id_to_node)
                # print(link_matrix)
                # print(id_to_node)
                # exit(0)
                p.append(multiprocessing.Process(target = control_function, args = (begin,async_tick, link_matrix, id_to_node, params, process_count + random_seed, j+i,cur_run+1,)))
                p[process_count].daemon = False
                p[process_count].start()
                p[process_count].join()
                p[process_count].close()
                process_count += 1


            finish_flag = 1
            #for proc in psutil.process_iter():
            #    print (proc.open_files())
            #while finish_flag:
            #    finish_flag = 0
            #    time.sleep(1)
            #    for meow in range(process_count):
            #        if p[meow].is_alive():
            #            finish_flag = 1
            #            break
            plotter.plot_bar(j+i, id_to_node, params)
    os.remove("temp.txt")
    print("Finished in {} (h:m:s)".format(datetime.timedelta(seconds = int(time.time() - begin))))
