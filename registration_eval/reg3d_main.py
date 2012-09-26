#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo
A script that encapsulates all steps for evaluation of 3d-registration using SHOT+PVM
September 12, 2012
"""
import os, sys, argparse, subprocess

CONFIGURATION= "Release";
#CONFIGURATION= "Debug";

VPCL_EXE_PATH="/Projects/vpcl/bin_make/" + CONFIGURATION + "/bin"

VXL_MODULE="/Projects/vxl/bin/" + CONFIGURATION + "/lib";
VXL_MODULE_LIB="/Projects/vxl/src/contrib/brl/bseg/boxm2/pyscripts";
VPCL_MODULE= "/Projects/vpcl/bin_make/" + CONFIGURATION+ "/lib";
VPCL_MODULE_LIB = "/Projects/vpcl/vpcl/pyscripts";
VOXELS_AT_LEMS_BOXM2 = "/Projects/voxels-at-lems-git/boxm2"
VOXELS_AT_LEMS_VPCL = "/Projects/voxels-at-lems-git/vpcl"

sys.path.append(VXL_MODULE);
sys.path.append(VXL_MODULE_LIB)
sys.path.append(VPCL_MODULE);
sys.path.append(VPCL_MODULE_LIB);
sys.path.append(VOXELS_AT_LEMS_BOXM2);
sys.path.append(VOXELS_AT_LEMS_VPCL);

#*******************************************************************************************************
#Compute Rigid Transformation
#*******************************************************************************************************

def register_ia(root_dir, descriptor_type, radius = 30, percentile = 99, nr_iterations=200, verbose = True):
  #read the scale from file
  Tfile = root_dir + "/Hs.txt";
  Tfis = open(Tfile, 'r')
  lines=[];
  lines = Tfis.readlines();
  scale = float(lines[0])
  Tfis.close();
  
  #path to where all scenes are
  src_scene_root=root_dir;
  tgt_scene_root="/Users/isa/Experiments/reg3d_eval/downtown_dan/original";
  basename_in="gauss_233_normals_pvn";


  src_fname =  src_scene_root + "/" + basename_in + "_" + str(percentile) + ".ply"
  src_features_dir = src_scene_root + "/" + descriptor_type + "_" + str(radius);
  src_features_fname = src_features_dir + "/descriptors_" + str(percentile) + ".pcd";

  tgt_fname =  tgt_scene_root + "/" + basename_in + "_" + str(percentile) + ".ply"
  tgt_features_dir = tgt_scene_root + "/" + descriptor_type + "_" + str(radius);
  tgt_features_fname = tgt_features_dir + "/descriptors_" + str(percentile) + ".pcd";

  output_cloud_fname =  src_features_dir + "/ia_cloud_" + str(percentile) +"_" + str(nr_iterations) + ".pcd";
  tform_fname =  src_features_dir + "/ia_transformation_" + str(percentile) +"_" + str(nr_iterations) + ".txt";

  tgt_scene_info = tgt_scene_root + "/scene_info.xml"
  tgt_scene_res = parse_scene_resolution(tgt_scene_info);

  if not verbose:
    py_vpcl.set_stdout(src_features_dir+ "/log_ia_" + str(percentile) +'.log')

  #****PARAMETERS*******#
  min_sample_distance = radius*tgt_scene_res;
  max_dist = 4*min_sample_distance;

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
                                 scale        = scale);

  if not verbose:  
    py_vpcl.reset_stdout();
  py_vpcl.clear();
  print "Done with SAC_IA";
  
def register_icp(root_dir, descriptor_type, radius = 30, percentile = 99, nr_iterations=200, rej_normals=False, verbose = True):
  
  #path to where all scenes are
  src_scene_root=root_dir;
  tgt_scene_root="/Users/isa/Experiments/reg3d_eval/downtown_dan/original";
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


def visualize_reg_ia(descriptor, radius = 30, percentile = 99, nr_iterations=200):
  tgtRoot="/Users/isa/Experiments/reg3d_eval/downtown_dan/original"
  tgt_cloud=tgtRoot + "/gauss_233_normals_pvn_" + str(percentile) + ".ply"
  src_cloud=root_dir + "/" + descriptor + "_" + str(radius) + "/ia_cloud_" + str(percentile) + "_" + str(nr_iterations) + ".pcd"
  exe = VPCL_EXE_PATH + "/visualize"
  subprocess.call([exe , src_cloud, tgt_cloud])

def visualize_reg_icp(descriptor, radius = 30, percentile = 99, nr_iterations=200, rej_normals = False):
  tgtRoot="/Users/isa/Experiments/reg3d_eval/downtown_dan/original"
  tgt_cloud= tgtRoot+ "/gauss_233_normals_pvn_" +str(percentile) + ".ply"
  if rej_normals:
    src_cloud=root_dir + "/" + descriptor + "_" + str(radius) + "/icp_cloud_" + str(percentile) + "_" + str(nr_iterations) + "_n.pcd"
  else:
    src_cloud=root_dir + "/" + descriptor + "_" + str(radius) + "/icp_cloud_" + str(percentile) + "_" + str(nr_iterations) + ".pcd"
  exe = VPCL_EXE_PATH + "/visualize"
  subprocess.call([exe , src_cloud, tgt_cloud])
  
if __name__ == "__main__":
  
  # import vpcl_compute_omp_descriptors;
  import vpcl_adaptor
  from vpcl_register import py_vpcl
  from boxm2_utils import *
  
  parser = argparse.ArgumentParser()
  parser.add_argument("--trial",          action="store",   type=int,     dest="trial",       default=0,      help="Trial number");
  parser.add_argument("--reg_ia",         action="store",   type=bool,    dest="reg_ia",      default=False,  help="Run initial alignment");
  parser.add_argument("--reg_icp",        action="store",   type=bool,    dest="reg_icp",     default=False,  help="Run ICP");
  parser.add_argument("--vis_ia",         action="store",   type=bool,    dest="vis_ia",      default=False,  help="Visualize initial alignment");
  parser.add_argument("--vis_icp",        action="store",   type=bool,    dest="vis_icp",     default=False,  help="Visualize ICP");
  parser.add_argument("--descriptor",     action="store",   type=str,     dest="descriptor",  default="FPFH", help="Trial number");
  parser.add_argument("--rej_normals",    action="store",   type=bool,    dest="rej_normals", default=False,  help="Reject normals?");
  parser.add_argument("--verbose",        action="store",   type=bool,    dest="verbose",     default=False,  help="Print or redirect to log file");
  parser.add_argument("--n_iter",         action="store",   type=int,     dest="n_iter",      default=200,    help="Number of iterations");
  
  
  args = parser.parse_args()
  
  print args
  
  trial_number = args.trial;  
  root_dir="/Users/isa/Experiments/reg3d_eval/downtown_dan/trial_" + str(trial_number)
  descriptor_type=args.descriptor
  radius=30;
  percentile=99;
  verbose=args.verbose;

  if args.reg_ia:
   print "Running IA"
   register_ia(root_dir, descriptor_type, radius, percentile, args.n_iter, verbose)

  if args.reg_icp:
   print "Running ICP"
   register_icp(root_dir, descriptor_type, radius, percentile, args.n_iter, args.rej_normals, verbose)

  if args.vis_ia:
   print "Visualizing  IA"
   visualize_reg_ia(descriptor_type, radius, percentile, args.n_iter)

  if args.vis_icp:
   print "Visualizing  ICP"
   visualize_reg_icp(descriptor_type, radius, percentile, args.n_iter, args.rej_normals)
     
 
