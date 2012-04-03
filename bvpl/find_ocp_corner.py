# Script to run find 2d corners on appearance grid
# Author : Isabel Restrepo
#8-31-2009

import bvpl_batch
import time
time.sleep(30);
bvpl_batch.register_processes();
bvpl_batch.register_datatypes();


class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

save_hue = 1;
data_dir = "c:/Experiments/object_recognition/bvpl/CapitolSiteHigh_sfm/front_wall"
output_dir = "c:/Experiments/object_recognition/bvpl/CapitolSiteHigh_sfm/front_wall/results/corner2d_ocp/0_90_180_270_plane_010_scale_221"
#param_dir = "c:/Projects/vxl/vxl/contrib/brl/contrib/lemsvxl/src/contrib/isabel/params"


print("Load Voxel Grid");
bvpl_batch.init_process("bvxmLoadGridProcess");
bvpl_batch.set_input_string(0, data_dir +"/ocp_cropped.vox");
bvpl_batch.set_input_string(1,"float");
bvpl_batch.run_process();
(world_id,world_type)= bvpl_batch.commit_output(0);
world = dbvalue(world_id,world_type);

print("Creating corner 2d kernel");
bvpl_batch.init_process("bvplCreateCorner2dKernelVectorProcess");
bvpl_batch.set_input_unsigned(0, 2);  #lhalf length
bvpl_batch.set_input_unsigned(1, 2);  #half width
bvpl_batch.set_input_unsigned(2, 1);  #half thickness
bvpl_batch.run_process();
(kernel_id,kernel_type)= bvpl_batch.commit_output(0);
kernel_vector = dbvalue(kernel_id,kernel_type);

print("Running Operator");
bvpl_batch.init_process("bvplVectorOperatorProcess");
bvpl_batch.set_input_from_db(0,world );
bvpl_batch.set_input_from_db(1,kernel_vector);
bvpl_batch.set_input_string(2,"float");
bvpl_batch.set_input_string(3,"edge_algebraic_mean");
bvpl_batch.set_input_string(4, output_dir + "/ocp_response_s221.vox");
bvpl_batch.set_input_string(5, output_dir + "/ocp_id_s221.vox");
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
  bvpl_batch.set_input_string(3, output_dir + "/hue_ocp_s221.vox");
  bvpl_batch.set_input_string(4, output_dir + "/hue_ocp_s221.svg");
  bvpl_batch.run_process();
  (hue_grid_id,hue_grid_type)= bvpl_batch.commit_output(0);
  hue_grid = dbvalue(hue_grid_id,hue_grid_type);

  print("Writing Orientation Grid");
  bvpl_batch.init_process("bvxmGridToImageStackProcess");
  bvpl_batch.set_input_from_db(0,hue_grid);
  bvpl_batch.set_input_string(1,"vnl_float_4");
  bvpl_batch.set_input_string(2,output_dir + "/hue_world/");
  bvpl_batch.run_process();
# print("Non-max suppression");
# bvpl_batch.init_process("bvplNonMaxSuppressionProcess");
# bvpl_batch.set_input_from_db(0,response_grid );
# bvpl_batch.set_input_from_db(1,id_grid);
# bvpl_batch.set_input_from_db(2,kernel_vector);
# bvpl_batch.set_input_string(3, output_dir + "/KL_gaussf1_response_non_max.vox");
# (non_max_id,non_max_type)= bvpl_batch.commit_output(0);
# non_max_grid = dbvalue(non_max_id,non_max_type);

print("Writing Response Grid");
bvpl_batch.init_process("bvxmSaveGridRawProcess");
bvpl_batch.set_input_from_db(0,response_grid);
bvpl_batch.set_input_string(1,output_dir + "/ocp_response_s221_0.raw");
bvpl_batch.set_input_string(2,"float");
bvpl_batch.run_process();


# print("Writing Non-Max Grid");
# bvpl_batch.init_process("bvxmSaveGridRawProcess");
# bvpl_batch.set_input_from_db(0,non_max_grid);
# bvpl_batch.set_input_string(1,output_dir + "/KL_gaussf1_response_non_max.raw");
# bvpl_batch.set_input_string(2,"float");
# bvpl_batch.run_process();

# print("Writing Response Grid");
# bvpl_batch.init_process("bvxmSaveGridRawProcess");
# bvpl_batch.set_input_from_db(0,id_grid);
# bvpl_batch.set_input_string(1,output_ dir + "/KL_gaussf1_id.raw");
# bvpl_batch.set_input_string(2,"unsigned");
# bvpl_batch.run_process();
