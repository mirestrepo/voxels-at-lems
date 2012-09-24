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
    Tfile = "/data/lidar_providence/downtown_offset-1-financial-Hs.txt"
    Tfis = open(Tfile, 'r')
    lines=[];
    lines = Tfis.readlines();
    geo_scale = float(lines[0])
    quat_line = lines[1].split(" ");
    geo_quat = np.array([float(quat_line[1]), float(quat_line[2]), float(quat_line[3]), float(quat_line[0])])
    trans_line = lines[2].split(" ");
    geo_trans = np.array([[float(trans_line[0]), float(trans_line[1]), float(trans_line[2])]])
    geo_trans = geo_trans.reshape(3,1);
    Tfis.close();

    #read source to target "Ground Truth" Transformation
    Tfile = src_scene_root + "/Hs.txt";
    Tfis = open(Tfile, 'r')
    lines=[];
    lines = Tfis.readlines();
    scale = float(lines[0])
    quat_line = lines[1].split(" ");
    quat = np.array([float(quat_line[1]), float(quat_line[2]), float(quat_line[3]), float(quat_line[0])])
    trans_line = lines[2].split(" ");
    trans = np.array([[float(trans_line[0]), float(trans_line[1]), float(trans_line[2])]])
    trans = trans.reshape(3,1);
    Tfis.close();
    Rs = tf.quaternion_matrix(quat)[0:3,0:3];

    #read source to target "Initial Alignment" Transformation
    Tfile = src_features_dir + "/ia_transformation_" + str(percentile) + "_" + str(niter) + ".txt";    
    Tfis = open(Tfile, 'r')
    Rs_ia=np.genfromtxt(Tfis, skip_header=1, skip_footer=1, usecols={0,1,2} );
    Tfis.close()
    Tfis = open(Tfile, 'r')
    Ts_ia=np.genfromtxt(Tfis, skip_header=1, skip_footer=1, usecols={3} );
    Ts_ia = Ts_ia.reshape(3,1);
    Tfis.close()
    Tfis = open(Tfile, 'r')
    Ss_ia=np.genfromtxt(Tfis, skip_footer=4, usecols={0} );
    Tfis.close()
    Ts_ia = (1/Ss_ia) * Ts_ia;
    Rs_ia =  (1/Ss_ia) * Rs_ia
        
    geo_scale_M = np.diag([geo_scale, geo_scale, geo_scale])
    ia_scale_M = np.diag([Ss_ia, Ss_ia, Ss_ia])
    
    Rs_geo = tf.quaternion_matrix(geo_quat)[0:3,0:3]
    
    Rs_ia_geo = geo_scale_M.dot(Rs_geo.dot(ia_scale_M.dot(Rs_ia)));
    Ts_ia_geo = geo_scale_M.dot(Rs_geo.dot(ia_scale_M.dot(Ts_ia))) + geo_scale_M.dot(geo_trans);
    
    scale_M = np.diag([scale, scale, scale])
    Rs_geo_true = geo_scale_M.dot(Rs_geo.dot(scale_M.dot(Rs)));
    Ts_geo_true = geo_scale_M.dot(Rs_geo.dot(scale_M.dot(trans))) + geo_scale_M.dot(geo_trans);
    
    import code; code.interact(local=locals())
    

  #  print "IA:" , Hs_ica

  #   Tfile = src_features_dir + "/icp_transformation_" + str(percentile) + ".txt";
  #   Tfis = open(Tfile, 'r')
  #   Hs_icp=np.genfromtxt(Tfis, skip_footer=1, usecols={0,1,2} );
  #   Tfis.close()
  #   Tfis = open(Tfile, 'r')
  #   Ts_icp=np.genfromtxt(Tfis, skip_footer=1, usecols={3} );
  #   Ts_icp = Ts_icp.reshape(3,1);
  #   Tfis.close()
  # #  print "ICP:" , Hs_icp
  # 
  # #  scale_inv = Ss_ica;
  # #  Rs_inv = Hs_icp.dot(Hs_ica); print "ICP"
  # #  Ts_inv = Ts_ia + Ts_icp;
  # 
  #   scale_inv = Ss_ica;
  #   Rs_inv = (Rs_ia); print "IC"
  #   Ts_inv = Ts_ia;
  # 
  #   error_s = scale*scale_inv
  #   error_R = (error_s*(Rs_inv.dot(Rs)) - np.eye(3));
  #   error_T = error_s*(Rs_inv.dot(Ts)) + scale_inv*Ts_inv;

def main(argv=None):
    args = process_command_line(argv)
    compute_error(0, args.descriptor, 500, 99)
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
