#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo
March 25, 20123
Use this script to compute OpenMP PCL descriptors on PLY objects, uses vpcl instead of dbrec3d
"""
import os
import sys
import glob
import time
from optparse import OptionParser
from xml.etree.ElementTree import ElementTree

#set up enviroment
# CONFIGURATION= "Release";
#CONFIGURATION= "Debug";
# LEMS_PATH="/Projects/lemsvxl/bin/" + CONFIGURATION + "/lib";
# sys.path.append(LEMS_PATH);
# sys.path.append("/Projects/lemsvxl/src/contrib/dbrec_lib/dbrec3d/pyscripts");

import vpcl_adaptor as vpcl
import py_vpcl
from bmvc12_adaptor import *

parser = OptionParser()
parser.add_option("-r", "--radius", action="store", type="int", dest="radius", help="radius (multiple of resolution)");
parser.add_option("-p", "--percent", action="store", type="int", dest="percentile", help="data percentile");
parser.add_option("-d", "--descriptor", action="store", type="string", dest="descriptor_type", help="name of the descriptor i.e FPFH");
parser.add_option("-j", "--jobs", action="store", type="int", dest="njobs", default=8, help="number of jobs");
(opts, args) = parser.parse_args()
print opts
print args

#path to where all scenes are
scenes_root_path="/Users/isa/Experiments/helicopter_providence_3_12"
experiments_root="/Users/isa/Experiments/shape_features_bmvc12"
verbose=False; #if set to False, the standard output is redirected to a .log file
sites= [8,10,12,19,22,50,51];


radius = opts.radius; #gets multiplied by the resolution of the scene
percentile = opts.percentile;
descriptor_type = opts.descriptor_type;
njobs=opts.njobs;


# if (len(sites)!=17):
#   print "Wrong number of sites"
#   sys.exit(9);



print "STD_OUT is being redirected"

for si in sites:

  site_dir = scenes_root_path + "/site_" + str(si)
  obj_dir = site_dir + "/objects_with_aux"

  if not os.path.exists(obj_dir + "/"):
    print "Error: Objects' DIR not found! ", obj_dir
    sys.exit(-1)


  #figure out the resolution from the scene _info.xml
  resolution = parse_scene_resolution(site_dir + "/scene_info.xml");
  print "Resolution for site: " + str(si) + "is: " + str(resolution);


  categories = glob.glob(obj_dir + "/*" + str(percentile));


  for cat in categories:

    if not os.path.isdir(cat):
      continue;

    objs = glob.glob(cat + "/*.ply");

    features_dir = experiments_root + "/site_" + str(si) + "/" + descriptor_type + "_" + str(radius) + "/" +os.path.basename(cat);

    if not os.path.exists(features_dir + "/"):
      print features_dir + "/"
      os.makedirs(features_dir + "/");


    if not verbose:
      py_vpcl.set_stdout("./logs/log_" + descriptor_type + 'percetile' + str(percentile) +'.log')

    for file_in in objs:
        #features get written to a .txt file for now -- PCL reader/writter doesn't handle variable length descriptos
        file_out= features_dir + "/" + os.path.basename(file_in);
        file_out = file_out[:-len(".ply")]
        file_out = file_out  + ".txt";
        if verbose :
          print "Processing: "
          print file_in
          print "Saving to:"
          print file_out
        vpcl.compute_descriptor(file_in, file_out, radius*resolution, descriptor_type, njobs);


    if not verbose:
      py_vpcl.reset_stdout();


print "Done"

sys.exit(0)


