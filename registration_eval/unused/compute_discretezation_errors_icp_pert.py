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

  src_features_dir = "/data/reg3d_eval/downtown_dan/pert_01_" +str(trial)+ "/FPFH_30"
  
  percentile = 99;

  Hs = np.eye(3);

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

  Hs_inv = Hs_icp.dot(Hs_ica); print "ICP"
#  Hs_inv = LA.inv(Hs);
#  Hs_inv  = Hs_ica; print "IA"
#  print Hs_inv 
#  print LA.inv(Hs)


  #T = np.genfromtxt(T_fname);
  #T_prime = np.genfromtxt(T_prime_fname);
  #
  T = Hs_inv.dot(Hs); #if no error, this matrix should be identity .dot() because these are np arrays
  print T

  #The apriori covariance - assume uncorrelated variables
  s = 0.5  #meters
  COV = np.diagflat([s*s,s*s,s*s]);
  print "COV: ", COV

  COV_hat = T.dot(COV);
  print "COV_hat 1: ", COV_hat
  COV_hat = COV_hat.dot(T.transpose());
  print "COV_hat 2: ", COV_hat



  #
  ##Compute Circular Error and Elevetion Error
  w, v = LA.eig(COV_hat);
  print "w", w
  print "v", v
  axes = np.zeros((3,1))
  error_90 = 2*np.sqrt(w)*2.5 #to find 90% confidence ellipsoid, scale the eigenvalues, see pg. 416 on Intro To Modern Photogrammetry, Mikhail, et. al.
  print LA.norm(v[:,0]), LA.norm(v[:,1]), LA.norm(v[:,2])
  wi, vi = LA.eig(np.eye(3))
  print vi
  import code; code.interact(local=locals())


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
