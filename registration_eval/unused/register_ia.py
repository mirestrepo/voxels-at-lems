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
import argparse
from xml.etree.ElementTree import ElementTree

from vpcl_adaptor import *
from boxm2_utils import *

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--srcRoot", action="store", type="string", dest="src_scene_root", help="root folder, this is where the .ply input and output files should reside")
  parser.add_argument("--tgtRoot", action="store", type="string", dest="tgt_scene_root", help="root folder, this is where the .ply input and output files should reside")
  parser.add_argument("--basenameIn", action="store", type="string", dest="basename_in", help="basename of .ply file")
  parser.add_argument("-r", "--radius", action="store", type="int", dest="radius", help="radius (multiple of resolution)");
  parser.add_argument("-p", "--percent", action="store", type="int", dest="percentile", help="data percentile");
  parser.add_argument("-d", "--descriptor", action="store", type="string", dest="descriptor_type", help="name of the descriptor i.e FPFH");
  parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False, help="verbose - if false std is redirected to a logfile");
  parser.add_argument("-s", "--scale", action="store", type="float", dest="scale", help="apply scale");

  args = parser.parse_args()
  
  print args

  #path to where all scenes are
  src_scene_root=args.src_scene_root;
  tgt_scene_root=args.tgt_scene_root;
  radius = args.radius; #gets multiplied by the resolution of the scene
  percentile = args.percentile;
  descriptor_type = args.descriptor_type;
  verbose=args.verbose;

  if not verbose:
    py_vpcl.set_stdout("./logs/log_ia_" + descriptor_type + 'percetile' + str(percentile) +'.log')

  src_fname =  src_scene_root + "/" + args.basename_in + "_" + str(percentile) + ".ply"
  src_features_dir = src_scene_root + "/" + descriptor_type + "_" + str(radius);
  src_features_fname = src_features_dir + "/descriptors_" + str(percentile) + ".pcd";

  tgt_fname =  tgt_scene_root + "/" + args.basename_in + "_" + str(percentile) + ".ply"
  tgt_features_dir = tgt_scene_root + "/" + descriptor_type + "_" + str(radius);
  tgt_features_fname = tgt_features_dir + "/descriptors_" + str(percentile) + ".pcd";

  output_cloud_fname =  src_features_dir + "/ia_cloud_" + str(percentile) + ".pcd";
  tform_fname =  src_features_dir + "/ia_transformation_" + str(percentile) + ".txt";

  tgt_scene_info = tgt_scene_root + "/scene_info.xml"
  tgt_scene_res = parse_scene_resolution(tgt_scene_info);


  min_sample_distance = radius*tgt_scene_res;
  max_dist = 4*min_sample_distance;
  nr_iterations = 50;
  scale = args.scale;


  register_ia_sac( srcFname     = src_fname,
                   tgtFname     = tgt_fname,
                   srcFeatures  = src_features_fname,
                   tgtFeatures  = tgt_features_fname,
                   outCloud     = output_cloud_fname,
                   tformFname   = tform_fname,
                   descType     = descriptor_type,
                   minSampleDist= min_sample_distance,
                   maxCorrDist  = max_dist,
                   numIter      = nr_iterations,
                   scale        = scale);

  if not verbose:  
    py_vpcl.reset_stdout();
     
          
  print "Done"


if __name__ == "__main__":
    main();