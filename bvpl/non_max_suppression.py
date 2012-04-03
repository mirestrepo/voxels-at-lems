# Script to run find 2d corners on appearance grid
# Author : Isabel Restrepo
#8-31-2009

import bvpl_batch
import time

bvpl_batch.register_processes();
bvpl_batch.register_datatypes();


class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

visualize_all = 1;
non_max = 1;
data_dir =  "/Users/isa/Experiments/CapitolSiteHigh_sfm/few_windows/corner2d_apm/0+45-360_plane_010_scale_331"
output_dir = "/Users/isa/Experiments/CapitolSiteHigh_sfm/few_windows/corner2d_apm/0+45-360_plane_010_scale_331/non_max"

print("Creating corner 2d kernel");
bvpl_batch.init_process("bvplCreateCorner2dKernelVectorProcess");
bvpl_batch.set_input_unsigned(0, 3);  #half length
bvpl_batch.set_input_unsigned(1, 3);  #half width
bvpl_batch.set_input_unsigned(2, 1);  #half thickness
bvpl_batch.run_process();
(kernel_id,kernel_type)= bvpl_batch.commit_output(0);
kernel_vector = dbvalue(kernel_id,kernel_type);

#time.sleep(30);
print("Load Response Grid");
bvpl_batch.init_process("bvxmLoadGridProcess");
bvpl_batch.set_input_string(0, data_dir + "/KL_gaussf1_response.vox");
bvpl_batch.set_input_string(1,"bsta_gauss_f1");
bvpl_batch.run_process();
(response_grid_id,response_grid_type)= bvpl_batch.commit_output(0);
response_grid = dbvalue(response_grid_id,response_grid_type);

print("Load ID Grid");
bvpl_batch.init_process("bvxmLoadGridProcess");
bvpl_batch.set_input_string(0, data_dir + "/KL_gaussf1_id.vox");
bvpl_batch.set_input_string(1,"unsigned");
bvpl_batch.run_process();
(id_grid_id,id_grid_type)= bvpl_batch.commit_output(0);
id_grid = dbvalue(id_grid_id,id_grid_type);


if (non_max):
  print("Non-max suppression");
  bvpl_batch.init_process("bvplNonMaxSuppressionProcess");
  bvpl_batch.set_input_from_db(0,response_grid );
  bvpl_batch.set_input_from_db(1,id_grid);
  bvpl_batch.set_input_from_db(2,kernel_vector);
  bvpl_batch.set_input_string(3, output_dir + "/non_max.vox");
  bvpl_batch.run_process();
  (non_max_id,non_max_type)= bvpl_batch.commit_output(0);
  non_max_grid = dbvalue(non_max_id,non_max_type);

  # print("Writing Response Grid");
  # bvpl_batch.init_process("bvxmSaveGridRawProcess");
  # bvpl_batch.set_input_from_db(0,response_grid);
  # bvpl_batch.set_input_string(1,output_dir + "/KL_gaussf1_response.raw");
  # bvpl_batch.set_input_string(2,"float");
  # bvpl_batch.run_process();

  # print("Writing Non-Max Grid");
  # bvpl_batch.init_process("bvxmSaveGridRawProcess");
  # bvpl_batch.set_input_from_db(0,non_max_grid);
  # bvpl_batch.set_input_string(1,output_dir + "/KL_gaussf1_response_non_max.raw");
  # bvpl_batch.set_input_string(2,"float");
  # bvpl_batch.run_process();

  # print("Writing id Grid");
  # bvpl_batch.init_process("bvxmSaveGridRawProcess");
  # bvpl_batch.set_input_from_db(0,id_grid);
  # bvpl_batch.set_input_string(1,output_dir + "/KL_gaussf1_id.raw");
  # bvpl_batch.set_input_string(2,"unsigned");
  # bvpl_batch.run_process();

  if visualize_all :

    print("Converting ID to Hue ");
    bvpl_batch.init_process("bvplConvertIdToHueProcess");
    bvpl_batch.set_input_from_db(0,id_grid );
    bvpl_batch.set_input_from_db(1,non_max_grid );
    bvpl_batch.set_input_from_db(2,kernel_vector);
    bvpl_batch.set_input_string(3, output_dir + "/hue_kl_gauss.vox");
    bvpl_batch.set_input_string(4, output_dir + "/hue_kl_gauss.svg");
    bvpl_batch.run_process();
    (hue_grid_id,hue_grid_type)= bvpl_batch.commit_output(0);
    hue_grid = dbvalue(hue_grid_id,hue_grid_type);

    print("Writing Orientation Grid");
    bvpl_batch.init_process("bvxmGridToImageStackProcess");
    bvpl_batch.set_input_from_db(0,hue_grid);
    bvpl_batch.set_input_string(1,"vnl_float_4");
    bvpl_batch.set_input_string(2,output_dir + "/hue_world/");
    bvpl_batch.run_process();
    
  if (not (visualize_all)):

    bvpl_batch.init_process("bvplVisualizeResponseProcess");
    bvpl_batch.set_input_from_db(0,non_max_grid);
    bvpl_batch.set_input_from_db(1,id_grid);
    bvpl_batch.set_input_unsigned(2,0);
    bvpl_batch.set_input_string(3,output_dir + "/resp0.raw");
    bvpl_batch.run_process();

    bvpl_batch.init_process("bvplVisualizeResponseProcess");
    bvpl_batch.set_input_from_db(0,non_max_grid);
    bvpl_batch.set_input_from_db(1,id_grid);
    bvpl_batch.set_input_unsigned(2,1);
    bvpl_batch.set_input_string(3,output_dir + "/resp1.raw");
    bvpl_batch.run_process();


    bvpl_batch.init_process("bvplVisualizeResponseProcess");
    bvpl_batch.set_input_from_db(0,non_max_grid);
    bvpl_batch.set_input_from_db(1,id_grid);
    bvpl_batch.set_input_unsigned(2,2);
    bvpl_batch.set_input_string(3,output_dir + "/resp2.raw");
    bvpl_batch.run_process();
    
    bvpl_batch.init_process("bvplVisualizeResponseProcess");
    bvpl_batch.set_input_from_db(0,non_max_grid);
    bvpl_batch.set_input_from_db(1,id_grid);
    bvpl_batch.set_input_unsigned(2,3);
    bvpl_batch.set_input_string(3,output_dir + "/resp3.raw");
    bvpl_batch.run_process();
   
    bvpl_batch.init_process("bvplVisualizeResponseProcess");
    bvpl_batch.set_input_from_db(0,non_max_grid);
    bvpl_batch.set_input_from_db(1,id_grid);
    bvpl_batch.set_input_unsigned(2,4);
    bvpl_batch.set_input_string(3,output_dir + "/resp4.raw");
    bvpl_batch.run_process();

    bvpl_batch.init_process("bvplVisualizeResponseProcess");
    bvpl_batch.set_input_from_db(0,non_max_grid);
    bvpl_batch.set_input_from_db(1,id_grid);
    bvpl_batch.set_input_unsigned(2,5);
    bvpl_batch.set_input_string(3,output_dir + "/resp5.raw");
    bvpl_batch.run_process();

    bvpl_batch.init_process("bvplVisualizeResponseProcess");
    bvpl_batch.set_input_from_db(0,non_max_grid);
    bvpl_batch.set_input_from_db(1,id_grid);
    bvpl_batch.set_input_unsigned(2,6);
    bvpl_batch.set_input_string(3,output_dir + "/resp6.raw");
    bvpl_batch.run_process();
    
    bvpl_batch.init_process("bvplVisualizeResponseProcess");
    bvpl_batch.set_input_from_db(0,non_max_grid);
    bvpl_batch.set_input_from_db(1,id_grid);
    bvpl_batch.set_input_unsigned(2,7);
    bvpl_batch.set_input_string(3,output_dir + "/resp7.raw");
    bvpl_batch.run_process();
    
if (not(non_max)):

  output_dir = "/Users/isa/Experiments/CapitolSiteHigh_sfm/few_windows/corner2d_apm/0+45-360_plane_010_scale_331"
  if visualize_all :

    print("Converting ID to Hue ");
    bvpl_batch.init_process("bvplConvertIdToHueProcess");
    bvpl_batch.set_input_from_db(0,id_grid );
    bvpl_batch.set_input_from_db(1,response_grid );
    bvpl_batch.set_input_from_db(2,kernel_vector);
    bvpl_batch.set_input_string(3, output_dir + "/hue_kl_gauss.vox");
    bvpl_batch.set_input_string(4, output_dir + "/hue_kl_gauss.svg");
    bvpl_batch.run_process();
    (hue_grid_id,hue_grid_type)= bvpl_batch.commit_output(0);
    hue_grid = dbvalue(hue_grid_id,hue_grid_type);

    print("Writing Orientation Grid");
    bvpl_batch.init_process("bvxmGridToImageStackProcess");
    bvpl_batch.set_input_from_db(0,hue_grid);
    bvpl_batch.set_input_string(1,"vnl_float_4");
    bvpl_batch.set_input_string(2,output_dir + "/hue_world/");
    bvpl_batch.run_process();
    
  if (not (visualize_all)):

    bvpl_batch.init_process("bvplVisualizeResponseProcess");
    bvpl_batch.set_input_from_db(0,response_grid);
    bvpl_batch.set_input_from_db(1,id_grid);
    bvpl_batch.set_input_unsigned(2,0);
    bvpl_batch.set_input_string(3,output_dir + "/resp0.raw");
    bvpl_batch.run_process();

    bvpl_batch.init_process("bvplVisualizeResponseProcess");
    bvpl_batch.set_input_from_db(0,response_grid);
    bvpl_batch.set_input_from_db(1,id_grid);
    bvpl_batch.set_input_unsigned(2,1);
    bvpl_batch.set_input_string(3,output_dir + "/resp1.raw");
    bvpl_batch.run_process();


    bvpl_batch.init_process("bvplVisualizeResponseProcess");
    bvpl_batch.set_input_from_db(0,response_grid);
    bvpl_batch.set_input_from_db(1,id_grid);
    bvpl_batch.set_input_unsigned(2,2);
    bvpl_batch.set_input_string(3,output_dir + "/resp2.raw");
    bvpl_batch.run_process();
    
    bvpl_batch.init_process("bvplVisualizeResponseProcess");
    bvpl_batch.set_input_from_db(0,response_grid);
    bvpl_batch.set_input_from_db(1,id_grid);
    bvpl_batch.set_input_unsigned(2,3);
    bvpl_batch.set_input_string(3,output_dir + "/resp3.raw");
    bvpl_batch.run_process();
   
    bvpl_batch.init_process("bvplVisualizeResponseProcess");
    bvpl_batch.set_input_from_db(0,response_grid);
    bvpl_batch.set_input_from_db(1,id_grid);
    bvpl_batch.set_input_unsigned(2,4);
    bvpl_batch.set_input_string(3,output_dir + "/resp4.raw");
    bvpl_batch.run_process();

    bvpl_batch.init_process("bvplVisualizeResponseProcess");
    bvpl_batch.set_input_from_db(0,response_grid);
    bvpl_batch.set_input_from_db(1,id_grid);
    bvpl_batch.set_input_unsigned(2,5);
    bvpl_batch.set_input_string(3,output_dir + "/resp5.raw");
    bvpl_batch.run_process();

    bvpl_batch.init_process("bvplVisualizeResponseProcess");
    bvpl_batch.set_input_from_db(0,response_grid);
    bvpl_batch.set_input_from_db(1,id_grid);
    bvpl_batch.set_input_unsigned(2,6);
    bvpl_batch.set_input_string(3,output_dir + "/resp6.raw");
    bvpl_batch.run_process();
    
    bvpl_batch.init_process("bvplVisualizeResponseProcess");
    bvpl_batch.set_input_from_db(0,response_grid);
    bvpl_batch.set_input_from_db(1,id_grid);
    bvpl_batch.set_input_unsigned(2,7);
    bvpl_batch.set_input_string(3,output_dir + "/resp7.raw");
    bvpl_batch.run_process();