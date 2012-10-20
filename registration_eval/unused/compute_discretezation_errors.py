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

#parser = OptionParser()
#parser.add_option("--srcRoot", action="store", type="string", dest="src_scene_root", help="root folder, this is where the .ply input and output files should reside")
#parser.add_option("--tgtRoot", action="store", type="string", dest="tgt_scene_root", help="root folder, this is where the .ply input and output files should reside")
#parser.add_option("--basenameIn", action="store", type="string", dest="basename_in", help="basename of .ply file")
#parser.add_option("-r", "--radius", action="store", type="int", dest="radius", help="radius (multiple of resolution)");
#parser.add_option("-p", "--percent", action="store", type="int", dest="percentile", help="data percentile");
#parser.add_option("-d", "--descriptor", action="store", type="string", dest="descriptor_type", help="name of the descriptor i.e FPFH");
#parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="verbose - if false std is redirected to a logfile");
#(opts, args) = parser.parse_args()
#print opts
#print args
#
##path to where all scenes are
#src_scene_root=opts.src_scene_root;
#tgt_scene_root=opts.tgt_scene_root;
#radius = opts.radius; #gets multiplied by the resolution of the scene
#percentile = opts.percentile;
#descriptor_type = opts.descriptor_type;
#verbose=opts.verbose;

trial=4; 
src_scene_root = "/data/reg3d_eval/downtown_dan/trial_" +str(trial);
src_features_dir = "/data/reg3d_eval/downtown_dan/trial_" +str(trial)+ "/FPFH_30"
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
print Hs

Tfile = src_features_dir + "/ia_transformation_" + str(percentile) + ".txt";
Tfis = open(Tfile, 'r')
Hs_inv=np.genfromtxt(Tfis, skip_header=1, skip_footer=1, usecols={0,1,2} );
Tfis.close()

print Hs_inv 
print LA.inv(Hs)


#T = np.genfromtxt(T_fname);
#T_prime = np.genfromtxt(T_prime_fname);
#
T = Hs_inv.dot(Hs); #if no error, this matrix should be identity .dot() because these are np arrays


#The apriori covariance - assume uncorrelated variables
s = 0.5  #meters
COV = np.diagflat([s*s,s*s,s*s]);

COV_hat = T.dot(COV);
COV_hat = COV_hat.dot(T.transpose());


#
##Compute Circular Error and Elevetion Error
w, v = LA.eig(COV_hat);
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


##
##create the vector that corresponds to error ellipsoid
#major_ellipsoid = axes[0]*major;

#LE =  abs(major_ellipsoid[2]);
#CEx = abs(major_ellipsoid[0]);
#CEy = abs(major_ellipsoid[1]);

#CE = CEx > CEy ? CEx : CEy;
#
#if (LE > 2.5)
#  return false;
#if (CE > 2.5)
#  return false;
