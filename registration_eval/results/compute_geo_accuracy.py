#!/usr/bin/env python
# encoding: utf-8
"""
compute_transformation_error.py

Created by Maria Isabel Restrepo on 2012-09-24.
Copyright (c) 2012 . All rights reserved.
This script computes the distances betweeen an estimated similarity transformation and its ground truth
The transformation is used to transform a "source" coordinate system into a "target coordinate system"
To compute the error between the translations, the L2 norm diference translation vectors in the 
"source coordinate system" is computed. Since distances are preserved under R and T, only scale is applied.
The rotation error is computed as the half angle between the normalized queternions i.e acos(|<q1,q2>|) in [0, pi/2]
"""
import os
import sys
import logging
import argparse
import vpcl_adaptor as vpcl
import numpy as np
from numpy import linalg as LA
import transformations as tf
import math
import matplotlib.pyplot as plt

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
    parser.add_argument("-v", "--verbose",      action='store',    type = bool,   dest="verbose",   default=True,  help="Write debug log to log_file")
    parser.add_argument("-L", "--log", dest="logfile", help="write debug log to log_file")
 
    args = parser.parse_args(argv)
    
    # set up logging
    if args.verbose:
        LOG = setlogging(args.logfile)
        
    LOG.debug("debug message")
    LOG.info("info message")
    LOG.warn("warn message")
    LOG.error("error message")
    LOG.critical("critical message")
        
    # if not args.input_file or not args.output_file :
    #     pass
    #     LOG.error("Input or Output filename not specified")
    #     parser.error("You must supply an input file")
    
    return args
    
def compute_geo_accuracy(fid_path, geo_tform, trials_root, desc_name, reg_algo, niter, ntrials, percentile=99):
  
    success, rmse_x, rmse_y, rmse_z, CE_90, LE_90, radius = vpcl.compute_rmse(fidPath           = fid_path,
                                                                          trialRoot         = trials_root,
                                                                          descName          = desc_name,
                                                                          estimateBasename  = reg_algo + "_cloud_" + str(percentile) + "_" + str(niter),
                                                                          nTrials           = ntrials,
                                                                          tformFname        = geo_tform)
    return success, rmse_x, rmse_y, rmse_z, CE_90, LE_90, radius
    

def main(argv=None):
    args = process_command_line(argv)
    
    descriptors = ["FPFH_30"]
    # niter = [20, 50, 75, 100, 200, 500] 
    niter = 500;     
    ntrials = 10;
    plot_errors = True;
    
    if (plot_errors):
      colors = ['magenta','blue','green'];
      markers = ['o', 's', '*', '+', '^', 'v']
         
    fid_path = "/data/lidar_providence/downtown_offset-1-financial-dan-pts1.ply"
    trials_root = "/Users/isa/Experiments/reg3d_eval/downtown_dan";      
    geo_tform = "/data/lidar_providence/downtown_offset-1-financial-dan-Hs.txt"
    for d_idx in range(0, len(descriptors)):
      desc_name = descriptors[d_idx];
      success, rmse_x, rmse_y, rmse_z, CE_90, LE_90, radius  = compute_geo_accuracy(fid_path, geo_tform, trials_root,
                                                                                    desc_name, "icp", niter, 
                                                                                    ntrials, percentile=99);
      
      
      #sort the radius and errors according to the radius
      radius_np = np.array(radius);
      indeces = 	radius_np.argsort(axis=0)
      
      CE_90_np = np.array(CE_90);
      LE_90_np = np.array(LE_90);
      
      # import code; code.interact(local=locals())
      
      
      CE_90_np_sorted = CE_90_np[indeces];
      LE_90_np_sorted = LE_90_np[indeces];
      radius_np_sorted = radius_np[indeces];
      
                                                                                    
      if (plot_errors):
        #Plot CE and LE
        fig = plt.figure()
        ax = fig.add_subplot(111);
        plt.hold(True);
        plt.axis(tight=True);
        ax.plot(radius_np_sorted, CE_90_np_sorted, markers[2*d_idx], color=colors[d_idx], label=  "CE_90 " + desc_name);
        ax.plot(radius_np_sorted, LE_90_np_sorted, markers[2*d_idx+1], color=colors[d_idx], label= "LE_90 " + desc_name);

        ax.set_xlabel('Distance to Origin',fontsize= 20);
        ax.set_ylabel('90% Error (meters)',fontsize= 20);  
        # axT.set_xlim((0,505) );
        # axT.set_yticks(np.arange(0.0,250.0,20));
        # # axT.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
        # #             ncol=4, mode="expand", borderaxespad=0.)
      
        ax.legend(loc='upper center', frameon=False);  
        # 
        # figT.savefig("/Users/isa/Experiments/reg3d_eval/downtown_dan/T_error.pdf", transparent=True, pad_inches=5)

        plt.show();
                                                                                      
                                                                                      

def setlogging(logfile=None):
    level = logging.DEBUG
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    # create formatter and add it to the handlers
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    
    # create file handler which logs error messages
    if logfile:
        print "Logging to file"
        fh = logging.FileHandler(logfile)
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    
    #test logging
    logger.debug("debug message")
    logger.info("info message")
    logger.warn("warn message")
    logger.error("error message")
    logger.critical("critical message")
    
    return logger

if __name__ == '__main__':
    status = main()
    sys.exit(status)
