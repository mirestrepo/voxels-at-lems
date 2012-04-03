# Script to crop a voxel grid
# Author : Isabel Restrepo
# 6-14-2009

import bvpl_batch
import time
#time.sleep(60);
bvpl_batch.register_processes();
bvpl_batch.register_datatypes();


class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

data_dir = "/Volumes/Experiments/object_recognition/bvpl/CapitolSiteHigh/cropped_world"


print("Load Voxel World");
bvpl_batch.init_process("bvxmLoadGridProcess");
bvpl_batch.set_input_string(0, data_dir +"/ocp_cropped.vox");
bvpl_batch.set_input_string(1,"float");
bvpl_batch.run_process();
(world_id,world_type)= bvpl_batch.commit_output(0);
world = dbvalue(world_id,world_type);

print("Creating 3D edge kernel");
bvpl_batch.init_process("bvplCreateEdge3dKernelVectorProcess");
bvpl_batch.set_input_unsigned(0,3);
bvpl_batch.set_input_unsigned(1,3);
bvpl_batch.set_input_unsigned(2,3);
bvpl_batch.run_process();
(kernel_id,kernel_type)= bvpl_batch.commit_output(0);
kernel_vector = dbvalue(kernel_id,kernel_type);

print("Running Operator");
bvpl_batch.init_process("bvplNeighborhoodOperatorProcess");
bvpl_batch.set_input_from_db(0,world );
bvpl_batch.set_input_from_db(1,kernel);
bvpl_batch.set_input_string(2,"float");
bvpl_batch.set_input_string(3,"edge_algebraic_mean");
bvpl_batch.set_input_string(4, data_dir + "/edge_alge_100.vox");
bvpl_batch.run_process();
(result_x_world_id,result_x_world_type)= bvpl_batch.commit_output(0);
result_x_world = dbvalue(result_x_world_id,result_x_world_type);


print("Writing World");
bvpl_batch.init_process("bvxmSaveGridRawProcess");
bvpl_batch.set_input_from_db(0,result_x_world);
bvpl_batch.set_input_string(1,data_dir + "/edge_alge_100.raw");
bvpl_batch.set_input_string(2,"float");
bvpl_batch.run_process();

