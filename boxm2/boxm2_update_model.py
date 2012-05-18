 # Author : Andrew Miller
# Modifications: Isabel Restrepo
# Script to update a boxm2 scene

import random, os, sys;  
from boxm2_scene_adaptor import *; 
from vil_adaptor import *;
from vpgl_adaptor import *;
from bbas_adaptor import *;
from helpers import *;
from glob import glob
from optparse import OptionParser


####################################################### 
# handle inputs                                       #
#scene is given as first arg, figure out paths        #
parser = OptionParser()
parser.add_option("-s", "--sceneroot", action="store", type="string", dest="sceneroot", help="root folder for this scene")
parser.add_option("-x", "--xmlfile", action="store", type="string", dest="xml", default="uscene.xml", help="scene.xml file name (model/uscene.xml, model_fixed/scene.xml, rscene.xml)")
parser.add_option("-d", "--device",   action="store", type="string", dest="device",   default="gpu1", help="specify device (cpp, gpu0, gpu1, etc)")
parser.add_option("-c", "--clearApp", action="store_true", dest="clearApp", default=False, help="clear appearance model")
parser.add_option("-t", "--imtype", action="store", type="string", dest="itype", default="png", help="specify image type (tif, png, tiff, TIF)")
parser.add_option("-v", "--variance", action="store", type="float", dest="var", default="-1.0", help="Specify fixed mog3 variance, otherwise learn it")
parser.add_option("-n", "--skipFrame", action="store", type="int", dest="skip", default=1, help="Specify how many images to use in each pass (1=every, 2=every other...)")
parser.add_option("-i", "--initFrame", action="store", type="int", dest="initFrame", default=0, help="Specify the first frame to start ")
parser.add_option("-p", "--printFile" , action="store", type="string", dest="std_file", default="", help="if given, the std out is redirected to this file")

(options, args) = parser.parse_args()
print options
print args

# handle inputs
#scene is given as first arg, figure out paths
scene_root = options.sceneroot; 

# Set some update parameters
SCENE_NAME = options.xml
DEVICE = options.device
SKIP_FRAME = options.skip;
INIT_FRAME = options.initFrame;
CLEAR_APP=options.clearApp;

if options.std_file != "":
   saveout = sys.stdout   # save initial state of stdout
   print saveout
   print "STD_OUT is being redirected" 
   set_stdout(options.std_file)




#################################
#Initialize a DEVICE
print "Initializing Cache"

os.chdir(scene_root)
scene_path = os.getcwd() + "/" + SCENE_NAME
if not os.path.exists(scene_path):
  print "SCENE NOT FOUND! ", scene_path
  sys.exit(-1)
scene = boxm2_scene_adaptor (scene_path, DEVICE);  

#################################
# Get list of imgs and cams
train_imgs = os.getcwd() + "/imgs/*." + options.itype
train_cams = os.getcwd() + "/cams_krt/*.txt"
exp_imgs_dir = os.getcwd() + "/exp_imgs"

if not os.path.isdir(os.getcwd() + "/imgs/"):
   print "Expected image directory doesn't exist. \nPlease place images in: ! ", os.getcwd() + "/imgs/"
   sys.exit(5)

if not os.path.isdir(os.getcwd() + "/cams_krt/"):
   print "Expected camera directory doesn't exist. \nPlease place cameras in: ! ", os.getcwd() + "/cams_krt/"
   sys.exit(5)

if not os.path.isdir(exp_imgs_dir +"/"):
   os.mkdir(exp_imgs_dir + "/"); 
  
imgs = glob(train_imgs)
cams = glob(train_cams)
imgs.sort()
cams.sort() 
if len(imgs) != len(cams) :
  print "Error: CAMS NOT ONE TO ONE WITH IMAGES"
  print "CAMS: ", len(cams), "  IMGS: ", len(imgs)
  sys.exit(5);

#################################
#clear appearance model
if(INIT_FRAME == (SKIP_FRAME - 1) and CLEAR_APP) :
    print("Deleting Apperance....")   
    move_appearance( os.getcwd() + "/model/"); 


#update 
frames = range(INIT_FRAME,len(imgs)-1, SKIP_FRAME); 
print "Training with frames:"
print frames;

random.shuffle(frames); 
for idx, i in enumerate(frames):   
    
    print "Iteration ", idx, " of ", len(frames) , " on chunk " , INIT_FRAME
    
    #load image and camera
    pcam        = load_perspective_camera(cams[i]); 
    img, ni, nj = load_image (imgs[i]); 
    exp_fname= exp_imgs_dir + "/exp_img_%(#)05d.tiff"%{"#":i};
 
    
    #render and expected image
    if idx%10==9:
      #save an expected image
      exp_image = render_grey(scene.scene, scene.active_cache, pcam, ni, nj, scene.device);
      save_image(exp_image, exp_fname)
      remove_from_db([exp_image])
        
    #update scene
    status = scene.update(pcam, img, True, None, "",  options.var); 
    if(status == False) :
       print "Update Failed, clearing cache and exiting:"
       scene.clear_cache();
       boxm2_batch.clear();
       sys.exit(1);

    #clean up
    remove_from_db([img, pcam])


#write and clear cache before exiting    
scene.write_cache(); 
scene.clear_cache();
boxm2_batch.clear();

if options.std_file != "":
   reset_stdout();
   print "STD_OUT is being reset" 

print "Done"

sys.exit(0)

