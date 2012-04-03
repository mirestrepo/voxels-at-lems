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
param_dir = "/Projects/lemsvxl/src/contrib/isabel/params"
#first creat an empty world.
print("Load Voxel World");
bvpl_batch.init_process("bvxmLoadGridProcess");
bvpl_batch.set_input_string(0, data_dir +"/ocp_cropped.vox");
bvpl_batch.set_input_string(1,"float");
bvpl_batch.run_process();
(world_id,world_type)= bvpl_batch.commit_output(0);
world = dbvalue(world_id,world_type);

print("Creating 2D edge kernel");
bvpl_batch.init_process("bvplCreateEdge2dKernelVectorProcess");
bvpl_batch.set_input_unsigned(0, 5);
bvpl_batch.set_input_unsigned(1, 5);
bvpl_batch.run_process();
(kernel_id,kernel_type)= bvpl_batch.commit_output(0);
kernel_vector = dbvalue(kernel_id,kernel_type);

print("Running Operator");
bvpl_batch.init_process("bvplVectorOperatorProcess");
bvpl_batch.set_input_from_db(0,world );
bvpl_batch.set_input_from_db(1,kernel_vector);
bvpl_batch.set_input_string(2,"float");
bvpl_batch.set_input_string(3,"edge2d");
bvpl_batch.set_input_string(4, data_dir + "/edge2d_all.vox");
bvpl_batch.set_input_string(5, data_dir + "/edge2d_all_orientations.vox");
bvpl_batch.run_process();
(response_grid_id,response_grid_type)= bvpl_batch.commit_output(0);
response_grid = dbvalue(response_grid_id,response_grid_type);
(orientation_grid_id,orientation_grid_type)= bvpl_batch.commit_output(1);
orientation_grid = dbvalue(orientation_grid_id,orientation_grid_type);

print("Writing Response Grid");
bvpl_batch.init_process("bvxmSaveGridRawProcess");
bvpl_batch.set_input_from_db(0,response_grid);
bvpl_batch.set_input_string(1,data_dir + "/edge2d_all.raw");
bvpl_batch.set_input_string(2,"float");
bvpl_batch.run_process();

print("Writing Orientation Grid");
bvpl_batch.init_process("bvxmSaveGridRawProcess");
bvpl_batch.set_input_from_db(0,orientation_grid);
bvpl_batch.set_input_string(1,data_dir + "/edge2d_all_orientation.raw");
bvpl_batch.set_input_string(2,"float");
bvpl_batch.run_process();


