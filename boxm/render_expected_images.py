import boxm_batch;
import os;
boxm_batch.register_processes();
boxm_batch.register_datatypes();

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string


# Capitol
model_dir = "/Users/isa/Experiments/CapitolBOXM";
model_imgs_dir = "/Users/isa/Experiments/CapitolBOXM/imgs360"
if not os.path.isdir( model_imgs_dir + "/"):
  os.mkdir( model_imgs_dir + "/");
camera_fnames = "/Volumes/vision/video/dec/capitol_sfm_rotated/cameras_KRT/camera_%05d.txt";
expected_fname = model_imgs_dir + "/expected_%05d.tiff";


print("Creating a Scene");
boxm_batch.init_process("boxmCreateSceneProcess");
boxm_batch.set_input_string(0,  model_dir +"/scene.xml");
boxm_batch.run_process();
(scene_id, scene_type) = boxm_batch.commit_output(0);
scene = dbvalue(scene_id, scene_type);

for i in range(0,255,8):

  print("Loading Camera");
  boxm_batch.init_process("vpglLoadPerspectiveCameraProcess");
  boxm_batch.set_input_string(0,camera_fnames % i);
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
  
  print("saving expected image");
  boxm_batch.init_process("vilSaveImageViewProcess");
  boxm_batch.set_input_from_db(0,expected);
  boxm_batch.set_input_string(1,expected_fname % i);
  boxm_batch.run_process();