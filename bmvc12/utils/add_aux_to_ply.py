#!/usr/bin/python
# encoding: utf-8
"""
Author: Isabel Restrepo
April 30, 2012

Add auxiliary data (vis, prob, nmag) to the vertices in a .PLY file
"""
import os
import sys
import glob
from optparse import OptionParser


CONFIGURATION= "Release";
#CONFIGURATION= "Debug";

VXL_PATH="/Projects/vxl/bin/" + CONFIGURATION + "/lib";

sys.path.append(VXL_PATH);
sys.path.append("/Projects/vxl/src/contrib/brl/bseg/boxm2/pyscripts");
                
from bbas_adaptor import *;
from boxm2_scene_adaptor import *

parser = OptionParser()
parser.add_option("-s", "--site", action="store", type="int", dest="site", help="site number");
(opts, args) = parser.parse_args()


#path to where all scenes are
scenes_root_path="/data/helicopter_providence_3_12"
experiments_root="/Users/isa/Experiments/shape_features_bmvc12"
verbose=True; #if set to False, the standard output is redirected to a .log file

site=opts.site;

site_dir = scenes_root_path + "/site_" + str(site) ;
scene_path = site_dir + "/model/scene.xml" 
obj_dir = site_dir + "/objects"

scene = boxm2_scene_adaptor (scene_path, "gpu1");  

if not os.path.exists(obj_dir + "/"):
  print "Error: Objects' DIR not found! ", obj_dir
  sys.exit(-1)
       
 
categories = glob.glob(obj_dir + "/*");

  
for cat in categories:
  
  if not os.path.isdir(cat):
    continue;
    
  objs = glob.glob(cat + "/*.ply");
  
  output_dir = site_dir + "/objects_with_aux/" + os.path.basename(cat);
  
  if not os.path.exists(output_dir + "/"):
    print output_dir + "/"
    os.makedirs(output_dir + "/");
  
  for file_in in objs:
    #features get written to a .txt file for now -- PCL reader/writter doesn't handle variable length descriptos
    file_out= output_dir + "/" + os.path.basename(file_in);
    if verbose :
      print "Processing: "
      print file_in
      print "Saving to:"
      print file_out 
      scene.add_aux_info_to_ply(file_in, file_out);
      
scene.clear_cache();
boxm2_batch.clear();  
    
            
print "Done"

sys.exit(0)


