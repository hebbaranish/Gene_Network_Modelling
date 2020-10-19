import modules.async_sim as async_sim
import modules.async_sim1 as async_sim1
import modules.sync_sim as sync_sim
import modules.sync_sim_1 as sync_sim_1
def control_function(begin,async_tick, link_matrix, id_to_node, params, random_seed, filename,cur_run):
    if async_tick:
        async_sim.async_simulator(begin,random_seed, link_matrix, id_to_node, params, filename,cur_run)
        
        
    else:
        sync_sim_1.sync_simulator(begin,random_seed, link_matrix, id_to_node, params, filename,cur_run)
        #u=0