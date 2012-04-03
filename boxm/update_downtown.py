import boxm_batch;
import os;
import time;
boxm_batch.register_processes();
boxm_batch.register_datatypes();

#time.sleep(10);
class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string


# Capitol
model_dir = "/Users/isa/Experiments/DowntownBOXM_12_12_4";
model_imgs_dir = "/Users/isa/Experiments/DowntownBOXM_12_12_4/imgs"
around_imgs_dir = "/Users/isa/Experiments/DowntownBOXM_12_12_4/imgs360_%03d"

if not os.path.isdir( model_imgs_dir + "/"):
  os.mkdir( model_imgs_dir + "/");

image_fnames = "/Volumes/vision/video/dec/Downtown/video/frame_%05d.png";
camera_fnames = "/Volumes/vision/video/dec/Downtown/cameras_KRT/camera_%05d.txt";
expected_fname = model_imgs_dir + "/expected_%05d.tiff";
image_id_fname = model_imgs_dir + "/schedule.txt";
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


nframes =181;
import random;
schedule = [i for i in range(0,nframes)];
random.shuffle(schedule);
#schedule = [176, 158, 146, 174, 9, 96, 89, 40, 152, 41, 58, 51, 175, 125, 155, 42, 10, 75, 173, 34, 145, 135, 163, 6, 11, 104, 3, 121, 52, 102, 46, 60, 117, 93, 126, 67, 16, 166, 13, 107, 164, 38, 78, 33, 56, 100, 24, 43, 120, 27, 113, 84, 151, 165, 147, 71, 131, 109, 124, 141, 105, 21, 129, 112, 137, 87, 26, 128, 180, 68, 142, 47, 48, 77, 150, 50, 91, 161, 144, 83, 64, 140, 81, 36, 167, 72, 45, 98, 88, 85, 156, 39, 12, 103, 2, 55, 61, 148, 80, 157, 136, 70, 23, 92, 8, 73, 172, 111, 116, 177, 29, 178, 49, 14, 138, 1, 115, 94, 22, 20, 66, 35, 17, 160, 154, 132, 99, 31, 18, 28, 57, 133, 54, 32, 127, 171, 76, 79, 168, 122, 143, 90, 149, 62, 108, 170, 37, 101, 179, 82, 106, 114, 5, 110, 169, 97, 44, 25, 118, 95, 7, 19, 162, 119, 134, 159, 15, 59, 63, 123, 130, 65, 69, 86, 139, 0, 53, 153, 74, 4, 30];
bad_frames = [34, 49, 63, 76, 113, 118, 127, 148]
print "schedule is ", schedule;

# write schedule file
fd = open(image_id_fname,"w");
print >>fd, len(schedule);
print >>fd, schedule;
fd.close()


print schedule;

for x in range(0,len(schedule),1):
#for x in range(63,64,1):


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
      
      #refine only for first 140 images
      if(x < 140 ): 
        print("Refine Scene");
        boxm_batch.init_process("boxmRefineSceneProcess");
        boxm_batch.set_input_from_db(0,scene);
        boxm_batch.set_input_float(1,0.2);
        boxm_batch.set_input_bool(2,1);
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
      
    if(((x+1) % 50 == 0) or (x == 180)):
      temp_dir = around_imgs_dir % x;
      os.mkdir( temp_dir + "/");

      for j in range(0,nframes,8):

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
        boxm_batch.set_input_string(1, temp_dir + image_name);
        boxm_batch.run_process();
 

#print("Save Scene");
#boxm_batch.init_process("boxmSaveOccupancyRawProcess");
#boxm_batch.set_input_from_db(0,scene);
#boxm_batch.set_input_string(1,model_dir + "/sample_scene.raw");
#boxm_batch.set_input_unsigned(2,0);
#boxm_batch.set_input_unsigned(3,0);
#boxm_batch.run_process();

print("Save Scene");
boxm_batch.init_process("boxmSaveOccupancyRawProcess");
boxm_batch.set_input_from_db(0,scene);
boxm_batch.set_input_string(1,model_dir + "/all_sample_scene.raw");
boxm_batch.set_input_unsigned(2,0);
boxm_batch.set_input_unsigned(3,1);
boxm_batch.run_process();