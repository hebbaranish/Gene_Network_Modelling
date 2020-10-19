import numpy as np
import time
import multiprocessing
from multiprocessing import Value, Lock, Process
import os
import sys
lock = Lock()
ss_file = open("temp.txt", 'w')
nss_file = open("temp.txt", 'w')
initstates = open("temp.txt", 'w')

def simulate(begin,cur_run,random_seed,max_sim,link_matrix,n,params,filename,counter,id_counter):
    sim_num = 0
    global lock
    global ss_file
    global nss_file
    global initstates
    np.random.seed(random_seed + 10 * os.getpid())
    while sim_num < max_sim:
        # print(sim_num)
        # print(id_to_node)
        # exit(0)
        # curstate = np.array([1,-1,-1,1])
        # print(curstate)
        #lock.acquire()
        curstate = np.random.choice([-1,1], n)
        #lock.release()
        init_state = np.array(curstate)
        #print(init_state)
        # stable_counter = np.full(n, 0)
        stable_checker = 0
        for timeiter in range(params['maxtime']):
            stable_checker = 1
            activation = np.matmul(curstate, link_matrix)
            # print(curstate)
            # for i in range(n):
            #     if stable_counter[i] != curstate[i]:
            #         stable_checker = 0
            #         break
            for i in range(n):
                if activation[i] * curstate[i] < 0:
                    # print(activation[i] * curstate[i])
                    stable_checker = 0
                    break
            if stable_checker:
                lock.acquire()
                id_counter.value+=1
                stable_str = "{} ".format(id_counter.value)
                init_str = "{} ".format(id_counter.value)
                lock.release()
                #print(init_state)
                for i in init_state:
                    init_str += str(i) + " "
                for i in curstate:
                    stable_str += "{} ".format(i)
                #stable_str += "{} ".format(os.getpid())
                #init_str += "{} ".format(os.getpid())
                #print(init_str)
                #stable_str += init_str
                stable_str += "\n"
                init_str += "1\n"
                #lock.acquire()
                ss_file.write(stable_str)
                initstates.write(init_str)
                #lock.release()
                if ((counter.value)%(params['num_simulations']//100) == 0):
                    lock.acquire()
                    if ((counter.value)%(params['num_simulations']//100) == 0):
                        sys.stdout.write("{}_{}: {}% in {:.2f}s\r".format(filename,cur_run,int((counter.value)/params['num_simulations']*100), time.time()-begin))
                        if(params['num_runs']!=cur_run or int((counter.value)/params['num_simulations']*100)!=99 ):
                            sys.stdout.flush()
                        else:
                            print("\n")
                    lock.release()
                lock.acquire()
                (counter.value) += 1
                lock.release()
                sim_num+=1
                # print(timeiter)
                #lock.release()
                break
            else:
                #randnode = np.random.randint(0,n)
                #print(link_matrix)
                # print(activation)
                # print(randnode
                for i in range(n):
                    if activation[i] > 0:
                        curstate[i] = 1
                    elif activation[i] < 0:
                        curstate[i] = -1
        if (stable_checker==0):
            lock.acquire()
            id_counter.value+=1
            init_str = "{} ".format(id_counter.value)
            nss_str = "{} ".format(id_counter.value)
            for i in init_state:
                init_str += str(i) + " "
            for i in curstate:
                nss_str += "{} ".format(i)
            nss_str += "\n"
            init_str += "0\n"
            nss_file.write(nss_str)
            initstates.write(init_str)
            lock.release()
            #lock.release()
            # stable_counter[randnode] = curstate[randnode]
        # print(activation, " ", curstate, " ", init_state)
        # print(curstate)
        # print(id_to_node)
        # exit(0)
        #if stable_checker == 0:
    initstates.flush()
    ss_file.flush()
    nss_file.flush()
    #print(multiprocessing.current_process())
        # print(id_to_node)
        # exit(0)

def sync_simulator(begin,random_seed, link_matrix, id_to_node, params, filename, cur_run):
    global lock
    #lock.acquire()
    counter = Value('i',0)
    id_counter = Value('i',0)
    threads = params['num_threads']
    global ss_file
    global nss_file
    global initstates
    #np.random.seed(random_seed + np.random.randint(0,10000))
    n = link_matrix.shape[0]
    header_format = "ID "
    for i in range(n):
        if i == n-1:
            header_format += "{}"
            break
        header_format += "{} "
    ss_file.seek(0, 2)
    q=ss_file.tell()
    if(ss_file.tell() == 0):
        if "_weigh" in filename or params['selective_edge_weights']:
            np.savetxt("{}/{}_weights_run{}.txt".format(params['output_folder_name'], filename, cur_run), link_matrix, fmt = "%.7f")
    if(ss_file.tell()==0):
        ss_file = open("{}/{}_ss_run{}.txt".format(params['output_folder_name'], filename, cur_run), 'w')
        ss_file.write(header_format.format(*[id_to_node[i] for i in range(n)]) + "\n")
        ss_file.flush()
        nss_file = open("{}/{}_nss_run{}.txt".format(params['output_folder_name'], filename, cur_run), 'w')
        nss_file.write(header_format.format(*[id_to_node[i] for i in range(n)]) + "\n")
        nss_file.flush()
        initstates = open("{}/{}_init_run{}.txt".format(params['output_folder_name'], filename, cur_run), 'w')
        initstates.write(header_format.format(*[id_to_node[i] for i in range(n)]) + " Stable\n")
        initstates.flush()
    #lock.release()
    num_simulthread=[0]*threads
    for u in range(0,threads-1):
        num_simulthread[u]=params['num_simulations']//threads
    num_simulthread[threads-1]=params['num_simulations']//threads +params['num_simulations']%threads
    procs = [Process(target=simulate, args=(begin,cur_run,random_seed,num_simulthread[u],link_matrix,n,params,filename,counter,id_counter)) for u in range(threads)]
    for p in procs: p.daemon=True
    for p in procs: p.start()
    for p in procs: p.join()
    #print(counter.value)
    ss_file.close()
    nss_file.close()
    initstates.close()
