################################################################################
## Created by Isabel Restrepo                                                  
## March 1st, 2011                                                       
## Desciption: Render and expected image from top-down view                            
## LEMS, Brown University                                                     
## Last Updated:
################################################################################
import boxm_batch;
import os;
import time;
boxm_batch.register_processes();
boxm_batch.register_datatypes();

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string


# Capitol
#model_dir = "/Users/isa/Experiments/CapitolBOXM_6_4_4";
model_dir = "/Users/isa/Experiments/DowntownBOXM_3_3_1";
output_dir = model_dir;

#if not os.path.isdir( model_imgs_dir + "/"):
#  os.mkdir( model_imgs_dir + "/");

#camera_fname = "/Volumes/vision/video/dec/capitol_sfm_rotated/camera_top.txt";
camera_fname = "/Users/isa/Experiments/DowntownBOXM_3_3_1/camera_top.txt"
#camera_fname = "/Volumes/vision/video/dec/capitol_sfm_rotated/cameras_KRT/camera_00075.txt";
expected_fname = output_dir + "/expected_top.tiff";


print("Creating a Scene");
boxm_batch.init_process("boxmCreateSceneProcess");
boxm_batch.set_input_string(0,  model_dir +"/downtown_scene.xml");
boxm_batch.run_process();
(scene_id, scene_type) = boxm_batch.commit_output(0);
scene = dbvalue(scene_id, scene_type);

print("Loading Top Camera");
boxm_batch.init_process("vpglLoadPerspectiveCameraProcess");
boxm_batch.set_input_string(0,camera_fname);
boxm_batch.run_process();
(id,type) = boxm_batch.commit_output(0);
top_cam = dbvalue(id,type);


# Generate Expected Image 
print("Generating Expected Image");
boxm_batch.init_process("boxmRenderExpectedRTProcess");
boxm_batch.set_input_from_db(0,scene);
boxm_batch.set_input_from_db(1,top_cam); 
boxm_batch.set_input_unsigned(2,1280);
boxm_batch.set_input_unsigned(3,720);
boxm_batch.set_input_bool(4,0);   #black background
boxm_batch.run_process();
(id,type) = boxm_batch.commit_output(0);
expected = dbvalue(id,type);
(id,type) = boxm_batch.commit_output(1);
mask = dbvalue(id,type);
      
print("saving expected image");
boxm_batch.init_process("vilSaveImageViewProcess");
boxm_batch.set_input_from_db(0,expected);
boxm_batch.set_input_string(1,expected_fname);
boxm_batch.run_process();
      