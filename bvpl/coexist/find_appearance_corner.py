# Script to run find 2d corners on appearance grid
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
data_dir = "/Users/isa/Experiments/CapitolSiteHigh_sfm/few_windows"
output_dir = "/Users/isa/Experiments/CapitolSiteHigh_sfm/few_windows/corner2d_coexist/0+45-360_plane_010_scale_331"


print("Load Voxel Grid");
bvpl_batch.init_process("bvxmLoadGridProcess");
bvpl_batch.set_input_string(0, data_dir +"/KL_gaussf1.vox");
bvpl_batch.set_input_string(1,"bsta_gauss_f1");
bvpl_batch.run_process();
(world_id,world_type)= bvpl_batch.commit_output(0);
world = dbvalue(world_id,world_type);

print("Creating corner 2d kernel");
bvpl_batch.init_process("bvplCreateCorner2dKernelVectorProcess");
bvpl_batch.set_input_unsigned(0, 3);  #half length
bvpl_batch.set_input_unsigned(1, 3);  #half width
bvpl_batch.set_input_unsigned(2, 1);  #half thickness
bvpl_batch.run_process();
(kernel_id,kernel_type)= bvpl_batch.commit_output(0);
kernel_vector = dbvalue(kernel_id,kernel_type);


print("Running Kernels");
bvpl_batch.init_process("bvplSuppressAndCombineProcess");
bvpl_batch.set_input_from_db(0,world );
bvpl_batch.set_input_from_db(1,kernel_vector);
bvpl_batch.set_input_string(2,"bsta_gauss_f1");
bvpl_batch.set_input_string(3,"gauss_convolution");
bvpl_batch.set_input_string(4, output_dir + "/KL_gaussf1_response.vox");
bvpl_batch.set_input_string(5, output_dir + "/KL_gaussf1_id.vox");
bvpl_batch.run_process();
(all_resp_grid_id,all_resp_grid_type)= bvpl_batch.commit_output(0);
all_resp_grid = dbvalue(all_resp_grid_id,all_resp_grid_type);
(all_id_grid_id,all_id_grid_type)= bvpl_batch.commit_output(1);
all_id_grid = dbvalue(all_id_grid_id, all_id_grid_type);

print("Getting top response");
bvpl_batch.init_process("bvplExtractTopResponseProcess");
bvpl_batch.set_input_from_db(0,all_resp_grid );
bvpl_batch.set_input_from_db(1,all_id_grid);
bvpl_batch.set_input_unsigned(2,0);
bvpl_batch.set_input_string(3, output_dir + "/KL_top_response.vox");
bvpl_batch.set_input_string(4, output_dir + "/KL_top_id.vox");
bvpl_batch.run_process();
(response_grid_id,response_grid_type)= bvpl_batch.commit_output(0);
response_grid = dbvalue(response_grid_id,response_grid_type);
(id_grid_id,id_grid_type)= bvpl_batch.commit_output(1);
id_grid = dbvalue(id_grid_id,id_grid_type);


if save_hue :

  print("Converting ID to Hue ");
  bvpl_batch.init_process("bvplConvertIdToHueProcess");
  bvpl_batch.set_input_from_db(0,id_grid );
  bvpl_batch.set_input_from_db(1,response_grid );
  bvpl_batch.set_input_from_db(2,kernel_vector);
  bvpl_batch.set_input_string(3, output_dir + "/hue_KL_gaussf1.vox");
  bvpl_batch.set_input_string(4, output_dir + "/hue_KL_gaussf1.svg");
  bvpl_batch.run_process();
  (hue_grid_id,hue_grid_type)= bvpl_batch.commit_output(0);
  hue_grid = dbvalue(hue_grid_id,hue_grid_type);

  print("Writing Orientation Grid");
  bvpl_batch.init_process("bvxmGridToImageStackProcess");
  bvpl_batch.set_input_from_db(0,hue_grid);
  bvpl_batch.set_input_string(1,"vnl_float_4");
  bvpl_batch.set_input_string(2,output_dir + "/hue_world/");
  bvpl_batch.run_process();


print("Writing Response Grid");
bvpl_batch.init_process("bvxmSaveGridRawProcess");
bvpl_batch.set_input_from_db(0,response_grid);
bvpl_batch.set_input_string(1,output_dir + "/KL_gaussf1_response.raw");
bvpl_batch.run_process();


