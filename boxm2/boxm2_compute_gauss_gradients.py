# Author: Isabel Restrepo

import random, os, sys, time;  
from boxm2_scene_adaptor import *; 
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
parser.add_option("--export_file", action="store", type="string", dest="export_file",   default="", help="if non empty, export to oriented point cloud (as PLY or ZYX)")
parser.add_option("--use_sum",action="store_true", dest="use_sum", default=False, help="use (and store) sum of visibility to flip normals, instead of using max")
parser.add_option("--p_thresh", action="store", type="float", dest="p_thresh", default="0.0", help="Probability threshold")
parser.add_option("--vis_thresh", action="store", type="float", dest="vis_thresh", default="0.0", help="Visibility threshold")
parser.add_option("--nmag_thresh", action="store", type="float", dest="nmag_thresh", default="0.0", help="Normal magnitude threshold")


(opts, args) = parser.parse_args()

print "This is boxm2_compute_gauss_gradients.py. With arguments"
print opts
print args
time.sleep(3)


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
  sys.exit(-1)
scene = boxm2_scene_adaptor (scene_path, GPU);  


####################################################### 
#Compute Gradients
####################################################### 
filters = create_kernel_vector("gauss_x", "XYZ", opts.dim_x, opts.dim_y, opts.dim_z, opts.supp_x, opts.supp_y, opts.supp_z);
scene.kernel_vector_filter(filters);
scene.write_cache(); 
scene.interpolate_normals(filters);
scene.write_cache(); 

####################################################### 
#Export oriented point cloud
####################################################### 
if opts.export_file != "":
  scene.extract_cell_centers();
  scene.flip_normals(USE_SUM);
  scene.write_cache(); 
  scene.export_points_and_normals(opts.export_file, True, opts.p_thresh, opts.vis_thresh, opts.nmag_thresh, "")


####################################################### 
#Clean Up  
####################################################### 
scene.clear_cache();
boxm2_batch.clear();

if opts.std_file != "":
   reset_stdout();
   print "STD_OUT is being reset" 

print "Done"

sys.exit(0)

