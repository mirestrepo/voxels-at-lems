################################################################################
## Created by Gamze Tunali                                                   
## October 2, 2009                                                        
## Desciption: Updates Capitol Scene in batch mode                            
## LEMS, Brown University                                                     
## Last Updated:
## Jan 8, 2009  -Isabel Restrepo
################################################################################

import boxm_batch
import os
boxm_batch.register_processes();
boxm_batch.register_datatypes();


do_init = 1;
do_refine = 1;
num_its = 35;

refine_prob = 0.2;
damping_factor = 0.75;


# Capitol rotated (aligned with x-axis) and Cameras obtained from structure from motion algorithm
model_dir = "/Users/isa/Experiments/CapitolBOXM";
if not os.path.isdir( model_dir + "/"):
  os.mkdir( model_dir + "/");
  
model_imgs_dir = "/Users/isa/Experiments/CapitolBOXM/imgs"
if not os.path.isdir( model_imgs_dir + "/"):
  os.mkdir( model_imgs_dir + "/");
  
image_fname = "/Volumes/vision/video/dec/CapitolSiteHigh/video_grey/frame_%05d.png";
camera_fname = "/Volumes/vision/video/dec/capitol_sfm_rotated/cameras_KRT/camera_%05d.txt";
expected_fname = model_imgs_dir + "/expected_%05d.tiff";
image_id_fname = model_dir + "/image_list.txt";
camera_idx = range(0,100,10);
raw_fname = model_dir + "/Capitol%d";

class dbvalue:
  def __init__(self, index, type):
    self.id = index
    self.type = type


# write camera indices to file
image_ids = [];
fd = open(image_id_fname,"w");
print >>fd, len(camera_idx);
for c in camera_idx:
  img_id = "gray%d" % c;
  image_ids.append(img_id);
  print >>fd, img_id;
fd.close();

# load scene 
print("Creating a Scene");
boxm_batch.init_process("boxmCreateSceneProcess");
boxm_batch.set_input_string(0,  model_dir +"/scene.xml");
boxm_batch.run_process();
(scene_id, scene_type) = boxm_batch.commit_output(0);
scene = dbvalue(scene_id, scene_type);

print("Loading Virtual Camera");
boxm_batch.init_process("vpglLoadPerspectiveCameraProcess");
boxm_batch.set_input_string(0,camera_fname % 0);
boxm_batch.run_process();
(id,type) = boxm_batch.commit_output(0);
vcam = dbvalue(id,type);
vcam = dbvalue(id,type);

for it in range(0,num_its,1):
  for c in range(0,len(camera_idx),1):
    
    print("Loading Camera");
    boxm_batch.init_process("vpglLoadPerspectiveCameraProcess");
    boxm_batch.set_input_string(0,camera_fname % camera_idx[c]);
    boxm_batch.run_process();
    (id,type) = boxm_batch.commit_output(0);
    cam = dbvalue(id,type);
    
    print("Loading Image");
    boxm_batch.init_process("vilLoadImageViewProcess");
    boxm_batch.set_input_string(0,image_fname % camera_idx[c]);
    boxm_batch.run_process();
    (id,type) = boxm_batch.commit_output(0);
    image = dbvalue(id,type);
    
    print "Generating opt_samples for camera ", camera_idx[c];
    boxm_batch.init_process("boxmGenerateOptSamplesProcess");
    boxm_batch.set_input_from_db(0,image);
    boxm_batch.set_input_from_db(1,cam);
    boxm_batch.set_input_from_db(2,scene);
    boxm_batch.set_input_string(3,image_ids[c]);
    boxm_batch.set_input_bool(4,0);
    boxm_batch.run_process();

  # Do the optimization
  boxm_batch.init_process("boxmOptBayesianUpdateProcess");
  boxm_batch.set_input_from_db(0,scene);
  boxm_batch.set_input_float(1,damping_factor);
  boxm_batch.set_input_string(2,image_id_fname);
  boxm_batch.run_process();
  
  # Generate Expected Image 
  print("Generating Expected Image");
  boxm_batch.init_process("boxmRenderExpectedRTProcess");
  boxm_batch.set_input_from_db(0,scene);
  boxm_batch.set_input_from_db(1,vcam); 
  boxm_batch.set_input_unsigned(2,1280);
  boxm_batch.set_input_unsigned(3,720);
  boxm_batch.set_input_bool(4,0);
  boxm_batch.run_process();
  (id,type) = boxm_batch.commit_output(0);
  expected = dbvalue(id,type);
  (id,type) = boxm_batch.commit_output(1);
  mask = dbvalue(id,type);
  
  print("saving expected image");
  boxm_batch.init_process("vilSaveImageViewProcess");
  boxm_batch.set_input_from_db(0,expected);
  boxm_batch.set_input_string(1,expected_fname % it);
  boxm_batch.run_process();

  boxm_batch.remove_data(expected.id);
  boxm_batch.remove_data(mask.id);
    
  if ( (do_refine) & (it+1 < num_its) ):    
    print("Refining Scene");
    boxm_batch.init_process("boxmRefineSceneProcess");
    boxm_batch.set_input_from_db(0,scene);
    boxm_batch.set_input_float(1,refine_prob);
    boxm_batch.set_input_bool(2,False);
    boxm_batch.run_process();
  
  boxm_batch.remove_data(cam.id);
  boxm_batch.remove_data(image.id);

  print("Save Scene");
  boxm_batch.init_process("boxmSaveOccupancyRawProcess");
  boxm_batch.set_input_from_db(0,scene);
  boxm_batch.set_input_string(1,raw_fname % it);
  boxm_batch.set_input_unsigned(2,0);
  boxm_batch.set_input_unsigned(3,1);
  boxm_batch.run_process();

boxm_batch.remove_data(scene.id);

# switch processes to make sure scene destructor is called
boxm_batch.init_process("vilLoadImageViewProcess");

print("Done.");
