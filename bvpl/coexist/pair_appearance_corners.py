# Script to run find 2d corners on appearance grid
# Author : Isabel Restrepo
#8-31-2009

import bvpl_batch
import time
import os
#time.sleep(30);
bvpl_batch.register_processes();
bvpl_batch.register_datatypes();


class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

find_corners = 1;
pair_corners = 1;
save_corners_vrml = 1;
save_pairs_vrml = 1;
data_dir = "/Users/isa/Experiments/CapitolSFM/few_windows"



corner_length = 3;
corner_width = 3;
corner_thickness =1;


directions = "main_corners"
output_dir = "/Users/isa/Experiments/CapitolSFM/few_windows/corner2d_coexist/main_corners_331_n"
num_corners=4;


#directions = "main_plane"
#output_dir = "/Users/isa/Experiments/CapitolSFM/few_windows/corner2d_coexist/main_plane_331"
#num_corners = 8;

#directions = "all_corners"
#output_dir = "/Users/isa/Experiments/CapitolSFM/few_windows/corner2d_coexist/all_corners_331"
#num_corners = 104;#112;

if not os.path.isdir( output_dir + "/"):
  os.mkdir( output_dir + "/");

if (find_corners):

  print("Load Voxel Grid");
  bvpl_batch.init_process("bvxmLoadGridProcess");
  bvpl_batch.set_input_string(0, data_dir +"/KL_gaussf1.vox");
  bvpl_batch.set_input_string(1,"bsta_gauss_f1");
  bvpl_batch.run_process();
  (world_id,world_type)= bvpl_batch.commit_output(0);
  app_grid = dbvalue(world_id,world_type);

  print("Creating corner 2d kernel");
  bvpl_batch.init_process("bvplCreateCorner2dKernelVectorProcess");
  bvpl_batch.set_input_unsigned(0, corner_length);  #half length
  bvpl_batch.set_input_unsigned(1, corner_width);  #half width
  bvpl_batch.set_input_unsigned(2, corner_thickness);  #half thickness
  bvpl_batch.set_input_string(3, directions);
  bvpl_batch.run_process();
  (kernel_id,kernel_type)= bvpl_batch.commit_output(0);
  corners_kernel_vector = dbvalue(kernel_id,kernel_type);

  print("Running Kernels");
  bvpl_batch.init_process("bvplSuppressAndCombineProcess");
  bvpl_batch.set_input_from_db(0,app_grid );
  bvpl_batch.set_input_from_db(1,corners_kernel_vector);
  bvpl_batch.set_input_string(2,"bsta_gauss_f1");
  bvpl_batch.set_input_string(3,"negative_gauss_convolution");
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
  bvpl_batch.set_input_string(3, output_dir + "/KL_top_resp.vox");
  bvpl_batch.set_input_string(4, output_dir + "/KL_top_id.vox");
  bvpl_batch.run_process();
  (response_grid_id,response_grid_type)= bvpl_batch.commit_output(0);
  response_grid = dbvalue(response_grid_id,response_grid_type);
  (id_grid_id,id_grid_type)= bvpl_batch.commit_output(1);
  id_grid = dbvalue(id_grid_id,id_grid_type);


if pair_corners:

  print("Creating kernels to search for corners");
  bvpl_batch.init_process("bvplCreateWCKernelVectorProcess");
  bvpl_batch.set_input_unsigned(0, 3);  #half length
  bvpl_batch.set_input_unsigned(1, 4);  #half width
  bvpl_batch.set_input_unsigned(2, 2);  #half thickness
  bvpl_batch.set_input_string(3, directions);
  bvpl_batch.run_process();
  (kernel_id,kernel_type)= bvpl_batch.commit_output(0);
  wc_kernel_vector = dbvalue(kernel_id,kernel_type);

  print("Searching for corners");
  bvpl_batch.init_process("bvplFindCornerPairsProcess");
  bvpl_batch.set_input_from_db(0,id_grid );
  bvpl_batch.set_input_from_db(1,response_grid );
  bvpl_batch.set_input_from_db(2,wc_kernel_vector);
  bvpl_batch.set_input_from_db(3,corners_kernel_vector);
  bvpl_batch.run_process();
  (pairs_id,pairs_type)= bvpl_batch.commit_output(0);
  pairs = dbvalue(pairs_id,pairs_type);
	
if save_corners_vrml :

  print("Converting ID to Hue ");
  bvpl_batch.init_process("bvplConvertIdToHueProcess");
  bvpl_batch.set_input_from_db(0,id_grid );
  bvpl_batch.set_input_from_db(1,response_grid );
  bvpl_batch.set_input_from_db(2,corners_kernel_vector);
  bvpl_batch.set_input_string(3, output_dir + "/hue_KL.vox");
  bvpl_batch.set_input_string(4, output_dir + "/hue_KL.svg");
  bvpl_batch.run_process();
  (hue_grid_id,hue_grid_type)= bvpl_batch.commit_output(0);
  hue_grid = dbvalue(hue_grid_id,hue_grid_type);

  print("Writing Orientation Grid");
  bvpl_batch.init_process("bvxmSaveRGBAGridVrmlProcess");
  bvpl_batch.set_input_from_db(0,hue_grid);
  bvpl_batch.set_input_float(1,0.0);
  bvpl_batch.set_input_string(2,output_dir + "/all_lines.wrl");
  bvpl_batch.run_process();
	
if save_pairs_vrml :

  hue = 0.125;
    
  for i in range(0,num_corners,1):

    print(i);
    
    print("Visualize pairs");
    bvpl_batch.init_process("bvplVisualizeCornerPairsProcess");
    bvpl_batch.set_input_from_db(0,pairs );
    bvpl_batch.set_input_unsigned(1,i);
    bvpl_batch.set_input_string(2,output_dir +   "/all_lines.wrl");
    bvpl_batch.set_input_bool(3, 0);
    bvpl_batch.set_input_float(4, hue);
    bvpl_batch.run_process();
    
    hue = hue + 1.0/float(num_corners);

print("Writing Response Grid");
bvpl_batch.init_process("bvxmSaveGridRawProcess");
bvpl_batch.set_input_from_db(0,response_grid);
bvpl_batch.set_input_string(1,output_dir + "/KL_resp.raw");
bvpl_batch.run_process();


