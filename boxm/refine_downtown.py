#Created by Isabel Restrepo
#Updates boxm_model without refining

import boxm_batch;
import os;
boxm_batch.register_processes();
boxm_batch.register_datatypes();

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string


# Capitol
model_dir = "/Users/isa/Experiments/DowntownBOXM_4_4_1";
model_imgs_dir = "/Users/isa/Experiments/DowntownBOXM_4_4_1/imgs_refined"
around_imgs_dir = "/Users/isa/Experiments/DowntownBOXM_4_4_1/imgs360_refined"

if not os.path.isdir( model_imgs_dir + "/"):
  os.mkdir( model_imgs_dir + "/");

image_fnames = "/Volumes/vision/video/dec/Downtown/video/frame_%05d.png";
camera_fnames = "/Volumes/vision/video/dec/Downtown/cameras_KRT/camera_%05d.txt";
expected_fname = model_imgs_dir + "/expected_%05d.tiff";
image_id_fname = model_imgs_dir + "/schedule_refined.txt";
expected_fname_no_dir = "/expected_%05d.tiff"



print("Creating a Scene");
boxm_batch.init_process("boxmCreateSceneProcess");
boxm_batch.set_input_string(0,  model_dir +"/downtown_scene.xml");
boxm_batch.run_process();
(scene_id, scene_type) = boxm_batch.commit_output(0);
scene = dbvalue(scene_id, scene_type);

print("Loading Virtual Camera");
boxm_batch.init_process("vpglLoadPerspectiveCameraProcess");
boxm_batch.set_input_string(0,camera_fnames % 40);
boxm_batch.run_process();
(id,type) = boxm_batch.commit_output(0);
vcam = dbvalue(id,type);



import random;
schedule = [i for i in range(0,180,9)];
nframes =len(schedule);
#random.shuffle(schedule);

bad_frames = [34, 49, 63, 76, 113, 118, 127, 148]
print "schedule is ", schedule;

# write schedule file
fd = open(image_id_fname,"w");
print >>fd, len(schedule);
print >>fd, schedule;
fd.close()


print schedule;

for x in range(0,len(schedule),1):


  i = schedule[x];
  is_good_frame = 1;
  
  for b in range(0, len(bad_frames),1):
    if (bad_frames[b]== i):
      is_good_frame = 0;
      print ("Skiping frame: "); print(i);
      break;
 
  if(is_good_frame):
    print("Loading Camera");
    boxm_batch.init_process("vpglLoadPerspectiveCameraProcess");
    boxm_batch.set_input_string(0,camera_fnames % i);
    status = boxm_batch.run_process();
    (id,type) = boxm_batch.commit_output(0);
    cam = dbvalue(id,type);

    print("Loading Image");
    boxm_batch.init_process("vilLoadImageViewProcess");
    boxm_batch.set_input_string(0,image_fnames % i);
    status = status & boxm_batch.run_process();
    (id,type) = boxm_batch.commit_output(0);
    image = dbvalue(id,type);

    if(status):
      print("Updating Scene");
      boxm_batch.init_process("boxmUpdateRTProcess");
      boxm_batch.set_input_from_db(0,image);
      boxm_batch.set_input_from_db(1,cam);
      boxm_batch.set_input_from_db(2,scene);
      boxm_batch.set_input_unsigned(3,0);
      boxm_batch.set_input_bool(4, 0);
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
      boxm_batch.set_input_string(1,expected_fname % i);
      boxm_batch.run_process();
      
    

os.mkdir( around_imgs_dir + "/");

for j in range(0,180,10):

  print("Loading Camera");
  boxm_batch.init_process("vpglLoadPerspectiveCameraProcess");
  boxm_batch.set_input_string(0,camera_fnames % j);
  status = boxm_batch.run_process();
  (id,type) = boxm_batch.commit_output(0);
  cam = dbvalue(id,type);
  
   # Generate Expected Image 
  print("Generating Expected Image");
  boxm_batch.init_process("boxmRenderExpectedRTProcess");
  boxm_batch.set_input_from_db(0,scene);
  boxm_batch.set_input_from_db(1,cam); 
  boxm_batch.set_input_unsigned(2,1280);
  boxm_batch.set_input_unsigned(3,720);
  boxm_batch.set_input_bool(4,0);
  boxm_batch.run_process();
  (id,type) = boxm_batch.commit_output(0);
  expected = dbvalue(id,type);
  (id,type) = boxm_batch.commit_output(1);
  mask = dbvalue(id,type);
  

  image_name = expected_fname_no_dir % j
  
  print("saving expected image");
  boxm_batch.init_process("vilSaveImageViewProcess");
  boxm_batch.set_input_from_db(0,expected);
  boxm_batch.set_input_string(1, around_imgs_dir + image_name);
  boxm_batch.run_process();


print("Save Scene");
boxm_batch.init_process("boxmSaveOccupancyRawProcess");
boxm_batch.set_input_from_db(0,scene);
boxm_batch.set_input_string(1,model_dir + "/refined_scene.raw");
boxm_batch.set_input_unsigned(2,0);
boxm_batch.set_input_unsigned(3,1);
boxm_batch.run_process();