import boxm_batch;
import sys;
import optparse;
import os;
import glob;

#import matplotlib.pyplot as plt;
boxm_batch.register_processes();
boxm_batch.register_datatypes();

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string
    
#dir = "/Users/isa/Experiments/super3d/sr2_scene_sr2_images/expectedImgs_1" 

#dir = "/Users/isa/Experiments/super3d/sr2_3scene_sr2_images/expectedImgs_2" 

#dir = "/Users/isa/Experiments/super3d/scene_sr2_images/expectedImgs_2" 

#dir = "/Users/isa/Experiments/super3d/scene/expectedImgs_2" 

#dir = "/Volumes/vision/video/isabel/super3d/scili_experiment/normal_scene/expectedImgs_0"

dir = "/Users/isa/Experiments/super3d/scili_experiments_bicubic/sr2_scene_sr2_images/expectedImgs_0"
   
boxm_batch.init_process("vilLoadImageViewProcess");
boxm_batch.set_input_string(0,dir + "/exepected_var.tiff");
boxm_batch.run_process();
(id,type) = boxm_batch.commit_output(0);
var_img = dbvalue(id,type);

boxm_batch.init_process("vilImageMeanProcess");
boxm_batch.set_input_from_db(0,var_img);
boxm_batch.run_process();
(id,type) = boxm_batch.commit_output(0);
mean = dbvalue(id,type);
mean_val = boxm_batch.get_output_float(mean.id);
 
  
mean_file = dir + "/mean_var.txt"
f = open(mean_file, 'w');
f.write(str(mean_val));
f.close();