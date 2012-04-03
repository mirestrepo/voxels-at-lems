# Script to run save a grid as vrml
# Author : Isabel Restrepo
# 10-7-2009

import bvxm_batch
import time
import os
#time.sleep(30);
bvxm_batch.register_processes();
bvxm_batch.register_datatypes();


class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string


data_dir = "/Users/isa/Experiments/CapitolSFM/few_windows";
output_dir = "/Users/isa/Experiments/CapitolSFM/few_windows";

if not os.path.isdir( output_dir + "/"):
  os.mkdir( output_dir + "/");



#print("Load Voxel Grid");
#bvxm_batch.init_process("bvxmLoadGridProcess");
#bvxm_batch.set_input_string(0, data_dir +"/KL_gaussf1.vox");
#bvxm_batch.set_input_string(1,"bsta_gauss_f1");
#bvxm_batch.run_process();
#(world_id,world_type)= bvxm_batch.commit_output(0);
#app_grid = dbvalue(world_id,world_type);


print("Load Voxel Grid");
bvxm_batch.init_process("bvxmLoadGridProcess");
bvxm_batch.set_input_string(0, data_dir +"/ocp.vox");
bvxm_batch.set_input_string(1,"float");
bvxm_batch.run_process();
(world_id,world_type)= bvxm_batch.commit_output(0);
ocp_grid = dbvalue(world_id,world_type);

print("Writing Orientation Grid");
bvxm_batch.init_process("bvxmSaveRGBAGridVrmlProcess");
bvxm_batch.set_input_from_db(0,ocp_grid);
bvxm_batch.set_input_float(1,0.3);
bvxm_batch.set_input_string(2,output_dir + "/ocp_s.wrl");
bvxm_batch.run_process();