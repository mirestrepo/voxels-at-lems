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
import argparse

import vpcl_adaptor as vpcl
from boxm2_utils import *

def compute_omp_descriptors(scene_root, descriptor_type, radius, njobs, percentile, verbose=True):
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
  
  vpcl.compute_descriptor(file_in, file_out, radius*resolution, descriptor_type, njobs);

  if not verbose:  
    vpcl_batch.reset_stdout();

  print "Done"


if __name__ == "__main__":
   parser = argparse.ArgumentParser()
   parser.add_option("-s", "--sceneroot", action="store", type="string", dest="sceneroot", help="root folder, this is where the .ply input and output files should reside")
   parser.add_argument("--basenameIn",       action="store", type=str,   dest="basename_in",  default="",      help="basename of .ply file")
   parser.add_argument("-r", "--radius",     action="store", type=int,   dest="radius",       default=30,      help="radius (multiple of resolution)");
   parser.add_argument("-p", "--percent",    action="store", type=int,   dest="percentile",   default=99,      help="data percentile");
   parser.add_argument("-d", "--descriptor", action="store", type=str,   dest="descriptor",   default="FPFH",      help="name of the descriptor i.e FPFH");
   parser.add_argument("-j", "--jobs",       action="store", type=int,   dest="njobs",        default=8,      help="number of jobs");
   parser.add_argument("-v", "--verbose",    action="store", type=bool,  dest="verbose",      default=False,  help="verbose - if false std is redirected to a logfile");

   args = parser.parse_args()

   #path to where all scenes are
   scene_root=args.sceneroot;
   radius = args.radius; #gets multiplied by the resolution of the scene
   percentile = args.percentile;
   descriptor_type = args.descriptor;
   njobs=args.njobs;
   verbose=args.verbose;

   compute_omp_descriptors(scene_root, descriptor_type, radius, njobs, percentile, verbose=True)
