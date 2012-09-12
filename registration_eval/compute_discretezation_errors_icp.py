#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo

"""
import os, sys, subprocess
import glob
import time
from optparse import OptionParser

import numpy as np
from numpy import linalg as LA
#from vpcl_adaptor import *
#from boxm2_utils import *

def compute_error(trial):

#  src_scene_root = "/data/reg3d_eval/downtown_dan/trial_" +str(trial);
#  src_features_dir = "/data/reg3d_eval/downtown_dan/trial_" +str(trial)+ "/FPFH_30"
  #  root_dir="/data/reg3d_eval/downtown_dan/pert_01_$trial_number"
  src_scene_root = "/data/reg3d_eval/downtown_dan/pert_005_" +str(trial);
  src_features_dir = "/data/reg3d_eval/downtown_dan/pert_005_" +str(trial)+ "/FPFH_30"
  
  percentile = 99;

  #read source to target "Ground Truth" Transformation
  Tfile = src_scene_root + "/Hs_inv.txt";
  Tfis = open(Tfile, 'r')
  lines=[];
  lines = Tfis.readlines();
  scale = float(lines[0])
  quat_line = lines[1].split(" ");
  quat = np.array([float(quat_line[0]), float(quat_line[1]), float(quat_line[2]), float(quat_line[3])])
  trans_line = lines[2].split(" ");
  trans = np.array([[float(trans_line[0]), float(trans_line[1]), float(trans_line[2])]])
  Tfis.close();

  R = np.array(np.zeros([3,3]));
  x = quat[0];
  y= quat[1];
  z = quat[2];
  u = quat[3];

  R[0,0] = 1 - 2*y*y - 2*z*z
  R[1,1] = 1 - 2*x*x - 2*z*z
  R[2,2] = 1 - 2*x*x - 2*y*y

  R[0,1] = 2*x*y + 2*u*z
  R[0,2] = 2*x*z - 2*u*y

  R[1,0] = 2*x*y - 2*u*z
  R[1,2] = 2*y*z + 2*u*x

  R[2,0] = 2*x*z + 2*u*y
  R[2,1] = 2*y*z - 2*u*x

  R = R.transpose()
  #T

  #Hs = np.concatenate((scale*R,scale*trans.T), axis=1)
  #Hs = np.concatenate((Hs, np.array([[0, 0, 0,1]])) , axis=0);
  Hs = scale*R;
#  print Hs

  Tfile = src_features_dir + "/ia_transformation_" + str(percentile) + ".txt";
  Tfis = open(Tfile, 'r')
  Hs_ica=np.genfromtxt(Tfis, skip_header=1, skip_footer=1, usecols={0,1,2} );
  Tfis.close()
#  print "IA:" , Hs_ica

  Tfile = src_features_dir + "/icp_transformation_" + str(percentile) + ".txt";
  Tfis = open(Tfile, 'r')
  Hs_icp=np.genfromtxt(Tfis, skip_footer=1, usecols={0,1,2} );
  Tfis.close()
#  print "ICP:" , Hs_icp

#  Hs_inv = Hs_icp.dot(Hs_ica); print "ICP"
  Hs_inv  = Hs_ica; print "IA"
#  print Hs_inv 
#  print LA.inv(Hs)


  #T = np.genfromtxt(T_fname);
  #T_prime = np.genfromtxt(T_prime_fname);
  #
  T = Hs_inv.dot(Hs); #if no error, this matrix should be identity .dot() because these are np arrays
#  import code; code.interact(local=locals())

  #The apriori covariance - assume uncorrelated variables
  s = 0.5  #meters
  COV = np.diagflat([s*s,s*s,s*s]);

  COV_hat = T.dot(COV);
  COV_hat = COV_hat.dot(T.transpose());


  #
  ##Compute Circular Error and Elevetion Error
  w, v = LA.eig(COV_hat);
  print w
  axes = np.zeros((3,1))
  error_90 = 2*np.sqrt(w)*2.5 #to find 90% confidence ellipsoid, scale the eigenvalues, see pg. 416 on Intro To Modern Photogrammetry, Mikhail, et. al.


  #now find LE (vertical error) by projecting onto z-axis
  z_proj = v[2,:]
  weight_z_proj = error_90 * z_proj;
  LE = np.max(abs(weight_z_proj));

  x_proj = v[0,:];
  weight_x_proj = error_90 * x_proj;
  CE_x = np.max(abs(weight_x_proj));

  y_proj = v[1,:];
  weight_y_proj = error_90 * y_proj;
  CE_y = np.max(abs(weight_y_proj));

  print LE, CE_x, CE_y
  
  return COV_hat


if __name__ == "__main__":

  COV_inv = np.eye(3);
  for t in range(0,3):
    print "trial:" + str(t)
    COV_inv = COV_inv + LA.inv(compute_error(t));
    
  COV_combined = LA.inv(COV_inv);
  
  ##Compute Circular Error and Elevetion Error
  w, v = LA.eig(COV_combined);
  axes = np.zeros((3,1))
  error_90 = 2*np.sqrt(w)*2.5 #to find 90% confidence ellipsoid, scale the eigenvalues, see pg. 416 on Intro To Modern Photogrammetry, Mikhail, et. al.


  #now find LE (vertical error) by projecting onto z-axis
  z_proj = v[2,:]
  weight_z_proj = error_90 * z_proj;
  LE = np.max(abs(weight_z_proj));

  x_proj = v[0,:];
  weight_x_proj = error_90 * x_proj;
  CE_x = np.max(abs(weight_x_proj));

  y_proj = v[1,:];
  weight_y_proj = error_90 * y_proj;
  CE_y = np.max(abs(weight_y_proj));

  print "Cobined Errors:"
  print LE, CE_x, CE_y
