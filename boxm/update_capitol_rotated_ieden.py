import boxm_batch;
import os;
boxm_batch.register_processes();
boxm_batch.register_datatypes();

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string


# Capitol
model_dir = "/Users/isa/Experiments/CapitolBOXM_6_4_4";
model_imgs_dir = "/Users/isa/Experiments/CapitolBOXM_6_4_4/imgs"
around_imgs_dir = "/Users/isa/Experiments/CapitolBOXM_6_4_4/imgs360_%03d"

if not os.path.isdir( model_imgs_dir + "/"):
  os.mkdir( model_imgs_dir + "/");

image_fnames = "/Volumes/vision/video/dec/CapitolSiteHigh/video_grey/frame_%05d.png";
camera_fnames = "/Volumes/vision/video/dec/capitol_sfm_rotated/cameras_KRT/camera_%05d.txt";
expected_fname = model_imgs_dir + "/expected_%05d.tiff";
image_id_fname = model_imgs_dir + "/schedule2.txt";
expected_fname_no_dir = "/expected_%05d.tiff"

print("Creating a Scene");
boxm_batch.init_process("boxmCreateSceneProcess");
boxm_batch.set_input_string(0,  model_dir +"/capitol_scene.xml");
boxm_batch.run_process();
(scene_id, scene_type) = boxm_batch.commit_output(0);
scene = dbvalue(scene_id, scene_type);

print("Loading Virtual Camera");
boxm_batch.init_process("vpglLoadPerspectiveCameraProcess");
boxm_batch.set_input_string(0,camera_fnames % 40);
boxm_batch.run_process();
(id,type) = boxm_batch.commit_output(0);
vcam = dbvalue(id,type);


nframes =255;
#import random;
#schedule = [i for i in range(0,nframes)];
#random.shuffle(schedule);

schedule= [209, 164, 152, 246, 131, 175, 110, 250, 129, 35, 140, 93, 248, 108, 79, 46, 194, 141, 4, 212, 169, 220, 61, 199, 202, 5, 65, 24, 32, 193, 133, 157, 3, 180, 195, 25, 214, 118, 233, 92, 187, 144, 208, 182, 204, 47, 16, 254, 127, 98, 121, 251, 151, 112, 50, 190, 40, 139, 94, 160, 249, 168, 252, 31, 238, 83, 37, 147, 36, 96, 247, 244, 9, 192, 236, 52, 97, 107, 75, 34, 77, 78, 111, 99, 76, 184, 12, 1, 130, 186, 189, 167, 68, 128, 8, 242, 39, 73, 103, 179, 183, 231, 218, 88, 213, 116, 188, 17, 172, 113, 211, 109, 122, 62, 185, 221, 230, 154, 74, 89, 125, 219, 53, 29, 162, 217, 205, 66, 171, 235, 69, 163, 41, 159, 226, 63, 138, 173, 57, 124, 10, 161, 27, 33, 178, 44, 170, 201, 243, 43, 155, 149, 54, 30, 222, 123, 22, 150, 148, 198, 60, 196, 105, 48, 80, 95, 115, 87, 120, 104, 177, 42, 137, 101, 228, 49, 81, 85, 215, 18, 239, 191, 234, 210, 86, 156, 55, 56, 28, 72, 6, 135, 253, 26, 119, 227, 203, 84, 245, 23, 241, 207, 181, 19, 174, 197, 136, 143, 146, 106, 114, 51, 70, 142, 21, 223, 102, 229, 0, 134, 7, 15, 71, 58, 14, 158, 67, 2, 176, 126, 91, 232, 82, 237, 11, 145, 224, 100, 20, 200, 166, 132, 225, 13, 90, 206, 117, 64, 216, 153, 165, 240, 59];
print "schedule is ", schedule;

# write schedule file
fd = open(image_id_fname,"w");
print >>fd, len(schedule);
print >>fd, schedule;
fd.close()


print schedule;

for x in range(0,len(schedule),1):


  i = schedule[x];
 
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
    
  if(x % 50 == 0):
    temp_dir = around_imgs_dir % x;
    os.mkdir( temp_dir + "/");

    for j in range(0,255,8):

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
 

print("Save Scene");
boxm_batch.init_process("boxmSaveOccupancyRawProcess");
boxm_batch.set_input_from_db(0,scene);
boxm_batch.set_input_string(1,model_dir + "/sample_scene.raw");
boxm_batch.set_input_unsigned(2,0);
boxm_batch.set_input_unsigned(3,0);
boxm_batch.run_process();

print("Save Scene");
boxm_batch.init_process("boxmSaveOccupancyRawProcess");
boxm_batch.set_input_from_db(0,scene);
boxm_batch.set_input_string(1,model_dir + "/all_sample_scene.raw");
boxm_batch.set_input_unsigned(2,0);
boxm_batch.set_input_unsigned(3,1);
boxm_batch.run_process();