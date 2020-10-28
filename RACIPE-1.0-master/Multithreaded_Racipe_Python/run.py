import os
import shutil
import multiprocessing
import pandas as pd
from time import time, sleep
import datetime
import subprocess

start_time = time()

# ************RACIPE parameter list*******************
param_dict = {}
param_dict['maxtime'] = 23.5
param_dict['solver'] = 1
param_dict['flag'] = 0
param_dict['dist'] = 1
param_dict['SF'] = 1
param_dict['num_findT'] = 100
param_dict['num_paras'] = 300
param_dict['num_ode'] = 100
param_dict['num_stability'] = 10
param_dict['thrd'] = 1.0
param_dict['Toggle_f_p'] = 1
param_dict['stepsize'] = 0.1
param_dict['maxiters'] = 20
param_dict['Toggle_T_test'] = 1
param_dict['SBML_model'] = 0
param_dict['seed'] = 0 # Remember to change this for each run
param_dict['minP'] = 1.0
param_dict['maxP'] = 100.0
param_dict['minK'] = 0.1
param_dict['maxK'] = 1.0
param_dict['maxN'] = 1.0
param_dict['minF'] = 6.0
param_dict['maxF'] = 100.0
# param_dict['KDID'] = ""
# param_dict['OEID'] = ""
# param_dict['OEFD'] = ""
# param_dict['DEID'] = ""
# param_dict['DEFD'] = ""

# *************python parameters****************
num_threads = 3 #default
master_dir = os.getcwd()
topo_filename = ""

#***************user input***********************
input_file = open("init.txt").read()
input_file = input_file.split("\n")[:-1]
extract_count = 0

# filename - line 1
temp = input_file[extract_count]
temp = temp.split(" ")[1]
temp = temp.split(".")
topo_filename = temp[0] + '{}.' + temp[1]
extract_count += 1
# print(extract_count)

#threads - line 2
temp = input_file[extract_count]
temp = temp.split(" ")[1]
num_threads = int(temp)
extract_count += 1
# print(extract_count)

# params with integer inputs - line 3 to 14
for i in range(3,15):
    temp = input_file[extract_count].split(" ")
    param_dict[temp[0]] = int(temp[1])
    extract_count += 1
    # print(extract_count)

# params with float inputs - line 15 to 25
for i in range(15,26):
    temp = input_file[extract_count].split(" ")
    param_dict[temp[0]] = float(temp[1])
    extract_count += 1
    # print(extract_count)

# params with random lengths of inputs - line 26 to 30
# for i in range(26,31):
#     temp = input_file[extract_count].split(" ")
#     inputs = ""
#     for j in range(1,len(temp)):
#         inputs += temp[j] + " "
#     inputs = inputs[:-1]
#     param_dict[temp[0]] = inputs
#     extract_count += 1
#     # print(extract_count)

# ***********dividing params amongst threads*************
temp_param_count = param_dict['num_paras'] #modified during param distribution btw!
#check if parameters per process is > 100
thread_num_change = 0 #flag
while int(temp_param_count/num_threads) < 100:
    num_threads -= 1
    thread_num_change = 1
    if num_threads == 0:
        print("Please give atleast 100 parameters for processing. Exiting program...")
        exit(0)
if thread_num_change == 1:
    print("Thread number has been changed to {} to give at least 100 parameters to each process. This causes issues in RACIPE otherwise".format(num_threads))
    print("Press enter to continue, or stop process to change parameters:")
    c = input()

#distribute parameters
param_dist = []
for i in range(num_threads-1):
    param_dist.append(int(temp_param_count/(num_threads-i)))
    temp_param_count -= int(temp_param_count/(num_threads-i))
param_dist.append(temp_param_count)

def command_maker(filename, param_dict, cur, num_threads):
    #remember to check if KDID and so on are empty or not. if empty, dont include in racipe
    # list_verify = ["KDID", "OEID", "OEFD", "DEID", "DEFD"]
    exclude = []
    global racipe_command
    racipe_command = "./RACIPE "+filename.format(cur+1) + " "
    racipe_command += "-{} {} -{} {} ".format("maxthreads", num_threads, "curthread", cur)
    # for i in list_verify:
    #     if param_dict[i] == "":
    #         exclude.append(i)
    key_list = list(param_dict.keys())
    for i in key_list:
        if i not in exclude:
            racipe_command += "-{} {} ".format(i, param_dict[i])
    return racipe_command


def run_racipe(racipe_command):
    subprocess.call(racipe_command, shell=True)

# ******************processing**********************
total_num_paras = param_dict['num_paras']
p = []
for i in range(num_threads):
    param_dict['seed'] = i
    param_dict['num_paras'] = param_dist[i]
    racipe_command = command_maker(topo_filename, param_dict, i, num_threads)
    p.append(multiprocessing.Process(target = run_racipe, args = (racipe_command,)))
    shutil.copy('{}/{}'.format(master_dir, topo_filename.format("")), '{}/{}'.format(master_dir, topo_filename.format(i+1)))
    p[i].start()

process_completion_flag = 0
while process_completion_flag == 0:
    process_completion_flag = 1
    for i in range(num_threads):
        if p[i].is_alive():
            process_completion_flag = 0
            break
    sleep(1) #check if this harms process -> it does for time = 5, dont use it

param_dict['num_paras'] = total_num_paras
#****************Combining files*******************
filename_notopo = topo_filename.format("").split(".")[0]

#writing data into final file
# writing in parameter values
if(param_dict["Toggle_f_p"] == 1):
    a = pd.read_csv(filename_notopo + "1_parameters.dat", sep = "\t", header = None)
    for i in range(2,num_threads + 1):
        temp_frame = pd.read_csv(filename_notopo + "{}_parameters.dat".format(i), sep = "\t", header = None)
        temp_frame[0] = temp_frame[0].apply(lambda x: x+param_dist[i-1]*(i-1))
        a = pd.concat([a, temp_frame])
    a.to_csv(filename_notopo + "_parameters.dat", sep="\t", float_format = "%.6f", index = False, header = False)

# writing in T_test values
if(param_dict["Toggle_T_test"] == 1):
    b = pd.read_csv(filename_notopo + "1_T_test.dat", sep = "\t", header = None)
    for i in range(2,num_threads + 1):
        temp_frame = pd.read_csv(filename_notopo + "{}_T_test.dat".format(i), sep = "\t", header = None)
        temp_frame[0] = temp_frame[0].apply(lambda x: x+param_dist[i-1]*(i-1))
        b = pd.concat([b, temp_frame])
    b.to_csv(filename_notopo + "_T_test.dat", sep="\t", float_format = "%.6f", index = False, header = False)

# writing in solution_i values
for j in range(1,param_dict['num_stability'] + 1):
    a = pd.read_csv(filename_notopo + "1_solution_{}.dat".format(j), sep = "\t", header = None)
    for i in range(2,num_threads+1):
        temp_frame = pd.read_csv(filename_notopo + "{}_solution_{}.dat".format(i,j), sep = "\t", header = None)
        temp_frame[0] = temp_frame[0].apply(lambda x: x+param_dist[i-1]*(i-1))
        a = pd.concat([a, temp_frame])
    a.to_csv(filename_notopo + "_solution_{}.dat".format(j), sep="\t", float_format = "%.6f", index = False, header = False)

#writing in .prs file
shutil.copy('{}/{}'.format(master_dir, "{}1.prs".format(filename_notopo)), '{}/{}'.format(master_dir, "{}.prs".format(filename_notopo)))

#writing in .cfg file
shutil.copy('{}/{}'.format(master_dir, "{}1.cfg".format(filename_notopo)), '{}/{}'.format(master_dir, "{}.cfg".format(filename_notopo)))
a = open(filename_notopo + ".cfg", 'r').read().split("\n")[:-1]
a[3] = a[3].split("\t")
a[3] = a[3][0] + "\t{}".format(str(param_dict['num_paras']))
strcfg = ""
for i in a:
    strcfg += i + "\n"
a = open(filename_notopo + ".cfg", 'w')
a.write(strcfg)
a.close()

#***************Deleting old files***********************
for i in range(1,num_threads+1):
    tempname = [filename_notopo + "{}.topo", filename_notopo + "{}_parameters.dat", filename_notopo + "{}_T_test.dat", filename_notopo + "{}.prs", filename_notopo + "{}.cfg"]
    for j in tempname:
        os.remove("{}/{}".format(master_dir, j.format(i)))
    tempname = filename_notopo + "{}_solution_{}.dat"
    for j in range(1,param_dict['num_stability'] + 1):
        os.remove("{}/{}".format(master_dir, tempname.format(i, j)))

# print("Total time taken: {:.2f} minutes".format((time() - start_time)/60))
print("Total time taken: {} (h:m:s)".format(datetime.timedelta(seconds = int(time() - start_time))))
