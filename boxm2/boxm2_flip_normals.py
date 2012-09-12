#!/usr/bin/env python
# encoding: utf-8
#################################################################################### 
# Author: Isabel Restrepo
# Computes the normals for a boxm2 scene using gaussian derivatives. 
# Surface normals are oriented according to the hemisphere of greater visibility
#################################################################################### 


import random, os, sys, time;  
from boxm2_scene_adaptor import *; 
from bbas_adaptor import *;
from boxm2_filtering_adaptor import *;
from glob import glob
from optparse import OptionParser


####################################################### 
# handle inputs                                       #
####################################################### 
parser = OptionParser()
parser.add_option("-s", "--sceneroot", action="store", type="string", dest="sceneroot", help="root folder for this scene")
parser.add_option("-x", "--xmlfile", action="store", type="string", dest="xml", default="uscene.xml", help="scene.xml file name (model/uscene.xml, model_fixed/scene.xml, rscene.xml)")
parser.add_option("-g", "--gpu",   action="store", type="string", dest="gpu",   default="gpu1", help="specify gpu (gpu0, gpu1, etc)")
parser.add_option("-p", "--printFile" , action="store", type="string", dest="std_file", default="", help="if given, the std out is redirected to this file")
parser.add_option("--use_sum",action="store_true", dest="use_sum", default=False, help="use (and store) sum of visibility to flip normals, instead of using max")

(opts, args) = parser.parse_args()

print "This is boxm2_compute_gauss_gradients.py. With arguments"
print opts
print args

# handle inputs
scene_root = opts.sceneroot; 

# Set some update parameters
SCENE_NAME = opts.xml
GPU = opts.gpu
USE_SUM=opts.use_sum;

if opts.std_file != "":
   saveout = sys.stdout   # save initial state of stdout
   print saveout
   print "STD_OUT is being redirected" 
   set_stdout(opts.std_file)


####################################################### 
#Initialize a GPU
####################################################### 
print "Initializing GPU"

os.chdir(scene_root)
scene_path = os.getcwd() + "/" + SCENE_NAME
if not os.path.exists(scene_path):
  print "Error: Scene not found! ", scene_path
  sys.exit(1)
scene = boxm2_scene_adaptor (scene_path, GPU);  

#######################################################
#Clean Up
#######################################################

#delete all 
scene_dir = os.path.dirname(scene_path)
vis_score = glob( scene_dir + "/*vis_score*"); 
vis_sphere = glob( scene_dir + "/*vis_sphere*"); 
aux = glob( scene_dir + "/*aux*"); 

toRemove = vis_score + vis_sphere + aux;

for f in toRemove:
  os.remove(f);   


######################################################## 
#Flip Gradients
######################################################## 
status = scene.flip_normals(USE_SUM);
if(status == False) :
     print "Flipping Normals Failed, clearing cache and exiting:"
     scene.clear_cache();
     boxm2_batch.clear();
     sys.exit(2);


####################################################### 
#write and clear cache before exiting 
####################################################### 
print "WRITING CACHE..." 
scene.write_cache(); 
print "CLEANING CACHE..." 
scene.clear_cache();
print "CLEANING DB..." 
boxm2_batch.clear();

if opts.std_file != "":
   reset_stdout();
   print "STD_OUT is being reset" 

print "Done"

sys.exit(0)

