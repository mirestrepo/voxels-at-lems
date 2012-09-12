import boxm2_batch,os;
from glob import glob;

boxm2_batch.register_processes();
boxm2_batch.register_datatypes();

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string
import random
imgs_dir="/data/hemenways/imgs/";
cams_dir="/data/hemenways/cams_krt/";
imgs=os.listdir(imgs_dir);
cams=os.listdir(cams_dir);

print("Loading a Scene");
boxm2_batch.init_process("boxm2LoadSceneProcess");
boxm2_batch.set_input_string(0,"/data/hemenways/model/scene.xml");
boxm2_batch.run_process();
(scene_id, scene_type) = boxm2_batch.commit_output(0);
scene = dbvalue(scene_id, scene_type);

print("Create Main Cache");
boxm2_batch.init_process("boxm2CreateCacheProcess");
boxm2_batch.set_input_from_db(0,scene);
boxm2_batch.set_input_string(1,"lru");
boxm2_batch.run_process();
(id,type) = boxm2_batch.commit_output(0);
cache = dbvalue(id, type);

print("Init Manager");
boxm2_batch.init_process("boclInitManagerProcess");
boxm2_batch.run_process();
(id, type) = boxm2_batch.commit_output(0);
mgr = dbvalue(id, type);

print("Get Gpu Device");
boxm2_batch.init_process("boclGetDeviceProcess");
boxm2_batch.set_input_string(0,"cpu0")
boxm2_batch.set_input_from_db(1,mgr)
boxm2_batch.run_process();
(id, type) = boxm2_batch.commit_output(0);
device = dbvalue(id, type);

print("Create Gpu Cache");
boxm2_batch.init_process("boxm2CreateOpenclCacheProcess");
boxm2_batch.set_input_from_db(0,device)
boxm2_batch.set_input_from_db(1,scene)
boxm2_batch.run_process();
(id, type) = boxm2_batch.commit_output(0);
openclcache = dbvalue(id, type);



# Get list of imgs and cams
train_imgs = imgs_dir + "*.png"
train_cams = cams_dir + "*.txt"
exp_imgs_dir = os.getcwd() + "/exp_imgs"

if not os.path.isdir(exp_imgs_dir +"/"):
   os.mkdir(exp_imgs_dir + "/"); 
  

imgs = glob(train_imgs)
cams = glob(train_cams)
imgs.sort()
cams.sort()
if len(imgs) != len(cams) :
  print "CAMS NOT ONE TO ONE WITH IMAGES"
  print "CAMS: ", len(cams), "  IMGS: ", len(imgs)
  sys.exit();

for x in range(0,len(cams)):
	i = random.randint(0,len(cams)-1);

	camera_fname = cams[i];
	image_fname = imgs[i];
  
	exp_fname="./frame_%(#)05d.tiff"%{"#":i};

	boxm2_batch.init_process("vpglLoadPerspectiveCameraProcess"); 
	boxm2_batch.set_input_string(0,camera_fname);
	boxm2_batch.run_process();
	(id,type) = boxm2_batch.commit_output(0);
	cam = dbvalue(id,type);
	
	boxm2_batch.init_process("vilLoadImageViewProcess");
	boxm2_batch.set_input_string(0,image_fname);
	boxm2_batch.run_process();
	(id,type) = boxm2_batch.commit_output(0);
	img = dbvalue(id,type);
	
	print("Update");
	boxm2_batch.init_process("boxm2OclUpdateProcess");
	boxm2_batch.set_input_from_db(0,device);
	boxm2_batch.set_input_from_db(1,scene);
	boxm2_batch.set_input_from_db(2,openclcache);
	boxm2_batch.set_input_from_db(3,cam);
	boxm2_batch.set_input_from_db(4,img);
	boxm2_batch.run_process();
	print("Refine");
	boxm2_batch.init_process("boxm2OclRefineProcess");
	boxm2_batch.set_input_from_db(0,device);
	boxm2_batch.set_input_from_db(1,scene);
	boxm2_batch.set_input_from_db(2,openclcache);
	boxm2_batch.set_input_float(3,0.3);
	boxm2_batch.run_process();

	print("Render");
	boxm2_batch.init_process("boxm2OclRenderExpectedImageProcess");
	boxm2_batch.set_input_from_db(0,device);
	boxm2_batch.set_input_from_db(1,scene);
	boxm2_batch.set_input_from_db(2,openclcache);
	boxm2_batch.set_input_from_db(3,cam);
	boxm2_batch.set_input_unsigned(4,1280);
	boxm2_batch.set_input_unsigned(5,720);
	boxm2_batch.run_process();
	(id,type) = boxm2_batch.commit_output(0);
	exp_img = dbvalue(id,type);
	
	boxm2_batch.init_process("vilSaveImageViewProcess");
	boxm2_batch.set_input_from_db(0,exp_img);
	boxm2_batch.set_input_string(1,exp_fname);
	boxm2_batch.run_process();


