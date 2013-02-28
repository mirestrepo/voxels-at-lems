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
parser.add_option("--dim_x", action="store", type="float", dest="dim_x", default="2.0", help="Sigma in the x-dimension")
parser.add_option("--dim_y", action="store", type="float", dest="dim_y", default="3.0", help="Sigma in the x-dimension")
parser.add_option("--dim_z", action="store", type="float", dest="dim_z", default="3.0", help="Sigma in the x-dimension")
parser.add_option("--supp_x", action="store", type="float", dest="supp_x", default="1.5", help="Kernel support in the x-dimension")
parser.add_option("--supp_y", action="store", type="float", dest="supp_y", default="1.0", help="Kernel support  in the x-dimension")
parser.add_option("--supp_z", action="store", type="float", dest="supp_z", default="1.0", help="Kernel support  in the x-dimension")


(opts, args) = parser.parse_args()

print "This is boxm2_compute_gauss_gradients.py. With arguments"
print opts
print args

# handle inputs
scene_root = opts.sceneroot;

# Set some update parameters
SCENE_NAME = opts.xml
GPU = opts.gpu

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
  sys.exit(-1)
scene = boxm2_scene_adaptor (scene_path, GPU);

#######################################################
#Clean Up
#######################################################

#delete all
scene_dir = os.path.dirname(scene_path)
gauss = glob( scene_dir + "/*gauss*");
normal = glob( scene_dir + "/*normal*");
points = glob( scene_dir + "/*point*");
aux = glob( scene_dir + "/*aux*");

toRemove = gauss + normal + points + aux;

for f in toRemove:
  os.remove(f);


########################################################
#Compute Gradients and exctract points
########################################################
filters = create_kernel_vector("gauss_x", "XYZ", opts.dim_x, opts.dim_y, opts.dim_z, opts.supp_x, opts.supp_y, opts.supp_z);
status = scene.kernel_vector_filter(filters);
if(status == False) :
     print "Computing Filters Failed, clearing cache and exiting:"
     scene.clear_cache();
     boxm2_batch.clear();
     sys.exit(2);
scene.write_cache();
scene.clear_cache();
status = scene.interpolate_normals(filters);
if(status == False) :
     print "Interpolating Normal Failed, clearing cache and exiting:"
     scene.clear_cache();
     boxm2_batch.clear();
     sys.exit(2);
scene.write_cache();
scene.clear_cache();
status = scene.extract_cell_centers();
if(status == False) :
     print "Extracting cell centers Failed, clearing cache and exiting:"
     scene.clear_cache();
     boxm2_batch.clear();
     sys.exit(2);
scene.write_cache();

########################################################
#Clean Up
########################################################
scene.clear_cache();
boxm2_batch.clear();

if opts.std_file != "":
   reset_stdout();
   print "STD_OUT is being reset"

print "Done"

sys.exit(0)

