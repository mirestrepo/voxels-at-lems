# THIS IS /helicopter_providence/middletown_3_29_11/site2_planes/boxm2_1/boxm2_update_and_refine_scene.py
import boxm2_batch,os;
import sys;
import optparse;
import time;

#import matplotlib.pyplot as plt;
boxm2_batch.register_processes();
boxm2_batch.register_datatypes();

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string
    
import random

#Parse inputs
parser = optparse.OptionParser(description='Update BOXM2 Scene without refinement 0');

parser.add_option('--model_dir', action="store", dest="model_dir");
parser.add_option('--boxm2_dir', action="store", dest="boxm2_dir");
parser.add_option('--imgs_dir', action="store", dest="imgs_dir");
parser.add_option('--cams_dir', action="store", dest="cams_dir");
parser.add_option('--NI', action="store", dest="NI", type='int');
parser.add_option('--NJ', action="store", dest="NJ", type='int');
parser.add_option('--repeat', action="store", dest="repeat", type='int');


options, args = parser.parse_args()

model_dir = options.model_dir;
boxm2_dir = options.boxm2_dir;
imgs_dir = options.imgs_dir;
cams_dir = options.cams_dir;
NI = options.NI;
NJ = options.NJ
repeat = options.repeat;

if not os.path.isdir(boxm2_dir + '/'):
    print "Invalid Site Dir"
    sys.exit(-1);

if not os.path.isdir(imgs_dir):
    print "Invalid Image Dir"
    sys.exit(-1);
    
if not os.path.isdir(cams_dir):
    print "Invalid Cams Dir"
    sys.exit(-1);
    
expected_img_dir = boxm2_dir +  "/expectedImgs_" + str(repeat)
if not os.path.isdir(expected_img_dir + '/'):
    os.mkdir(expected_img_dir + '/');


print("Loading a Scene");
boxm2_batch.init_process("boxm2LoadSceneProcess");
boxm2_batch.set_input_string(0, boxm2_dir + "/scene.xml");
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
boxm2_batch.set_input_string(0,"gpu")
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


frames=[66,182,180,236,222,252,68,10,240,108,4,190,270,134,30,278,268,136,228,20,200,106,208,58,264,88,152,118,224,146,154,142,122,138,256,212,266,100,64,12,170,204,74,198,114,150,160,176,82,54,254,32,260,80,238,92,220,194,158,26,90,110,124,206,184,232,14,132,166,276,178,192,274,164,116,210,156,282,8,94,214,104,56,40,48,102,216,72,126,60,96,52,218,120,174,98,172,50,84,246,186,36,202,86,258,28,144,0,248,70,230,162,140,44,280,250,272,128,2,262,226,6,34,168,148,46,188,76,24,16,130,38,112,242,18,22,234];

test_frames=[244,196,62,78,42];
	
print 'STARTING UPDATE'

iter = 0;

for i in frames:
    
    print 'ITERATION %d' % iter
    iter = iter+1;
    camera_fname = cams_dir+"/camera%(#)05d.txt"%{"#":i}
    image_fname = imgs_dir+"/frames_%(#)05d.tif"%{"#":i}
	
    exp_fname= expected_img_dir+ "/frame_%(#)05d.tiff"%{"#":i};

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
    boxm2_batch.set_input_string(5,"");
    boxm2_batch.run_process(); 
 
    
    print("Render");
    boxm2_batch.init_process("boxm2OclRenderExpectedImageProcess");
    boxm2_batch.set_input_from_db(0,device);
    boxm2_batch.set_input_from_db(1,scene);
    boxm2_batch.set_input_from_db(2,openclcache);
    boxm2_batch.set_input_from_db(3,cam);
    boxm2_batch.set_input_unsigned(4,NI);
    boxm2_batch.set_input_unsigned(5,NJ);
    boxm2_batch.run_process();
    (id,type) = boxm2_batch.commit_output(0);
    exp_img = dbvalue(id,type);

    boxm2_batch.init_process("vilSaveImageViewProcess");
    boxm2_batch.set_input_from_db(0,exp_img);
    boxm2_batch.set_input_string(1,exp_fname);
    boxm2_batch.run_process();

    boxm2_batch.remove_data(exp_img.id)	


    boxm2_batch.remove_data(img.id)
    boxm2_batch.remove_data(cam.id)


 
nadir_cam_fname=cams_dir+ "/camera_nadir.txt"
for test_img_idx in test_frames :
	prediction_cam_fname= cams_dir+ "/camera_%(#)05d.txt"%{"#":test_img_idx};
 
	# Render the the predicted image
	boxm2_batch.init_process("vpglLoadPerspectiveCameraProcess"); 
	boxm2_batch.set_input_string(0,prediction_cam_fname);
	boxm2_batch.run_process();
	(id,type) = boxm2_batch.commit_output(0);
	prediction_cam = dbvalue(id,type);

	print("Render");
	boxm2_batch.init_process("boxm2OclRenderExpectedImageProcess");
	boxm2_batch.set_input_from_db(0,device);
	boxm2_batch.set_input_from_db(1,scene);
	boxm2_batch.set_input_from_db(2,openclcache);
	boxm2_batch.set_input_from_db(3,prediction_cam);
	boxm2_batch.set_input_unsigned(4,NI);
	boxm2_batch.set_input_unsigned(5,NJ);
	boxm2_batch.run_process();
	(id,type) = boxm2_batch.commit_output(0);
	exp_img = dbvalue(id,type);
	(id,type) = boxm2_batch.commit_output(1);
	vis_img = dbvalue(id,type);

	boxm2_batch.init_process("vilSaveImageViewProcess");
	boxm2_batch.set_input_from_db(0,exp_img);
	boxm2_batch.set_input_string(1,expected_img_dir+ "/predicted_img_%(#)05d.tiff"%{"#":test_img_idx});
	boxm2_batch.run_process();
	
	boxm2_batch.init_process("vilSaveImageViewProcess");
	boxm2_batch.set_input_from_db(0,vis_img);
	boxm2_batch.set_input_string(1,expected_img_dir+ "/predicted_img_mask_%(#)05d.tiff"%{"#":test_img_idx});
	boxm2_batch.run_process();

# Render the depth/variance image
boxm2_batch.init_process("vpglLoadPerspectiveCameraProcess"); 
boxm2_batch.set_input_string(0,nadir_cam_fname);
boxm2_batch.run_process();
(id,type) = boxm2_batch.commit_output(0);
nadir_cam = dbvalue(id,type);

boxm2_batch.init_process("boxm2OclRenderExpectedDepthProcess")
boxm2_batch.set_input_from_db(0,device);
boxm2_batch.set_input_from_db(1,scene);
boxm2_batch.set_input_from_db(2,openclcache);
boxm2_batch.set_input_from_db(3,nadir_cam);
boxm2_batch.set_input_unsigned(4,NI);
boxm2_batch.set_input_unsigned(5,NJ);
boxm2_batch.run_process();
(id,type) = boxm2_batch.commit_output(0);
exp_depth_img = dbvalue(id,type);
(id,type) = boxm2_batch.commit_output(1);
exp_var_img = dbvalue(id,type);

boxm2_batch.init_process("vilSaveImageViewProcess");
boxm2_batch.set_input_from_db(0, exp_depth_img);
boxm2_batch.set_input_string(1, expected_img_dir+ "/exepected_depth.tiff");
boxm2_batch.run_process();

boxm2_batch.init_process("vilSaveImageViewProcess");
boxm2_batch.set_input_from_db(0, exp_var_img);
boxm2_batch.set_input_string(1, expected_img_dir+ "/exepected_var.tiff");
boxm2_batch.run_process();

print("Write Main Cache");
boxm2_batch.init_process("boxm2WriteCacheProcess");
boxm2_batch.set_input_from_db(0,cache);
boxm2_batch.run_process(); 

boxm2_batch.clear()

