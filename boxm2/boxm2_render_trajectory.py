from boxm2_scene_adaptor import *; 
from vil_adaptor import *;
from vpgl_adaptor import *;
from bbas_adaptor import *
import random, os, sys;  
from optparse import OptionParser

####################################################### 
# handle inputs                                       #
# scene is given as first arg, figure out paths       #
####################################################### 

parser = OptionParser()
parser.add_option("-s", "--sceneroot", action="store", type="string", dest="sceneroot", help="root folder for this scene")
parser.add_option("-x", "--xmlfile", action="store", type="string", dest="xml", default="uscene.xml", help="scene.xml file name (model/uscene.xml, model_fixed/scene.xml, rscene.xml)")
parser.add_option("-g", "--gpu",   action="store", type="string", dest="gpu",   default="gpu1", help="specify gpu (gpu0, gpu1, etc)")
parser.add_option("-m", "--maxFrames", action="store", type="int", dest="maxFrames", default=500, help="max number of frames to render")
parser.add_option("-r", "--radius", action="store", type="float", dest="radius", default=1.0, help="distance from cam center to model center")

(options, args) = parser.parse_args()
print options
print args

# handle inputs
#scene is given as first arg, figure out paths
scene_root = options.sceneroot; 
SCENE_NAME = options.xml
GPU = options.gpu
MAX_FRAMES = options.maxFrames
NI=1280
NJ=720

#################################
#Initialize a GPU
#################################

print "Initializing GPU"

os.chdir(scene_root)
scene_path = os.getcwd() + "/" + SCENE_NAME
if not os.path.exists(scene_path):
  print "SCENE NOT FOUND! ", scene_path
  sys.exit(-1)
scene = boxm2_scene_adaptor (scene_path, GPU);  
(sceneMin, sceneMax) = scene.bounding_box(); 

#################################
#init trajectory 
#################################

startInc = 38.0; 
endInc = 38.0; 
radius   = max(options.radius, 1.4*(sceneMax[0]-sceneMin[0])); 
trajectory = init_trajectory(scene.scene, startInc, endInc, radius, NI, NJ);
trajDir = os.getcwd() + "/trajectory/"
if not os.path.exists(trajDir):
  os.mkdir(trajDir);

################# 
# UPDATE LOOP
#################
for x in range(0, MAX_FRAMES, 1):

  #render frame
  prcam = trajectory_next(trajectory); 
  expimg = render_grey(scene.scene, scene.active_cache, prcam, NI, NJ, scene.device);
  exp_fname = trajDir + "/exp_%(#)03d.tiff"%{"#":x};
  save_image(expimg, exp_fname); 

  #clean up
  remove_from_db([expimg, prcam])

#mencoder "mf://*.png" -mf fps=18 -o demo.avi -ovc lavc -lavcopts vcodec=msmpeg4v2:vbitrate=24000000

