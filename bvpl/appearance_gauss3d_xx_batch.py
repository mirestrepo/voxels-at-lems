# Script to run a second derivative gaussian kernel  on a grid
# Author : Isabel Restrepo
# 6-14-2009

import bvpl_batch
import time
#time.sleep(30);
bvpl_batch.register_processes();
bvpl_batch.register_datatypes();


class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

data_dir = "c:/Experiments/object_recognition/bvpl/CapitolSiteHigh/cropped_world"
output_dir = "c:/Experiments/object_recognition/bvpl/CapitolSiteHigh/gauss_xx_kernel"
#param_dir = "c:/Projects/vxl/vxl/contrib/brl/contrib/lemsvxl/src/contrib/isabel/params"


print("Load Voxel Grid");
bvpl_batch.init_process("bvxmLoadGridProcess");
bvpl_batch.set_input_string(0, data_dir +"/KL_gaussf1_cropped.vox");
bvpl_batch.set_input_string(1,"bsta_gauss_f1");
bvpl_batch.run_process();
(world_id,world_type)= bvpl_batch.commit_output(0);
world = dbvalue(world_id,world_type);

print("Creating 3D edge kernel");
bvpl_batch.init_process("bvplCreateGauss3dXXKernelVectorProcess");
bvpl_batch.set_input_float(0, 1.5);  #Sigma1
bvpl_batch.set_input_float(1, 2);  #Sigma2 
bvpl_batch.set_input_float(2, 2);  #Sigma3
bvpl_batch.run_process();
(kernel_id,kernel_type)= bvpl_batch.commit_output(0);
kernel_vector = dbvalue(kernel_id,kernel_type);

print("Running Operator");
bvpl_batch.init_process("bvplVectorOperatorProcess");
bvpl_batch.set_input_from_db(0,world );
bvpl_batch.set_input_from_db(1,kernel_vector);
bvpl_batch.set_input_string(2,"bsta_gauss_f1");
bvpl_batch.set_input_string(3,"gauss_convolution");
bvpl_batch.set_input_string(4, output_dir + "/gauss_xx_response_c.vox");
bvpl_batch.set_input_string(5, output_dir + "/gauss_xx_orientations_c.vox");
bvpl_batch.run_process();
(response_grid_id,response_grid_type)= bvpl_batch.commit_output(0);
response_grid = dbvalue(response_grid_id,response_grid_type);
(orientation_grid_id,orientation_grid_type)= bvpl_batch.commit_output(1);
orientation_grid = dbvalue(orientation_grid_id,orientation_grid_type);

# print("Writing Response Grid");
# bvpl_batch.init_process("bvxmSaveGridRawProcess");
# bvpl_batch.set_input_from_db(0,response_grid);
# bvpl_batch.set_input_string(1,output_dir + "/gauss_xx_response.raw");
# bvpl_batch.set_input_string(2,"float");
# bvpl_batch.run_process();

print("Combine Crientation and Response Grids");
bvpl_batch.init_process("bvxmCombineGridsProcess");
bvpl_batch.set_input_from_db(0,orientation_grid );
bvpl_batch.set_input_from_db(1,response_grid );
bvpl_batch.set_input_string(2, output_dir + "/gauss_xx_response4d.vox");
bvpl_batch.run_process();
(temp_grid_id,temp_grid_type)= bvpl_batch.commit_output(0);
temp_grid = dbvalue(temp_grid_id,temp_grid_type);


print("Converting Directions to Hue ");
bvpl_batch.init_process("bvplConvertDirectionToHueProcess");
bvpl_batch.set_input_from_db(0,temp_grid );
bvpl_batch.set_input_from_db(1,kernel_vector);
bvpl_batch.set_input_string(2, output_dir + "/gauss_xx_hue_c.vox");
bvpl_batch.set_input_string(3, output_dir + "/gauss_xx_hue_c.svg");
bvpl_batch.run_process();
(hue_grid_id,hue_grid_type)= bvpl_batch.commit_output(0);
hue_grid = dbvalue(hue_grid_id,hue_grid_type);


print("Writing Orientation Grid");
bvpl_batch.init_process("bvxmGridToImageStackProcess");
bvpl_batch.set_input_from_db(0,hue_grid);
bvpl_batch.set_input_string(1,"vnl_vector_fixed_float_4");
bvpl_batch.set_input_string(2,output_dir + "/gauss_xx_hue_c");
bvpl_batch.run_process();


