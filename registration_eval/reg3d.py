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
import transformations as tf
import numpy as np
import reg3d_transformations as reg3d_T
import math
from numpy import linalg as LA


#*******************************************************************************************************
#Compute Rigid Transformation
#*******************************************************************************************************

def register_ia(gt_root_dir, trial_root_dir, descriptor_type, radius = 30,
                percentile = 99, nr_iterations=200, verbose = True,
                aux_output_string = "", descriptors_string = "descriptors",
                basename_in="gauss_233_normals_pvn", gt_fname ="Hs.txt"):

    #read the scale from file
    Tfile = trial_root_dir + "/" + gt_fname
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



    src_fname =  src_scene_root + "/" + basename_in + "_" + str(percentile) + ".ply"
    src_features_dir = src_scene_root + "/" + descriptor_type + "_" + str(radius)
    src_features_fname = src_features_dir + "/" + descriptors_string + "_" + str(percentile) + ".pcd"

    tgt_fname =  tgt_scene_root + "/" + basename_in + "_" + str(percentile) + ".ply"
    tgt_features_dir = tgt_scene_root + "/" + descriptor_type + "_" + str(radius)
    tgt_features_fname = tgt_features_dir + "/" + descriptors_string + "_" + str(percentile) + ".pcd"

    output_cloud_fname =  src_features_dir + "/ia_cloud_" + str(percentile) +"_" + str(nr_iterations) + "_" + aux_output_string + ".pcd";
    tform_fname =  src_features_dir + "/ia_transformation_" + str(percentile) +"_" + str(nr_iterations) + "_" + aux_output_string + ".txt";

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

def register_icp(gt_root_dir,trial_root_dir, descriptor_type, radius = 30,
                 percentile = 99, nr_iterations=200, rej_normals=False,
                 verbose = True, use_max_nr_iter=False,
                 aux_output_string = "", basename_in="gauss_233_normals_pvn"):

  #path to where all scenes are
  src_scene_root=trial_root_dir;
  tgt_scene_root=gt_root_dir;


  src_features_dir = src_scene_root + "/" + descriptor_type + "_" + str(radius);
  src_fname = src_features_dir + "/ia_cloud_" + str(percentile) +"_" + str(nr_iterations) + "_" + aux_output_string + ".pcd";

  tgt_fname =  tgt_scene_root + "/" + basename_in + "_" + str(percentile) + ".ply"
  tgt_features_dir = tgt_scene_root + "/" + descriptor_type + "_" + str(radius);

  if rej_normals:
    output_cloud_fname =  src_features_dir + "/icp_cloud_" + str(percentile) + "_" + str(nr_iterations) + "_" + aux_output_string +"_n.pcd"
    tform_fname =  src_features_dir + "/icp_transformation_" + str(percentile) + "_" + str(nr_iterations) + "_" + aux_output_string +"_n.txt"
  else:
    output_cloud_fname =  src_features_dir + "/icp_cloud_" + str(percentile) + "_" + str(nr_iterations) + "_" + aux_output_string + ".pcd"
    tform_fname =  src_features_dir + "/icp_transformation_" + str(percentile) + "_" + str(nr_iterations) + "_" + aux_output_string + ".txt"

  tgt_scene_info = tgt_scene_root + "/scene_info.xml"
  tgt_scene_res = parse_scene_resolution(tgt_scene_info);

  if not verbose:
    py_vpcl.set_stdout(src_features_dir+ "/log_icp_" + str(percentile) +'.log')

  min_sample_distance = radius*tgt_scene_res;
  max_dist = 4*min_sample_distance;
  translation_threshold = 0.001 * tgt_scene_res #used to be 0.1
  rotation_threshold = 0.001; #0.1 degree

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


def visualize_reg_ia(gt_root_dir,trial_root_dir, descriptor, radius = 30,
                     percentile = 99, nr_iterations=200, geo=False,
                     aux_output_string = "", basename_in="gauss_233_normals_pvn"):

  if geo:
    tgtRoot=gt_root_dir
    tgt_cloud= tgtRoot+ "/" + basename_in +"_" +str(percentile) + "_XYZ_geo.pcd"
    src_cloud=trial_root_dir + "/" + descriptor + "_" + str(radius) + "/ia_cloud_" + str(percentile) + "_" + str(nr_iterations) + "_geo.pcd"
  else:
    tgtRoot=gt_root_dir
    tgt_cloud=tgtRoot + "/" + basename_in +"_" + str(percentile) + ".ply"
    src_cloud=trial_root_dir + "/" + descriptor + "_" + str(radius) + "/ia_cloud_" + str(percentile) + "_" + str(nr_iterations) + "_" +aux_output_string + ".pcd"

  exe = VPCL_EXE_PATH + "/visualize"
  subprocess.call([exe , src_cloud, tgt_cloud])

def visualize_reg_icp(gt_root_dir,trial_root_dir, descriptor, radius = 30, percentile = 99, nr_iterations=200, rej_normals = False, geo=False, aux_output_string = "", basename_in="gauss_233_normals_pvn"):

  if geo:
    tgtRoot=gt_root_dir
    tgt_cloud= tgtRoot+ "/" + basename_in + "_99_XYZ.pcd"
    src_cloud=trial_root_dir + "/" + descriptor + "_" + str(radius) + "/icp_cloud_" + str(percentile) + "_" + str(nr_iterations) + "_geo.pcd"
    exe = PCLVIEW_EXE_PATH + "/pcl_viewer"
  else:
    tgtRoot=gt_root_dir
    tgt_cloud= tgtRoot+ "/" + basename_in +"_" +str(percentile) + ".ply"
    if rej_normals:
      src_cloud=trial_root_dir + "/" + descriptor + "_" + str(radius) + "/icp_cloud_" + str(percentile) + "_" + str(nr_iterations) +  "_" +aux_output_string +  "_n.pcd"
    else:
      src_cloud=trial_root_dir + "/" + descriptor + "_" + str(radius) + "/icp_cloud_" + str(percentile) + "_" + str(nr_iterations) +  "_" +aux_output_string +  ".pcd"
    exe = VPCL_EXE_PATH + "/visualize"

  subprocess.call([exe , src_cloud, tgt_cloud])

def transformation_error(**kwargs):

  root_dir = kwargs.get('root_dir')
  descriptor_type = kwargs.get('descriptor_type')
  radius = kwargs.get('radius', 30)
  percentile = kwargs.get('percentile', 99)
  nr_iterations = kwargs.get('nr_iterations', 500)
  aux_output_string = kwargs.get('aux_output_string', "")
  descriptors_string = kwargs.get('descriptors_string', "descriptors")
  gt_fname = kwargs.get('gt_fname', "Hs.txt")
  geo_tfile = kwargs.get('geo_tfile', "")



  src_features_dir = root_dir + "/" + descriptor_type + "_" + str(radius)

  #************GEO**************"
  #load the geo tranformation
  GEO = reg3d_T.geo_transformation(geo_tfile)

  #************Hs**************#
  #read source to target "Ground Truth" Transformation
  Tfile = root_dir + "/" + gt_fname;
  GT_Tform = reg3d_T.gt_transformation(Tfile)

  #************PCL IA and ICP**************
  #read source to target "Initial Alignment" Transformation
  Tfile_ia = src_features_dir + "/ia_transformation_" + str(percentile) + "_" + str(nr_iterations) + "_" + aux_output_string + ".txt";
  Tfile_icp = src_features_dir + "/icp_transformation_" + str(percentile) + "_" + str(nr_iterations) + "_" + aux_output_string + ".txt"

  REG_Tform = reg3d_T.pcl_transformation(Tfile_ia, Tfile_icp)


  #Initial Aligment errors
  #Rotation error - half angle between the normalized quaterions
  quat_ia = tf.unit_vector(tf.quaternion_from_matrix(REG_Tform.Rs_ia));
  Rs_error_ia_norm = math.acos(abs(np.dot(quat_ia, GT_Tform.quat)));

  #Translation error
  # x = REG_Tform.Rs_ia*x_ia + Ts_ia = REG_Tform.Rs_ia(x_ia + np.dot(REG_Tform.Rs_ia.T(), Ts_ia)
  # np.dot(REG_Tform.Rs_ia.T(), Ts_ia) correspond to trans on ia coordinate system
  Ts_error_ia = (REG_Tform.Rs_ia.T).dot(REG_Tform.Ts_ia) - (GT_Tform.Rs.T).dot(GT_Tform.Ts)
  Ts_error_ia_norm = GEO.scale_geo*GT_Tform.scale*LA.norm(Ts_error_ia)

  print  "Error (R,T)", Rs_error_ia_norm , Ts_error_ia_norm


  #ICP errors
  #Rotation error - half angle between the normalized quaterions
  quat_icp = tf.unit_vector(tf.quaternion_from_matrix(REG_Tform.Rs_icp));
  Rs_error_icp_norm = math.acos(abs(np.dot(quat_icp, GT_Tform.quat)));

  #Translation error
  # x = REG_Tform.Rs_ia*x_ia + Ts_ia = REG_Tform.Rs_ia(x_ia + np.dot(REG_Tform.Rs_ia.T(), Ts_ia)
  # np.dot(REG_Tform.Rs_ia.T(), Ts_ia) correspond to trans on ia coordinate system
  Ts_error_icp = (REG_Tform.Rs_icp.T).dot(REG_Tform.Ts_icp) - (GT_Tform.Rs.T).dot(GT_Tform.Ts)
  Ts_error_icp_norm = GEO.scale_geo*GT_Tform.scale*LA.norm(Ts_error_icp)

  print  "Error (R,T)", Rs_error_icp_norm , Ts_error_icp_norm

  IA_error = np.array([Rs_error_ia_norm, Ts_error_ia_norm]);
  ICP_error = np.array([Rs_error_icp_norm, Ts_error_icp_norm])
  # import code; code.interact(local=locals())

  return IA_error, ICP_error

