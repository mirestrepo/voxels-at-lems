#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo
August 15, 2012
Compute rigid transformation between two point clounds using feature correspondances
"""
import os, sys, subprocess
import glob
import time
from optparse import OptionParser
from xml.etree.ElementTree import ElementTree

from vpcl_adaptor import *
from boxm2_utils import *

parser = OptionParser()
parser.add_option("--srcRoot", action="store", type="string", dest="src_scene_root", help="root folder, this is where the .ply input and output files should reside")
parser.add_option("--tgtRoot", action="store", type="string", dest="tgt_scene_root", help="root folder, this is where the .ply input and output files should reside")
parser.add_option("--basenameIn", action="store", type="string", dest="basename_in", help="basename of .ply file")
parser.add_option("-r", "--radius", action="store", type="int", dest="radius", help="radius (multiple of resolution)");
parser.add_option("-p", "--percent", action="store", type="int", dest="percentile", help="data percentile");
parser.add_option("-d", "--descriptor", action="store", type="string", dest="descriptor_type", help="name of the descriptor i.e FPFH");
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="verbose - if false std is redirected to a logfile");
(opts, args) = parser.parse_args()
print opts
print args

#path to where all scenes are
src_scene_root=opts.src_scene_root;
tgt_scene_root=opts.tgt_scene_root;
radius = opts.radius; #gets multiplied by the resolution of the scene
percentile = opts.percentile;
descriptor_type = opts.descriptor_type;
verbose=opts.verbose;

if not verbose:
  py_vpcl.set_stdout("./logs/log_icp_" + descriptor_type + 'percetile' + str(percentile) +'.log')

src_features_dir = src_scene_root + "/" + descriptor_type + "_" + str(radius);
src_fname = src_features_dir + "/ia_cloud_" + str(percentile) + ".pcd";

tgt_fname =  tgt_scene_root + "/" + opts.basename_in + "_" + str(percentile) + ".ply"
tgt_features_dir = tgt_scene_root + "/" + descriptor_type + "_" + str(radius);

output_cloud_fname =  src_features_dir + "/icp_cloud_" + str(percentile) + ".pcd";
tform_fname =  src_features_dir + "/icp_transformation_" + str(percentile) + ".txt";

tgt_scene_info = tgt_scene_root + "/scene_info.xml"
tgt_scene_res = parse_scene_resolution(tgt_scene_info);

min_sample_distance = radius*tgt_scene_res;
max_dist = 4*min_sample_distance;
nr_iterations = 500;
outlier_thresh = max_dist;

register_icp(srcFname     = src_fname,
             tgtFname     = tgt_fname,
             outCloud     = output_cloud_fname,
             tformFname   = tform_fname,
             maxCorrDist  = max_dist,
             outlierThresh = outlier_thresh,
             numIter      = nr_iterations);

if not verbose:  
  py_vpcl.reset_stdout();
     
          
print "Done"

sys.exit(0)