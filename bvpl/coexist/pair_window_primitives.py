# Script pair window primitives
# Window primitives are defined as follows
#            ___  ____
# |        |    ||
# |___  ___|    ||
#
# Author : Isabel Restrepo
#8-31-2009

import bvpl_batch
import time
import os
import sys
#time.sleep(30);
bvpl_batch.register_processes();
bvpl_batch.register_datatypes();


class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string




pair_pairs = 1;
save_pairs_vrml = 0;
save_centers_vrml = 0;



data_dir = sys.argv[1];
output_dir = sys.argv[2];
directions = sys.argv[3];
num_corners = int(sys.argv[4]);

#directions = "main_corners"
#data_dir = "/Users/isa/Experiments/CapitolSFM/few_windows/ocp+app/main_corners_331/pair1"
#output_dir = "/Users/isa/Experiments/CapitolSFM/few_windows/ocp+app/main_corners_331/pair2"
#num_corners=4;


#directions = "main_plane"
#data_dir = "/Users/isa/Experiments/CapitolSFM/few_windows/ocp+app/main_plane_331/pair1"
#output_dir = "/Users/isa/Experiments/CapitolSFM/few_windows/ocp+app/main_plane_331/pair2"
#num_corners = 8;

#directions = "all_corners"
#data_dir = "/Users/isa/Experiments/CapitolSFM/few_windows/ocp+app/all_corners_331/pair1"
#output_dir = "/Users/isa/Experiments/CapitolSFM/few_windows/ocp+app/all_corners_331/pair2"
#num_corners = 104;#112;

opposite_angle = 180;

if not os.path.isdir( output_dir + "/"):
  os.mkdir( output_dir + "/");



print("Load Pair Grid");
bvpl_batch.init_process("bvplLoadPairGridProcess");
bvpl_batch.set_input_string(0, data_dir +"/pair_centers.vox");
bvpl_batch.run_process();
(id, type)= bvpl_batch.commit_output(0);
pair_grid = dbvalue(id, type);
	
	
if pair_pairs:

  print("Creating kernels to search for corners");
  bvpl_batch.init_process("bvplCreateWCKernelVectorProcess");
  bvpl_batch.set_input_int(0, 0);  #min length
  bvpl_batch.set_input_int(1, 5);   #max length
  bvpl_batch.set_input_int(2, -5);  #min width
  bvpl_batch.set_input_int(3, 0);   #max width
  bvpl_batch.set_input_int(4, -2);  #min thickness
  bvpl_batch.set_input_int(5, 2);   #max thickness
  bvpl_batch.set_input_string(6, directions);
  bvpl_batch.run_process();
  (kernel_id,kernel_type)= bvpl_batch.commit_output(0);
  wc_kernel_vector = dbvalue(kernel_id,kernel_type);

  print("Pairing Pairs");
  bvpl_batch.init_process("bvplFindPairsProcess");
  bvpl_batch.set_input_from_db(0,pair_grid );
  bvpl_batch.set_input_int(1, opposite_angle)
  bvpl_batch.set_input_from_db(2,wc_kernel_vector);
  bvpl_batch.set_input_string(3, output_dir + "/pair_centers.vox");
  bvpl_batch.run_process();
  (pairs_id,pairs_type)= bvpl_batch.commit_output(0);
  pairs = dbvalue(pairs_id,pairs_type);
  (pairs_id,pairs_type)= bvpl_batch.commit_output(1);
  pairs_grid = dbvalue(pairs_id,pairs_type);
  
  print("Extract Response");
  bvpl_batch.init_process("bvplPairToFloatProcess");
  bvpl_batch.set_input_from_db(0,pairs_grid);
  bvpl_batch.set_input_string(1, output_dir +"/pair_resp.vox");
  bvpl_batch.run_process();
  (id, type)= bvpl_batch.commit_output(0);
  float_grid = dbvalue(id, type);

  print("Writing Response Grid");
  bvpl_batch.init_process("bvxmSaveGridRawProcess");
  bvpl_batch.set_input_from_db(0,float_grid);
  bvpl_batch.set_input_string(1,output_dir + "/pair_resp.raw");
  bvpl_batch.run_process();
  
  
if save_centers_vrml :

  print("Converting ID to Hue ");
  bvpl_batch.init_process("bvplConvertPairToHueProcess");
  bvpl_batch.set_input_from_db(0,pairs_grid );
  bvpl_batch.set_input_from_db(1,wc_kernel_vector);
  bvpl_batch.set_input_string(2, output_dir + "/hue_centers.vox");
  bvpl_batch.set_input_string(3, output_dir + "/hue.svg");
  bvpl_batch.run_process();
  (hue_grid_id,hue_grid_type)= bvpl_batch.commit_output(0);
  centers_hue_grid = dbvalue(hue_grid_id,hue_grid_type);

  print("Writing Orientation Grid");
  bvpl_batch.init_process("bvxmSaveRGBAGridVrmlProcess");
  bvpl_batch.set_input_from_db(0,centers_hue_grid);
  bvpl_batch.set_input_float(1,0.0);
  bvpl_batch.set_input_string(2,output_dir + "/all_centers.wrl");
  bvpl_batch.run_process();
	
if save_pairs_vrml :

  hue = 0.0;
  
  print("Visualize pairs");
  bvpl_batch.init_process("bvplVisualizeCornerPairsProcess");
  bvpl_batch.set_input_from_db(0,pairs );
  bvpl_batch.set_input_unsigned(1,0);
  bvpl_batch.set_input_string(2,output_dir +   "/all_lines.wrl");
  bvpl_batch.set_input_bool(3, 1);
  bvpl_batch.set_input_float(4, hue);
  bvpl_batch.run_process();

  hue = hue + 1.0/float(num_corners);
    
  for i in range(1,int(num_corners),1):

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


