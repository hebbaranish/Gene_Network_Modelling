import os


dict={
  "GRHL2": 7,
  "GRHL2wa": 8,
  "OVOL2": 9,
  "OVOLsi": 8,
  "NRF2": 16,
  "OCT4": 10,
  "GRHL2f": 7
}
network='GRHL2'
init_info = """input_folder_name input
output_folder_name output
input_filenames {}
num_threads 10
num_runs 3
num_simulations 10000
maxtime 2000
asynchronous_run 1
synchronous_run 0
weighted_run 0
unweighted_run 1
selective_edge_weights 0
randomise_edges_file randomise.txt
constant_node_count 1
"""
try:
    os.mkdir("output")
except:
    pass
for i in range( dict[network]):
    for j in range(i+1, dict[network]):
            for k in range(0, dict[network]+1):
                print("processing {}{}_{}".format(i+1, j+1,  k))
                strtemp = "{}{}_{}".format(i+1, j+1,  k)
                fileboi = open("init.txt", "w")
                fileboi.write(init_info.format(strtemp))
                fileboi.close()
                os.system("./main")
                print("")
                # exit(0)
