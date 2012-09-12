#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo
April 28, 2012
Use this script to compute OpenMP PCL descriptors on PLY objects
"""
import os
import sys
import glob
import time
from optparse import OptionParser
from xml.etree.ElementTree import ElementTree

from vpcl_adaptor import *
from boxm2_utils import *

parser = OptionParser()
parser.add_option("-s", "--sceneroot", action="store", type="string", dest="sceneroot", help="root folder, this is where the .ply input and output files should reside")
parser.add_option("--basenameIn", action="store", type="string", dest="basename_in", help="basename of .ply file")
parser.add_option("-r", "--radius", action="store", type="int", dest="radius", help="radius (multiple of resolution)");
parser.add_option("-p", "--percent", action="store", type="int", dest="percentile", help="data percentile");
parser.add_option("-d", "--descriptor", action="store", type="string", dest="descriptor_type", help="name of the descriptor i.e FPFH");
parser.add_option("-j", "--jobs", action="store", type="int", dest="njobs", default=8, help="number of jobs");
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="verbose - if false std is redirected to a logfile");

(opts, args) = parser.parse_args()
print opts
print args

#path to where all scenes are
scene_root=opts.sceneroot;
radius = opts.radius; #gets multiplied by the resolution of the scene
percentile = opts.percentile;
descriptor_type = opts.descriptor_type;
njobs=opts.njobs;
verbose=opts.verbose;

   
#figure out the resolution from the scene _info.xml
resolution = parse_scene_resolution(scene_root + "/scene_info.xml");
print "Resolution for site is : " + str(resolution);

features_dir = scene_root + "/" + descriptor_type + "_" + str(radius);
  
if not os.path.exists(features_dir + "/"):
  print features_dir + "/"
  os.makedirs(features_dir + "/");

if not verbose:
  vpcl_batch.set_stdout("./logs/log_" + descriptor_type + 'percetile' + str(percentile) +'.log')

file_in =  scene_root + "/" + opts.basename_in + "_" + str(percentile) + ".ply"
file_out = features_dir + "/descriptors_" + str(percentile) + ".pcd";

if verbose :
  print "Processing: "
  print file_in
  print "Saving to:"
  print file_out 
  
compute_descriptor(file_in, file_out, radius*resolution, descriptor_type, njobs);

if not verbose:  
  vpcl_batch.reset_stdout();
     
          
print "Done"

sys.exit(0)


