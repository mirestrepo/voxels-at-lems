# Author: Isabel Restrepo

import random, os, sys, time, argparse;
from boxm2_scene_adaptor import *;
from boxm2_filtering_adaptor import *;
from glob import glob


#######################################################
# handle inputs                                       #
#######################################################

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--sceneroot", action="store", type=str, dest="sceneroot", help="root folder for this scene")
parser.add_argument("-x", "--xmlfile", action="store", type=str, dest="xml", default="uscene.xml", help="scene.xml file name (model/uscene.xml, model_fixed/scene.xml, rscene.xml)")
parser.add_argument("-g", "--gpu",   action="store", type=str, dest="gpu",   default="gpu1", help="specify gpu (gpu0, gpu1, etc)")
parser.add_argument("-p", "--printFile" , action="store", type=str, dest="std_file", default="", help="if given, the std out is redirected to this file")
parser.add_argument('--kernel_path', action="store",type=str, dest="kernel_path");
parser.add_argument("--k_idx",   action="store", type=int, dest="k_idx",   default="0", help="kernel index -- ideally we wouldn't need this but, as of now running all kernels runs out of resources")


args = parser.parse_args()

print "This is boxm2_compute_taylor_coefficients.py. With arguments"
print args

time.sleep(3)


# handle inputs
scene_root = args.sceneroot;

# Set some update parameters
SCENE_NAME = args.xml
GPU = args.gpu

if args.std_file != "":
   saveout = sys.stdout   # save initial state of stdout
   print saveout
   print "STD_OUT is being redirected"
   set_stdout(args.std_file)


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
#Taylor kernels
#######################################################
#Kernel names for 2-degree approximation
kernel_names=[];
kernel_list = [];
kernel_names.append("I0");
kernel_names.append("Ix");
kernel_names.append("Iy");
kernel_names.append("Iz");
kernel_names.append("Ixx");
kernel_names.append("Iyy");
kernel_names.append("Izz");
kernel_names.append("Ixy");
kernel_names.append("Ixz");
kernel_names.append("Iyz");

#######################################################
#Run kernels
#######################################################
for curr_kernel in range(0, len(kernel_names)):
    curr_kernel_path = args.kernel_path + "/" + kernel_names[curr_kernel]+ ".txt";
    taylor_kernel = create_taylor_kernel(curr_kernel_path)
    kernel_list.append(taylor_kernel)

status = True
status = status and scene.kernel_filter(kernel_list[args.k_idx])

if(status == False) :
     print "Computing Filters Failed, clearing cache and exiting:"
     scene.clear_cache();
     boxm2_batch.clear();
     sys.exit(2);

scene.write_cache();

#######################################################
#Clean Up
#######################################################
# boxm2_batch.print_db()

print "CLEANING CACHE..."
scene.clear_cache();
print "CLEANING DB..."
boxm2_batch.clear();
print "Done"

if args.std_file != "":
   reset_stdout();
   print "STD_OUT is being reset"

print "Done"

sys.exit(0)

