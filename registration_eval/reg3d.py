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
# from boxm2_utils import *
import transformations as tf
import numpy as np
import reg3d_transformations as reg3d_T
import math
from numpy import linalg as LA


#*******************************************************************************************************
#Compute Rigid Transformation
#*******************************************************************************************************

# def register_ia(gt_root_dir, trial_root_dir, descriptor_type, radius = 30,
#                 percentile = 99, nr_iterations=200, verbose = True,
#                 aux_output_string = "", descriptor_string = "descriptors",
#                 basename_in="gauss_233_normals_pvn", gt_fname ="Hs.txt"):

def register_ia(**kwargs):
    gt_root_dir         = kwargs.get('gt_root_dir')
    trial_root_dir      = kwargs.get('trial_root_dir')
    descriptor_type     = kwargs.get('descriptor_type')
    radius              = kwargs.get('radius', 30)
    percentile          = kwargs.get('percentile' ,99)
    nr_iterations       = kwargs.get('nr_iterations', 200)
    nsamples            = kwargs.get('nsamples', 3)
    min_sample_distance = kwargs.get('sample_distance', 1)
    #min_sample_distance gets multiplied by radius and resolution
    compute_scale       = kwargs.get('compute_scale', False)
    verbose             = kwargs.get('verbose', True)
    aux_output_string   = kwargs.get('aux_output_string', "")
    descriptor_string   = kwargs.get('descriptor_string', 'descriptors')
    basename_in         = kwargs.get('basename_in',"gauss_233_normals_pvn")
    gt_fname            = kwargs.get('gt_fname',"Hs.txt")
    scale               = kwargs.get('scale', 0)
    bound_scale         = kwargs.get('bound_scale', False)
    bound_percentile    = kwargs.get('bound_percentile', 100)


    for key in kwargs:
        print "Arguments: %s: %s" % (key, kwargs[key])

    print descriptor_string
    print aux_output_string
    max_scale=0;
    min_scale=0;
    #read the scale from file
    if(not compute_scale and scale == 0):
      Tfile = trial_root_dir + "/" + gt_fname
      try:
          Tfis = open(Tfile, 'r')
      except:
        scale = 1
        print "Failed to read " , Tfile
      else:
          lines = []
          lines = Tfis.readlines()
          scale = float(lines[0])
          Tfis.close()
          print "Scale read from file: " , scale

    if compute_scale and bound_scale:
      Tfile = trial_root_dir + "/" + gt_fname
      try:
          Tfis = open(Tfile, 'r')
      except:
        scale = 1
        print "Failed to read " , Tfile
      else:
          lines = []
          lines = Tfis.readlines()
          scale = float(lines[0])
          Tfis.close()
          print "Scale read from file: ", scale

      max_scale = scale + scale*bound_percentile*(1.0/100.0)
      min_scale = scale - scale*bound_percentile*(1.0/100.0)

      print "Scale bounds Percentile: " , bound_percentile
      print "Min Scale: ", min_scale
      print "max_scale: ", max_scale


    print "Using Scale: " , scale

    #path to where all scenes are
    src_scene_root=trial_root_dir
    tgt_scene_root=gt_root_dir

    src_fname =  src_scene_root + "/" + basename_in + "_" + str(percentile) + ".ply"
    src_features_dir = src_scene_root + "/" + descriptor_type + "_" + str(radius)
    src_features_fname = src_features_dir + "/" + descriptor_string + "_" + str(percentile) + ".pcd"

    tgt_fname =  tgt_scene_root + "/" + basename_in + "_" + str(percentile) + ".ply"
    tgt_features_dir = tgt_scene_root + "/" + descriptor_type + "_" + str(radius)
    tgt_features_fname = tgt_features_dir + "/" + descriptor_string + "_" + str(percentile) + ".pcd"

    output_cloud_fname =  src_features_dir + "/ia_cloud_" + str(percentile) +"_" + str(nr_iterations) + "_" + aux_output_string + ".pcd";
    tform_fname =  src_features_dir + "/ia_transformation_" + str(percentile) +"_" + str(nr_iterations) + "_" + aux_output_string + ".txt";

    tgt_scene_info = tgt_scene_root + "/scene_info.xml"
    tgt_scene_res = parse_scene_resolution(tgt_scene_info)

    print "Here"
    if not verbose:
        py_vpcl.set_stdout(src_features_dir+ "/log_ia_" + str(percentile) +"_" + str(nr_iterations) + "_" + aux_output_string +'.log')

    #****PARAMETERS*******#
    min_sample_distance = min_sample_distance*radius*tgt_scene_res
    max_dist = 4*radius*tgt_scene_res

    ransac_scale, avg_scale = vpcl_adaptor.register_ia_sac(  srcFname     = src_fname,
                                                             tgtFname     = tgt_fname,
                                                             srcFeatures  = src_features_fname,
                                                             tgtFeatures  = tgt_features_fname,
                                                             outCloud     = output_cloud_fname,
                                                             tformFname   = tform_fname,
                                                             descType     = descriptor_type,
                                                             minSampleDist= min_sample_distance,
                                                             maxCorrDist  = max_dist,
                                                             numIter      = nr_iterations,
                                                             numSamples   = nsamples,
                                                             computeScale = compute_scale,
                                                             scale        = scale,
                                                             boundScale   = bound_scale,
                                                             minScale     = min_scale,
                                                             maxScale     = max_scale)

    if not verbose:
        py_vpcl.reset_stdout();
        py_vpcl.clear();
    print "Done with SAC_IA";

    return ransac_scale, avg_scale

def register_icp(**kwargs):

  gt_root_dir         = kwargs.get('gt_root_dir')
  trial_root_dir      = kwargs.get('trial_root_dir')
  descriptor_type     = kwargs.get('descriptor_type')
                  = kwargs.get('radius', 30)
  percentile          = kwargs.get('percentile' ,99)
  nr_iterations       = kwargs.get('nr_iterations', 200)
  rej_normals         = kwargs.get('rej_normals', False)
  compute_scale       = kwargs.get('compute_scale', False)
  use_max_nr_iter     = kwargs.get('use_max_nr_iter', False)
  verbose             = kwargs.get('verbose', True)
  aux_output_string   = kwargs.get('aux_output_string', "")
  descriptor_string   = kwargs.get('descriptor_string', 'descriptors')
  basename_in         = kwargs.get('basename_in',"gauss_233_normals_pvn")



  for key in kwargs:
      print "Arguments: %s: %s" % (key, kwargs[key])

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
    py_vpcl.set_stdout(src_features_dir+ "/log_icp_" + str(percentile) +"_" + str(nr_iterations) + "_" + aux_output_string +'.log')

  max_dist = 4*radius*tgt_scene_res;
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
                             rejectNormals = rej_normals,
                             computeScale = compute_scale);

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

  print "calling with options"

  subprocess.call([exe , src_cloud, tgt_cloud, "-bc", "255,255,255", "-fc1", "255,0,255", "-fc2", "0,0,255" , "-ps", "1.5"])

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

  # subprocess.call([exe , src_cloud, tgt_cloud])
  subprocess.call([exe , src_cloud, tgt_cloud, "-bc", "255,255,255", "-fc1", "255,0,255", "-fc2", "0,0,255" , "-ps", "1.5"])

def transformation_error(**kwargs):

  root_dir          = kwargs.get('root_dir')
  descriptor_type   = kwargs.get('descriptor_type')
  radius            = kwargs.get('radius', 30)
  percentile        = kwargs.get('percentile', 99)
  nr_iterations     = kwargs.get('nr_iterations', 500)
  aux_output_string = kwargs.get('aux_output_string', "")
  descriptor_string = kwargs.get('descriptor_string', "descriptors")
  gt_fname          = kwargs.get('gt_fname', "Hs.txt")
  geo_tfile         = kwargs.get('geo_tfile', "")
  compute_scale     = kwargs.get('compute_scale', False)

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

  REG_Tform = reg3d_T.pcl_transformation(Tfile_ia, Tfile_icp, (not compute_scale))


  #Initial Alignment errors
  #Rotation error - half angle between the normalized quaternions
  quat_ia = tf.unit_vector(tf.quaternion_from_matrix(REG_Tform.Rs_ia));
  Rs_error_ia_norm = math.acos(abs(np.dot(quat_ia, GT_Tform.quat)))* 180/np.pi;

  #Translation error
  # x = REG_Tform.Rs_ia*x_ia + Ts_ia = REG_Tform.Rs_ia(x_ia + np.dot(REG_Tform.Rs_ia.T(), Ts_ia)
  # np.dot(REG_Tform.Rs_ia.T(), Ts_ia) correspond to trans on ia coordinate system
  Ts_error_ia = (REG_Tform.Rs_ia.T).dot(REG_Tform.Ts_ia) - (GT_Tform.Rs.T).dot(GT_Tform.Ts)
  Ts_error_ia_norm = GEO.scale_geo*GT_Tform.scale*LA.norm(Ts_error_ia)

  scale_error_ia = 1.0 - REG_Tform.scale_ia/GT_Tform.scale
  print  "Error (S,R,T)", scale_error_ia,  Rs_error_ia_norm , Ts_error_ia_norm

  #ICP errors
  #Rotation error - half angle between the normalized quaternions
  quat_icp = tf.unit_vector(tf.quaternion_from_matrix(REG_Tform.Rs_icp))
  Rs_error_icp_norm = math.acos(abs(np.dot(quat_icp, GT_Tform.quat)))* 180/np.pi

  #Translation error
  # x = REG_Tform.Rs_ia*x_ia + Ts_ia = REG_Tform.Rs_ia(x_ia + np.dot(REG_Tform.Rs_ia.T(), Ts_ia)
  # np.dot(REG_Tform.Rs_ia.T(), Ts_ia) correspond to trans on ia coordinate system
  Ts_error_icp = (REG_Tform.Rs_icp.T).dot(REG_Tform.Ts_icp) - (GT_Tform.Rs.T).dot(GT_Tform.Ts)
  Ts_error_icp_norm = GEO.scale_geo*GT_Tform.scale*LA.norm(Ts_error_icp)
  scale_error_icp = 1.0 - (REG_Tform.scale_icp*REG_Tform.scale_ia)/GT_Tform.scale
  print  "Error (S, R,T)", scale_error_icp, Rs_error_icp_norm , Ts_error_icp_norm

  IA_error = np.array([scale_error_ia, Rs_error_ia_norm, Ts_error_ia_norm])
  ICP_error = np.array([scale_error_icp, Rs_error_icp_norm, Ts_error_icp_norm])
  # import code; code.interact(local=locals())

  return IA_error, ICP_error

def transformation_error_general(**kwargs):

  fname          = kwargs.get('fname') #filename trans. file
  gt_fname       = kwargs.get('gt_fname', "Hs.txt") #filename ground truth trans. file
  geo_fname      = kwargs.get('geo_fname', "")


  #************Hs**************#
  #read source to target "Ground Truth" Transformation
  GT_Tform = reg3d_T.gt_transformation(gt_fname)

  #**************************
  #read source to target estimated Transformation
  Tform = reg3d_T.gt_transformation(fname)

    #load the geo tranformation
  print "geo_fname", geo_fname
  if geo_fname == "":
    geo_scale = 1;
  else:
    GEO = reg3d_T.geo_transformation(geo_fname)
    geo_scale = GEO.scale_geo;



  #Initial Alignment errors
  #Rotation error - half angle between the normalized quaternions
  Rs_error_norm = math.acos(abs(np.dot(Tform.quat, GT_Tform.quat)))* 180/np.pi;

  #Translation error
  # import code; code.interact(local=locals())

  Ts_error = (Tform.Rs.T).dot(Tform.Ts) - (GT_Tform.Rs.T).dot(GT_Tform.Ts)
  Ts_error_norm =  geo_scale*GT_Tform.scale*LA.norm(Ts_error)

  scale_error = 1.0 - Tform.scale/GT_Tform.scale
  print  "Error (S,R,T)", scale_error,  Rs_error_norm , Ts_error_norm


  error = np.array([scale_error, Rs_error_norm, Ts_error_norm])
  # import code; code.interact(local=locals())

  return error

