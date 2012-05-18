# Author : Andrew Miller
# Modifications: Isabel Restrepo

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
parser.add_option("-d", "--device",   action="store", type="string", dest="device",   default="gpu1", help="specify gpu (gpu0, gpu1, etc)")
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

if options.std_file != "":
   saveout = sys.stdout   # save initial state of stdout
   print saveout
   print "STD_OUT is being redirected" 
   set_stdout(options.std_file)


#################################
#Initialize a GPU
#################################
print "Initializing DEVICE"

os.chdir(scene_root)
scene_path = os.getcwd() + "/" + SCENE_NAME
if not os.path.exists(scene_path):
  print "SCENE NOT FOUND! ", scene_path
  sys.exit(5)
scene = boxm2_scene_adaptor (scene_path, DEVICE);  

#################################
#refine
#################################

ncells = scene.refine();
if(ncells < 0) :
  print "Refined Failed, clearing cache and exiting:"
  scene.clear_cache();
  boxm2_batch.clear(); 
  sys.exit(1)

#################################
#write and clear cache before exiting    
#################################
scene.write_cache(); 
scene.clear_cache();
boxm2_batch.clear();

if options.std_file != "":
   reset_stdout();
   print "STD_OUT is being reset" 

print "Done"

sys.exit(0)

