#!/usr/bin/env python
# encoding: utf-8
"""
plot_ICP_iterations.py

Created by Maria Isabel Restrepo on 2012-09-24.
Copyright (c) 2012 . All rights reserved.
A better initial aligment should lead to a samller number of iterations rquiered for ICP to converge.
This script PLOTS the number of ICP iterations vs IA RANSAC iterations
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
    
def parse_IPC_iter(trial, descriptor_type, niter, percentile=99):

    src_scene_root = "/Users/isa/Experiments/reg3d_eval/downtown_dan/trial_" +str(trial);
    src_features_dir = "/Users/isa/Experiments/reg3d_eval/downtown_dan/trial_" +str(trial)+ "/" + descriptor_type + "_30"

    #read number of iterations
    Tfile = src_features_dir + "/icp_transformation_" + str(percentile) + "_" + str(niter) + "_time.txt";    
    Tfis = open(Tfile, 'r')
    lines=[];
    lines = Tfis.readlines();
    iter_line = lines[1].split(" ");
    icp_iter = int(iter_line[2])
    Tfis.close()
    # import code; code.interact(local=locals())
        
    return icp_iter


def main(argv=None):
    args = process_command_line(argv)
    
    descriptors = ["FPFH", "SHOT"]
    niter = [20, 50, 75, 100, 200, 500] 
    ntrials = 10;
    plot_errors = True;
    
    if (plot_errors):
      colors = ['magenta','blue','green', 'red', 'black'];
      markers = ['-o', '--*', '-s', '--^']
      fig = plt.figure()
      ax = fig.add_subplot(111);
      plt.hold(True);
      plt.axis(tight=True);
    
    
    ICP_iter_mean= np.zeros((len(niter), 1));
    ICP_iter_min= np.zeros((len(niter), 1))
    ICP_iter_max= np.zeros((len(niter), 1))
    ICP_iter_median= np.zeros((len(niter), 1))
    
    for d_idx in range(0, len(descriptors)):
      
      descriptor = descriptors[d_idx];
      
      for iter_idx in range(0,len(niter)):
      
        ICP_iter = np.zeros((ntrials, 1));
        ICP_error = np.zeros((ntrials, 1));

        for trial in range(0,ntrials):
          ICP_iter[trial,:] = parse_IPC_iter(trial, descriptor, niter[iter_idx], 99)
      
        #Compute mean, max and min
        print "Descriptor: ", descriptor
        print ICP_iter
        ICP_iter_mean[iter_idx, :] = np.mean(ICP_iter, axis=0)
        ICP_iter_max[iter_idx, :] = np.max(ICP_iter, axis=0)
        ICP_iter_min[iter_idx, :] = np.min(ICP_iter, axis=0)
        ICP_iter_median[iter_idx, :] = np.median(ICP_iter, axis=0)
      # import code; code.interact(local=locals())
  
    
      if (plot_errors):
            
        #plot IA, ICP --> missing to to ICP_normals
        ax.errorbar(niter, ICP_iter_median[:, 0], yerr=[ ICP_iter_median[:, 0]-ICP_iter_min[:, 0], ICP_iter_max[:, 0]- ICP_iter_median[:, 0]], fmt=markers[2*d_idx+1], color=colors[2*d_idx+1], label=descriptor , capsize=12, ms=12);
         
    if (plot_errors):  
      ax.set_xlabel('Number of RANSAC_FA Iterations',fontsize= 20);
      ax.set_ylabel('Number of ICP Iterations',fontsize= 20);  
      #classes= ['Plane', 'House', 'Building', 'Car', 'Parking Lot'];
      ax.set_xlim((0,505) );
      ax.set_xticks(np.arange(0,505,50) );
      ax.set_yticks(np.arange(0.0,265.0,20));
      ax.set_ylim((0,270) );
      # axT.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
      #             ncol=4, mode="expand", borderaxespad=0.)
      ax.legend(loc='upper center', frameon=False);  
      
      fig.savefig("/Users/isa/Experiments/reg3d_eval/downtown_dan/ICP_iter.pdf", transparent=True, pad_inches=5)
        
      #********************Detail Plot***************************
      # axT_detail.set_xlim((90,210) ); 
      # axT_detail.set_xticks((100,200 ) );
      # axT_detail.set_yticks(np.arange(0,25,3));
      # axT_detail.set_ylim((0,25))
      # figT_detail.savefig("/Users/isa/Experiments/reg3d_eval/downtown_dan/T_detail_error.pdf", transparent=True)
      
      plt.show();
      
  
    return 0

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


