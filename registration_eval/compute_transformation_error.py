#!/usr/bin/env python
# encoding: utf-8
"""
compute_transformation_error.py

Created by Maria Isabel Restrepo on 2012-09-24.
Copyright (c) 2012 . All rights reserved.
"""
import os
import sys
import logging
import argparse
from vpcl_adaptor import *
import numpy as np
from numpy import linalg as LA
import transformations as tf
import math

LOG = None

def process_command_line(argv):
    """
    Return a 2-tuple: (settings object, args list).
    `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
    """
    global LOG
    if argv is None:
        argv = sys.argv[1:]
    
    # initialize the parser object:
    parser = argparse.ArgumentParser(description="Export PLY to PCD file")
    
    # define options here:
    parser.add_argument("-d", "--descriptor",   action='store',    type = str,   dest="descriptor",    default="FPFH",    help="Type descriptor")
    parser.add_argument("-v", "--verbose",      action='store',    type = bool,   dest="verbose",       default=True,  help="Write debug log to log_file")
    parser.add_argument("-L", "--log", dest="logfile", help="write debug log to log_file")
 
    args = parser.parse_args(argv)
    
    # set up logging
    if args.verbose:
        LOG = setlogging(args.logfile)
        
    # if not args.input_file or not args.output_file :
    #     pass
    #     LOG.error("Input or Output filename not specified")
    #     parser.error("You must supply an input file")
    
    return args
    
def compute_error(trial, descriptor_type, niter, percentile=99):

    src_scene_root = "/Users/isa/Experiments/reg3d_eval/downtown_dan/trial_" +str(trial);
    src_features_dir = "/Users/isa/Experiments/reg3d_eval/downtown_dan/trial_" +str(trial)+ "/" + descriptor_type + "_30"

    #read "geo-transformatiom"
    print "************GEO**************"
    Tfile = "/data/lidar_providence/downtown_offset-1-financial-Hs.txt"
    Tfis = open(Tfile, 'r')
    lines=[];
    lines = Tfis.readlines();
    scale_geo = float(lines[0])
    Ss_geo = tf.scale_matrix(scale_geo);
    quat_line = lines[1].split(" ");
    quat_geo = np.array([float(quat_line[3]), float(quat_line[0]), float(quat_line[1]), float(quat_line[2])])
    Rs_geo = tf.quaternion_matrix(quat_geo);
    trans_line = lines[2].split(" ");
    trans_geo = np.array([float(trans_line[0]), float(trans_line[1]), float(trans_line[2])]);
    Tfis.close();
    Hs_geo = Rs_geo.copy();
    Hs_geo[:3, 3] = trans_geo[:3]
    Hs_geo = Ss_geo.dot(Hs_geo)
    print "Scale:\n", Ss_geo
    print "R:\n", Rs_geo
    print "T:\n", trans_geo
    print "H:\n", Hs_geo
    

    #read source to target "Ground Truth" Transformation
    # print "************Hs INV**************"
    # Tfile = src_scene_root + "/Hs_inv.txt";
    # Tfis = open(Tfile, 'r')
    # lines=[];
    # lines = Tfis.readlines();
    # scale = float(lines[0])
    # Ss_inv = tf.scale_matrix(scale);
    # quat_line = lines[1].split(" ");
    # quat_inv = np.array([float(quat_line[3]), float(quat_line[0]), float(quat_line[1]), float(quat_line[2])])
    # Rs_inv = tf.quaternion_matrix(quat_inv);
    # trans_line = lines[2].split(" ");
    # trans_inv = np.array([float(trans_line[0]), float(trans_line[1]), float(trans_line[2])]);
    # Tfis.close();
    # Hs_inv = Rs_inv.copy();
    # Hs_inv[:3, 3] = trans_inv[:3]
    # Hs_inv = Ss_inv.dot(Hs_inv)
    # 
    # print "Scale:\n", Ss_inv
    # print "R:\n", Rs_inv
    # print "T:\n", trans_inv
    # print "H:\n", Hs_inv
    
    #read source to target "Ground Truth" Transformation
    print "************Hs**************"
    Tfile = src_scene_root + "/Hs.txt";
    Tfis = open(Tfile, 'r')
    lines=[];
    lines = Tfis.readlines();
    scale = float(lines[0])
    Ss = tf.scale_matrix(scale);
    quat_line = lines[1].split(" ");
    quat = tf.unit_vector(np.array([float(quat_line[3]), float(quat_line[0]), float(quat_line[1]), float(quat_line[2])]))
    Hs = tf.quaternion_matrix(quat);
    trans_line = lines[2].split(" ");
    Ts = np.array([float(trans_line[0]), float(trans_line[1]), float(trans_line[2])]);
    Tfis.close();
    Rs = Hs.copy()[:3,:3];
    Hs[:3, 3] = Ts[:3]
    Hs=Ss.dot(Hs) 
    
    Rs = Rs;
    Ts = Ts;
  
    
    print "Scale:\n", Ss
    print "R:\n", Rs
    print "T:\n", Ts
    print "H:\n", Hs
    
    
    
    #read source to target "Initial Alignment" Transformation
    print "************Hs IA**************"
    Tfile = src_features_dir + "/ia_transformation_" + str(percentile) + "_" + str(niter) + ".txt";    
    Tfis = open(Tfile, 'r')
    Hs_ia = np.genfromtxt(Tfis, skip_header=1, usecols={0,1,2,3} );
    Tfis.close()
    Tfis = open(Tfile, 'r')
    Ss_ia=np.genfromtxt(Tfis, skip_footer=4, usecols={0} );
    Tfis.close()
    Rs_ia = Hs_ia[:3,:3]*(1.0/Ss_ia)
    Ts_ia = Hs_ia[:3,3]*(1.0/Ss_ia)
    
    print "R:\n", Rs_ia
    print "T:\n", Ts_ia
    print "H:\n", Hs_ia
    
    #Approximation of identinty transformation from initial alignmenet
    # HHinv_ia = Hs_inv.dot(Hs_ia);
    # RRinv_ia = HHinv_ia[:3, :3]
    # TTinv_ia = HHinv_ia[:3, 3]
    #Not really! -- The rotation error is given as the Forbenius Norm of ||H_error - I||_F
    # R_error_ia = RRinv_ia - np.identity(3)
    #   R_error_ia_norm = LA.norm(R_error_ia, 'fro')
    #   T_error_ia_norm = scale_geo*LA.norm(R_error_ia.T.dot(TTinv_ia))
    
    quat_ia = tf.unit_vector(tf.quaternion_from_matrix(Rs_ia));
    Rs_error_ia = Rs_ia - Rs;
    Ts_error_ia = (Rs_ia.T).dot(Ts_ia) - (Rs.T).dot(Ts)
    # Rs_error_ia_norm = scale_geo*scale*LA.norm(Rs_error_ia, 'fro') #Are there units for this norm? I don't think so, dow
    Rs_error_ia_norm = math.acos(abs(np.dot(quat_ia, quat)));
    Ts_error_ia_norm = scale_geo*scale*LA.norm(Ts_error_ia)
    
    print "Error (R,T) ", Rs_error_ia_norm, ",", Ts_error_ia_norm
        
    #read source to target "Initial Alignment" Transformation
    print "************Hs ICP**************"
    Tfile = src_features_dir + "/icp_transformation_" + str(percentile) + "_" + str(niter) + ".txt";    
    Tfis = open(Tfile, 'r')
    Hs_icp = np.genfromtxt(Tfis, usecols={0,1,2,3});
    Tfis.close()
    
    Hs_icp = Hs_icp.dot(Hs_ia)
    Rs_icp = Hs_icp[:3,:3]*(1.0/Ss_ia)
    Ts_icp = Hs_icp[:3,3]*(1.0/Ss_ia)
    
    print "R:\n", Rs_icp
    print "T:\n", Ts_icp
    print "H:\n", Hs_icp

    # #Approximation of identinty transformation from initial alignmenet+ICP
    # HHinv_icp = Hs_inv.dot(Hs_icp.dot(Hs_ia));
    # RRinv_icp = HHinv_icp[:3, :3]
    # TTinv_icp = HHinv_icp[:3, 3]
    # 
    # 
    # #The rotation error is given as the Forbenius Norm of ||H_error - I||_F
    # R_error_icp = RRinv_icp - np.identity(3)
    # R_error_icp_norm = LA.norm(R_error_icp, 'fro')
    # T_error_icp_norm = scale_geo*LA.norm(R_error_icp.T.dot(TTinv_icp))
    
    
    quat_icp = tf.unit_vector(tf.quaternion_from_matrix(Rs_icp));
    Rs_error_icp = Rs_icp - Rs;
    Ts_error_icp = (Rs_icp.T).dot(Ts_icp) - (Rs.T).dot(Ts)
    # Rs_error_icp_norm = scale_geo*scale*LA.norm(Rs_error_icp, 'fro') #Are there units for this norm? I don't think so, dow
    Rs_error_icp_norm = math.acos(abs(np.dot(quat_icp, quat)));
    Ts_error_icp_norm = scale_geo*scale*LA.norm(Ts_error_icp)

    print "Error (R,T) ", Rs_error_icp_norm, ",", Ts_error_icp_norm
    
    IA_error = np.array([Rs_error_ia_norm, Ts_error_ia_norm]);
    ICP_error = np.array([Rs_error_icp_norm, Ts_error_icp_norm])
    
    
    import code; code.interact(local=locals())
    
    
    
    return IA_error, ICP_error


def main(argv=None):
    args = process_command_line(argv)
    IA_error_mean= np.zeros((4, 2));
    IA_error_min= np.zeros((4, 2))
    IA_error_max= np.zeros((4, 2))
    IA_error_median= np.zeros((4, 2))
    
    ICP_error_mean= np.zeros((4, 2));
    ICP_error_min= np.zeros((4, 2))
    ICP_error_max= np.zeros((4, 2))
    ICP_error_median= np.zeros((4, 2))
    
    niter = [50,100,200,500]
    
    # for iter_idx in len():
    iter_idx=0;     
    IA_error = np.zeros((10, 2));
    ICP_error = np.zeros((10, 2));

    for trial in range(0,9):
      IA_error[trial,:], ICP_error[trial,:] = compute_error(0, args.descriptor, niter[0], 99)
      import code; code.interact(local=locals())
      
      # IA_error_mean[iter_idx, :] =   
    
    return 0

def setlogging(logfile=None):
    consolelevel = logging.DEBUG
    logger = logging.getLogger(__name__)
    logger.setLevel(consolelevel)
    # create formatter and add it to the handlers
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(consolelevel)
    ch.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    
    # create file handler which logs error messages
    if logfile:
        filelevel = logging.ERROR
        fh = logging.FileHandler(logfile)
        fh.setLevel(filelevel)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    
    #test logging
    # logger.debug("debug message")
    # logger.info("info message")
    # logger.warn("warn message")
    # logger.error("error message")
    # logger.critical("critical message")
    
    return logger

if __name__ == '__main__':
    status = main()
    sys.exit(status)
