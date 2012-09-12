# Author : Isabel Restrepo

import random, os, sys;  
from boxm2_scene_adaptor import *; 
from boxm2_filtering_adaptor import *;
from glob import glob


# handle inputs
#scene is given as first arg, figure out paths
scene_root = root_dir="/data/helicopter_providence_3_12/site_12";


# Set some update parameters
SCENE_NAME = "model/scene_cropped.xml"
GPU = "gpu1"
export_file = "normals.ply";
dim_x = 2;
dim_y = 3;
dim_z = 3;
supp_x = 1.5;
supp_y = 1;
supp_z = 1;
USE_SUM=True;
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
#Compute Gradients
####################################################### 
filters = create_kernel_vector("gauss_x", "XYZ", dim_x, dim_y, dim_z, supp_x, supp_y, supp_z);
scene.kernel_vector_filter(filters);
scene.write_cache(); 
scene.interpolate_normals(filters);
scene.write_cache(); 

####################################################### 
#Export oriented point cloud
####################################################### 
if export_file != "":
  scene.extract_cell_centers();
  scene.flip_normals(USE_SUM);
  scene.write_cache(); 
  scene.export_points_and_normals(export_file, True, 0.3, 0.0, 0.0, "")


####################################################### 
#Clean Up  
####################################################### 
scene.clear_cache();
boxm2_batch.clear();

print "Done"

sys.exit(0)

