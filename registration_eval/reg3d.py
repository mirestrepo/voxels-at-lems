#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo
A script that encapsulates 3d-registration algorithms in the PVM
September 12, 2012
"""
import os, sys, subprocess

CONFIGURATION= "Release";
#CONFIGURATION= "Debug";

VPCL_EXE_PATH="/Projects/vpcl/bin_make/" + CONFIGURATION + "/bin"

PCLVIEW_EXE_PATH="/Projects/pcl_dev/pcl/trunk/" + CONFIGURATION + "/bin/pcl_viewer.app/Contents/MacOS"

VXL_MODULE="/Projects/vxl/bin/" + CONFIGURATION + "/lib";
VXL_MODULE_LIB="/Projects/vxl/src/contrib/brl/bseg/boxm2/pyscripts";
VPCL_MODULE= "/Projects/vpcl/bin_make/" + CONFIGURATION+ "/lib";
VPCL_MODULE_LIB = "/Projects/vpcl/vpcl/pyscripts";
VOXELS_AT_LEMS_BOXM2 = "/Projects/voxels-at-lems-git/boxm2"
VOXELS_AT_LEMS_VPCL = "/Projects/voxels-at-lems-git/vpcl"
RESULTS = "/Projects/voxels-at-lems-git/registration_eval/results"

sys.path.append(VXL_MODULE)
sys.path.append(VXL_MODULE_LIB)
sys.path.append(VPCL_MODULE)
sys.path.append(VPCL_MODULE_LIB)
sys.path.append(VOXELS_AT_LEMS_BOXM2)
sys.path.append(VOXELS_AT_LEMS_VPCL)
sys.path.append(RESULTS)

import vpcl_adaptor
from vpcl_register import py_vpcl
from boxm2_utils import *


#*******************************************************************************************************
#Compute Rigid Transformation
#*******************************************************************************************************

def register_ia(gt_root_dir, trial_root_dir, descriptor_type, radius = 30, percentile = 99, nr_iterations=200, verbose = True):

    #read the scale from file
    Tfile = trial_root_dir + "/Hs.txt"
    scale = -1;
    try:
        Tfis = open(Tfile, 'r')
    except:
      scale = 1
    else:
        lines = []
        lines = Tfis.readlines()
        scale = float(lines[0])
        Tfis.close()


    print "Using Scale: " , scale

    #path to where all scenes are
    src_scene_root=trial_root_dir
    tgt_scene_root=gt_root_dir
    basename_in="gauss_233_normals_pvn"


    src_fname =  src_scene_root + "/" + basename_in + "_" + str(percentile) + ".ply"
    src_features_dir = src_scene_root + "/" + descriptor_type + "_" + str(radius)
    src_features_fname = src_features_dir + "/descriptors_" + str(percentile) + ".pcd"

    tgt_fname =  tgt_scene_root + "/" + basename_in + "_" + str(percentile) + ".ply"
    tgt_features_dir = tgt_scene_root + "/" + descriptor_type + "_" + str(radius)
    tgt_features_fname = tgt_features_dir + "/descriptors_" + str(percentile) + ".pcd"

    output_cloud_fname =  src_features_dir + "/ia_cloud_" + str(percentile) +"_" + str(nr_iterations) + ".pcd";
    tform_fname =  src_features_dir + "/ia_transformation_" + str(percentile) +"_" + str(nr_iterations) + ".txt";

    tgt_scene_info = tgt_scene_root + "/scene_info.xml"
    tgt_scene_res = parse_scene_resolution(tgt_scene_info)

    print "Here"
    if not verbose:
        py_vpcl.set_stdout(src_features_dir+ "/log_ia_" + str(percentile) +'.log')

    #****PARAMETERS*******#
    min_sample_distance = radius*tgt_scene_res
    max_dist = 4*min_sample_distance

    vpcl_adaptor.register_ia_sac(  srcFname     = src_fname,
                                 tgtFname     = tgt_fname,
                                 srcFeatures  = src_features_fname,
                                 tgtFeatures  = tgt_features_fname,
                                 outCloud     = output_cloud_fname,
                                 tformFname   = tform_fname,
                                 descType     = descriptor_type,
                                 minSampleDist= min_sample_distance,
                                 maxCorrDist  = max_dist,
                                 numIter      = nr_iterations,
                                 scale        = scale)

    if not verbose:
        py_vpcl.reset_stdout();
        py_vpcl.clear();
    print "Done with SAC_IA";

def register_icp(gt_root_dir,trial_root_dir, descriptor_type, radius = 30, percentile = 99, nr_iterations=200, rej_normals=False, verbose = True, use_max_nr_iter=False):

  #path to where all scenes are
  src_scene_root=trial_root_dir;
  tgt_scene_root=gt_root_dir;
  basename_in="gauss_233_normals_pvn";

  src_features_dir = src_scene_root + "/" + descriptor_type + "_" + str(radius);
  src_fname = src_features_dir + "/ia_cloud_" + str(percentile) +"_" + str(nr_iterations) + ".pcd";

  tgt_fname =  tgt_scene_root + "/" + basename_in + "_" + str(percentile) + ".ply"
  tgt_features_dir = tgt_scene_root + "/" + descriptor_type + "_" + str(radius);

  if rej_normals:
    output_cloud_fname =  src_features_dir + "/icp_cloud_" + str(percentile) + "_" + str(nr_iterations) +"_n.pcd";
    tform_fname =  src_features_dir + "/icp_transformation_" + str(percentile) + "_" + str(nr_iterations) + "_n.txt";
  else:
    output_cloud_fname =  src_features_dir + "/icp_cloud_" + str(percentile) + "_" + str(nr_iterations) +".pcd";
    tform_fname =  src_features_dir + "/icp_transformation_" + str(percentile) +"_" + str(nr_iterations) + ".txt";

  tgt_scene_info = tgt_scene_root + "/scene_info.xml"
  tgt_scene_res = parse_scene_resolution(tgt_scene_info);

  if not verbose:
    py_vpcl.set_stdout(src_features_dir+ "/log_icp_" + str(percentile) +'.log')

  min_sample_distance = radius*tgt_scene_res;
  max_dist = 4*min_sample_distance;
  translation_threshold = 0.1 * tgt_scene_res
  rotation_threshold = 0.1; #1 degree

  #set this flag to let ICP run for 500 - nr_iterations is used for naming conventions, but ignored here
  if use_max_nr_iter:
    nr_iterations = 500

  vpcl_adaptor.register_icp( srcFname     = src_fname,
                             tgtFname     = tgt_fname,
                             outCloud     = output_cloud_fname,
                             tformFname   = tform_fname,
                             maxCorrDist  = max_dist,
                             epsTrans     = translation_threshold,
                             epsRot       = rotation_threshold,
                             numIter      = nr_iterations,
                             rejectNormals = rej_normals);

  if not verbose:
    py_vpcl.reset_stdout();
  py_vpcl.clear();
  print "Done with ICP"


def visualize_reg_ia(gt_root_dir,trial_root_dir, descriptor, radius = 30, percentile = 99, nr_iterations=200, geo=False):

  if geo:
    tgtRoot=gt_root_dir
    tgt_cloud= tgtRoot+ "/gauss_233_normals_pvn_" +str(percentile) + "_XYZ_geo.pcd"
    src_cloud=trial_root_dir + "/" + descriptor + "_" + str(radius) + "/ia_cloud_" + str(percentile) + "_" + str(nr_iterations) + "_geo.pcd"
  else:
    tgtRoot=gt_root_dir
    tgt_cloud=tgtRoot + "/gauss_233_normals_pvn_" + str(percentile) + ".ply"
    src_cloud=trial_root_dir + "/" + descriptor + "_" + str(radius) + "/ia_cloud_" + str(percentile) + "_" + str(nr_iterations) + ".pcd"

  exe = VPCL_EXE_PATH + "/visualize"
  subprocess.call([exe , src_cloud, tgt_cloud])

def visualize_reg_icp(gt_root_dir,trial_root_dir, descriptor, radius = 30, percentile = 99, nr_iterations=200, rej_normals = False, geo=False, trial=-1):

  if geo:
    tgtRoot=gt_root_dir
    tgt_cloud= tgtRoot+ "/gauss_233_normals_pvn_99_XYZ.pcd"
    src_cloud=trial_root_dir + "/" + descriptor + "_" + str(radius) + "/icp_cloud_" + str(percentile) + "_" + str(nr_iterations) + "_geo.pcd"
    exe = PCLVIEW_EXE_PATH + "/pcl_viewer"
  else:
    tgtRoot=gt_root_dir
    tgt_cloud= tgtRoot+ "/gauss_233_normals_pvn_" +str(percentile) + ".ply"
    if rej_normals:
      src_cloud=trial_root_dir + "/" + descriptor + "_" + str(radius) + "/icp_cloud_" + str(percentile) + "_" + str(nr_iterations) + "_n.pcd"
    else:
      src_cloud=trial_root_dir + "/" + descriptor + "_" + str(radius) + "/icp_cloud_" + str(percentile) + "_" + str(nr_iterations) + ".pcd"
    exe = VPCL_EXE_PATH + "/visualize"

  subprocess.call([exe , src_cloud, tgt_cloud])
