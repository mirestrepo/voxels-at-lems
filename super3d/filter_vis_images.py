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
    
dir = "/Users/isa/Experiments/super3d/scene/expectedImgs_2"    
test_frames=[8, 112, 96, 208];
    
for frame in test_frames:
  boxm_batch.init_process("vilLoadImageViewProcess");
  boxm_batch.set_input_string(0,dir + "/predicted_img_mask_%(#)05d.tiff"%{"#":frame});
  boxm_batch.run_process();
  (id,type) = boxm_batch.commit_output(0);
  vis_img = dbvalue(id,type);


  boxm_batch.init_process("vilThresholdImageProcess");
  boxm_batch.set_input_from_db(0,vis_img);
  boxm_batch.set_input_float(1,0.99);
  boxm_batch.set_input_bool(2,True);
  boxm_batch.run_process();
  (id,type) = boxm_batch.commit_output(0);
  mask_img = dbvalue(id,type);

  boxm_batch.init_process("vilSaveImageViewProcess");
  boxm_batch.set_input_from_db(0,mask_img);
  boxm_batch.set_input_string(1,dir + "/binary_mask_%(#)05d.tiff"%{"#":frame});
  boxm_batch.run_process();

  boxm_batch.remove_data(vis_img.id)
  boxm_batch.remove_data(mask_img.id)