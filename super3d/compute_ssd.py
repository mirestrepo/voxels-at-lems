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
#original_img_dir = "/Users/isa/Experiments/super3d/sr2_needed_grey"   

#dir = "/Users/isa/Experiments/super3d/sr2_3scene_sr2_images/expectedImgs_2" 
#original_img_dir = "/Users/isa/Experiments/super3d/sr2_needed_grey" 
#
#dir = "/Users/isa/Experiments/super3d/scene_sr2_images/expectedImgs_2" 
#original_img_dir = "/Users/isa/Experiments/super3d/sr2_needed_grey"     
#
#dir = "/Users/isa/Experiments/super3d/scene/expectedImgs_2" 
#original_img_dir = "/Users/isa/Experiments/super3d/frames_grey"   

#dir = "/Volumes/vision/video/isabel/super3d/scili_experiment/sr2_scene_sr2_images/expectedImgs_0"
#original_img_dir = "/Volumes/vision/video/isabel/super3d/site12_superres"

#dir = "/Volumes/vision/video/isabel/super3d/scili_experiment/normal_scene/expectedImgs_0"
#original_img_dir ="/Volumes/vision/video/helicopter_providence/3d_models_3_11/site12/frames_grey"

dir = "/Users/isa/Experiments/super3d/scili_experiments_bicubic/sr2_scene_sr2_images/expectedImgs_0"
original_img_dir = "/Users/isa/Experiments/super3d/scili_experiments_bicubic/superresolved_imgs"
npixels = 720*1280*4
test_frames=[78, 196, 244, 42];
ssd_vals=[];
ssd_avg = 0;    
    
for frame in test_frames:
  boxm_batch.init_process("vilLoadImageViewProcess");
  boxm_batch.set_input_string(0,dir + "/predicted_img_%(#)05d.tiff"%{"#":frame});
  boxm_batch.run_process();
  (id,type) = boxm_batch.commit_output(0);
  pred_img = dbvalue(id,type);

  boxm_batch.init_process("vilConvertPixelTypeProcess");
  boxm_batch.set_input_from_db(0,pred_img);
  boxm_batch.set_input_string(1, "byte");
  boxm_batch.run_process();
  (id,type) = boxm_batch.commit_output(0);
  pred_img_byte = dbvalue(id,type);
  
  boxm_batch.init_process("vilSaveImageViewProcess");
  boxm_batch.set_input_from_db(0,pred_img_byte);
  boxm_batch.set_input_string(1,dir + "/predicted_img_%(#)05d.png"%{"#":frame});
  boxm_batch.run_process();

  

  boxm_batch.init_process("vilLoadImageViewProcess");
  boxm_batch.set_input_string(0,original_img_dir + "/frames_%(#)05d.tif"%{"#":frame});
  boxm_batch.run_process();
  (id,type) = boxm_batch.commit_output(0);
  true_img = dbvalue(id,type);

  boxm_batch.init_process("vilImageSSDProcess");
  boxm_batch.set_input_from_db(0,pred_img_byte);
  boxm_batch.set_input_from_db(1,true_img);
  boxm_batch.run_process();
  (id,type) = boxm_batch.commit_output(0);
  ssd = dbvalue(id,type);
  ssd_val = boxm_batch.get_output_float(ssd.id);
  
  ssd_vals.append(ssd_val);
  ssd_avg = ssd_avg + ssd_val;
  
  boxm_batch.remove_data(pred_img.id)
  boxm_batch.remove_data(true_img.id)
  
  
ssd_file = dir + "/ssd.txt"
f = open(ssd_file, 'w');
f.write(str(ssd_vals));
f.write("\n");
f.write(str(ssd_avg/(npixels*len(test_frames))));
f.close();