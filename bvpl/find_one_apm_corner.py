# Script to run find a one 2d corner on appearance grid
# Author : Isabel Restrepo
#8-31-2009

import bvpl_batch
import time
#time.sleep(30);
bvpl_batch.register_processes();
bvpl_batch.register_datatypes();


class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

save_hue = 1;
data_dir = "/Users/isa/Experiments/CapitolSFM/few_windows"
output_dir = "/Users/isa/Experiments/CapitolSFM/few_windows/corner2d_apm/0_plane_010_scale_331"


print("Load Voxel Grid");
bvpl_batch.init_process("bvxmLoadGridProcess");
bvpl_batch.set_input_string(0, data_dir +"/KL_gaussf1.vox");
bvpl_batch.set_input_string(1,"bsta_gauss_f1");
bvpl_batch.run_process();
(world_id,world_type)= bvpl_batch.commit_output(0);
world = dbvalue(world_id,world_type);


print("Creating corner 2d kernel");
bvpl_batch.init_process("bvplCreateCorner2dKernelProcess");
bvpl_batch.set_params_process(output_dir +"/corner2d_params.xml");
bvpl_batch.run_process();
(kernel_id,kernel_type)= bvpl_batch.commit_output(0);
kernel = dbvalue(kernel_id,kernel_type);

print("Running Operator");
bvpl_batch.init_process("bvplNeighborhoodOperatorProcess");
bvpl_batch.set_input_from_db(0,world );
bvpl_batch.set_input_from_db(1,kernel);
bvpl_batch.set_input_string(2,"bsta_gauss_f1");
bvpl_batch.set_input_string(3,"positive_gauss_convolution");
bvpl_batch.set_input_string(4, output_dir + "/KL_gaussf1_response.vox");
bvpl_batch.run_process();
(response_grid_id,response_grid_type)= bvpl_batch.commit_output(0);
response_grid = dbvalue(response_grid_id,response_grid_type);

print("Writing Response Grid");
bvpl_batch.init_process("bvxmSaveGridRawProcess");
bvpl_batch.set_input_from_db(0,response_grid);
bvpl_batch.set_input_string(1,output_dir + "/KL_gaussf1_response.raw");
bvpl_batch.run_process();


