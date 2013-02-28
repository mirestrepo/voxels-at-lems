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

def compute_error(trial, descriptor_type, niter, percentile=99):

    src_scene_root = "/Users/isa/Experiments/reg3d_eval/downtown_dan/trial_" +str(trial);
    src_features_dir = "/Users/isa/Experiments/reg3d_eval/downtown_dan/trial_" +str(trial)+ "/" + descriptor_type + "_30"

    #read "geo-transformatiom"
    #************GEO**************"
    Tfile = "/data/lidar_providence/downtown_offset-1-financial-dan-Hs.txt"
    Tfis = open(Tfile, 'r')
    lines = []
    lines = Tfis.readlines()
    scale_geo = float(lines[0])
    Ss_geo = tf.scale_matrix(scale_geo)
    quat_line = lines[1].split(" ")
    quat_geo = np.array([float(quat_line[3]), float(quat_line[0]), float(quat_line[1]), float(quat_line[2])])
    Rs_geo = tf.quaternion_matrix(quat_geo)
    trans_line = lines[2].split(" ")
    trans_geo = np.array([float(trans_line[0]), float(trans_line[1]), float(trans_line[2])])
    Tfis.close()
    Hs_geo = Rs_geo.copy()
    Hs_geo[:3, 3] = trans_geo[:3]
    Hs_geo = Ss_geo.dot(Hs_geo)

    LOG.debug( "\n************Geo************** \n Scale: \n%s \nR:\n%s \nT:\n%s \nH:\n%s", Ss_geo, Rs_geo, trans_geo, Hs_geo)


    #************Hs**************#
    #read source to target "Ground Truth" Transformation
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

    LOG.debug( "\n************Hs************** \n R:\n%s \nT:\n%s \nH:\n%s", Rs, Ts, Hs)

    #************Hs IA**************
    #read source to target "Initial Alignment" Transformation
    Tfile = src_features_dir + "/ia_transformation_" + str(percentile) + "_" + str(niter) + ".txt";
    Tfis = open(Tfile, 'r')
    Hs_ia = np.genfromtxt(Tfis, skip_header=1, usecols={0,1,2,3} );
    Tfis.close()
    Tfis = open(Tfile, 'r')
    Ss_ia=np.genfromtxt(Tfis, skip_footer=4, usecols={0} );
    Tfis.close()
    Rs_ia = Hs_ia[:3,:3]*(1.0/Ss_ia)
    Ts_ia = Hs_ia[:3,3]*(1.0/Ss_ia)

    LOG.debug( "\n************Hs IA************** \n R:\n%s \nT:\n%s \nH:\n%s", Rs_ia, Ts_ia, Hs_ia)

    #Initial Aligment errors
    #Rotation error - half angle between the normalized quaterions
    quat_ia = tf.unit_vector(tf.quaternion_from_matrix(Rs_ia));
    Rs_error_ia_norm = math.acos(abs(np.dot(quat_ia, quat)));

    #Translation error
    # x = Rs_ia*x_ia + Ts_ia = Rs_ia(x_ia + np.dot(Rs_ia.T(), Ts_ia)
    # np.dot(Rs_ia.T(), Ts_ia) correspond to trans on ia coordinate system
    Ts_error_ia = (Rs_ia.T).dot(Ts_ia) - (Rs.T).dot(Ts)
    Ts_error_ia_norm = scale_geo*scale*LA.norm(Ts_error_ia)

    LOG.debug(  "Error (R,T) %s , %s ", Rs_error_ia_norm , Ts_error_ia_norm )


    #read source to target "Initial Alignment" Transformation
    #************Hs ICP**************
    Tfile = src_features_dir + "/icp_transformation_" + str(percentile) + "_" + str(niter) + ".txt";
    Tfis = open(Tfile, 'r')
    Hs_icp = np.genfromtxt(Tfis, usecols={0,1,2,3});
    Tfis.close()

    Hs_icp = Hs_icp.dot(Hs_ia)
    Rs_icp = Hs_icp[:3,:3]*(1.0/Ss_ia)
    Ts_icp = Hs_icp[:3,3]*(1.0/Ss_ia)

    LOG.debug( "\n************Hs ICP************** \n R:\n%s \nT:\n%s \nH:\n%s", Rs_icp, Ts_icp, Hs_icp)

    #ICP errors
    #Rotation error - half angle between the normalized quaterions
    quat_icp = tf.unit_vector(tf.quaternion_from_matrix(Rs_icp));
    Rs_error_icp_norm = math.acos(abs(np.dot(quat_icp, quat)));

    #Translation error
    # x = Rs_ia*x_ia + Ts_ia = Rs_ia(x_ia + np.dot(Rs_ia.T(), Ts_ia)
    # np.dot(Rs_ia.T(), Ts_ia) correspond to trans on ia coordinate system
    Ts_error_icp = (Rs_icp.T).dot(Ts_icp) - (Rs.T).dot(Ts)
    Ts_error_icp_norm = scale_geo*scale*LA.norm(Ts_error_icp)

    LOG.debug(  "Error (R,T) %s , %s ", Rs_error_icp_norm , Ts_error_icp_norm )

    IA_error = np.array([Rs_error_ia_norm, Ts_error_ia_norm]);
    ICP_error = np.array([Rs_error_icp_norm, Ts_error_icp_norm])
    # import code; code.interact(local=locals())

    return IA_error, ICP_error


def main(logfile=None):

    global LOG
    LOG = setlogging(logfile)
    # descriptors = ["FPFH", "SHOT"]
    descriptors = ["FPFH"]
    # niter = [20, 50, 75, 100, 200, 500]
    niter = [500]

    ntrials = 10
    plot_errors = False

    if (plot_errors):
        colors = ['magenta','blue','green', 'red', 'black']
        markers = ['-o', '--*', '-s', '--^']
        figT = plt.figure()
        figR = plt.figure()
        axT = figT.add_subplot(111);
        axR = figR.add_subplot(111);
        figT_detail = plt.figure()
        figR_detail = plt.figure()
        axT_detail = figT_detail.add_subplot(111, aspect=6);
        axR_detail = figR_detail.add_subplot(111, aspect=1100);

        plt.hold(True);
        plt.axis(tight=True);


    IA_error_mean= np.zeros((len(niter), 2));
    IA_error_min= np.zeros((len(niter), 2))
    IA_error_max= np.zeros((len(niter), 2))
    IA_error_median= np.zeros((len(niter), 2))

    ICP_error_mean= np.zeros((len(niter), 2));
    ICP_error_min= np.zeros((len(niter), 2))
    ICP_error_max= np.zeros((len(niter), 2))
    ICP_error_median= np.zeros((len(niter), 2))

    for d_idx in range(0, len(descriptors)):

        descriptor = descriptors[d_idx];

        for iter_idx in range(0,len(niter)):

            IA_error = np.zeros((ntrials, 2));
            ICP_error = np.zeros((ntrials, 2));

            for trial in range(0,ntrials):
              IA_error[trial,:], ICP_error[trial,:] = compute_error(trial, descriptor, niter[iter_idx], 99)

            #Compute mean, max and min
            IA_error_mean[iter_idx, :] = np.mean(IA_error, axis=0)
            ICP_error_mean[iter_idx, :]= np.mean(ICP_error, axis=0)
            IA_error_max[iter_idx, :] = np.max(IA_error, axis=0)
            ICP_error_max[iter_idx, :]= np.max(ICP_error, axis=0)
            IA_error_min[iter_idx, :] = np.min(IA_error, axis=0)
            ICP_error_min[iter_idx, :]= np.min(ICP_error, axis=0)
            IA_error_median[iter_idx, :] = np.median(IA_error, axis=0)
            ICP_error_median[iter_idx, :]= np.median(ICP_error, axis=0)

            import code; code.interact(local=locals())

        if (plot_errors):

            #plot IA, ICP --> missing to to ICP_normals
            axT.errorbar(niter, IA_error_median[:, 1],
                         yerr=[ IA_error_median[:, 1]-IA_error_min[:, 1],
                         IA_error_max[:, 1]- IA_error_median[:, 1]],
                         fmt=markers[2*d_idx], color=colors[2*d_idx],
                         label=descriptor + " FA", capsize=12);
            axT.errorbar(niter, ICP_error_median[:, 1],
                         yerr=[ ICP_error_median[:, 1]-ICP_error_min[:, 1],
                         ICP_error_max[:, 1]- ICP_error_median[:, 1]],
                         fmt=markers[2*d_idx+1], color=colors[2*d_idx+1],
                         label=descriptor + " FA+ICP", capsize=12, ms=14)

            axR.errorbar(niter, IA_error_median[:, 0],
                         yerr=[IA_error_median[:, 0]- IA_error_min[:, 0],
                         IA_error_max[:, 0]-IA_error_median[:, 0]],
                         fmt=markers[2*d_idx], color=colors[2*d_idx],
                         label=descriptor + " FA", capsize=12);
            axR.errorbar(niter, ICP_error_median[:, 0],
                         yerr=[ICP_error_median[:, 0] - ICP_error_min[:, 0],
                         ICP_error_max[:, 0]- ICP_error_median[:, 0]],
                         fmt=markers[2*d_idx+1], color=colors[2*d_idx+1],
                          label=descriptor + " FA+ICP", capsize=12, ms=14)

            #********************Detail Plot***************************
            axT_detail.plot(niter, IA_error_median[:, 1],
                            markers[2*d_idx], color=colors[2*d_idx],
                            label=descriptor + " FA");
            axT_detail.plot(niter, ICP_error_median[:, 1],
                            markers[2*d_idx+1], color=colors[2*d_idx+1],
                            label=descriptor + " FA+ICP", ms=14)

            axR_detail.plot(niter, IA_error_median[:, 0],
                            markers[2*d_idx], color=colors[2*d_idx],
                            label=descriptor + " FA");
            axR_detail.plot(niter, ICP_error_median[:, 0],
                            markers[2*d_idx+1], color=colors[2*d_idx+1],
                            label=descriptor + " FA+ICP", ms=14)


    if (plot_errors):
        axT.set_xlabel('Number of RANSAC_FA Iterations',fontsize= 20);
        axT.set_ylabel('Error (meters)',fontsize= 20);
        axT.set_xlim((0,505) );
        axT.set_yticks(np.arange(0.0,250.0,20));
        # axT.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
        #             ncol=4, mode="expand", borderaxespad=0.)
        axT.legend(loc='upper center', frameon=False);

        figT.savefig("/Users/isa/Experiments/reg3d_eval/downtown_dan/T_error.pdf",
                   transparent=True, pad_inches=5)


        axR.set_xlabel('Number of RANSAC_FA Iterations',fontsize= 20)
        axR.set_ylabel('Error (degrees)', fontsize = 20)
        axR.set_xlim((0, 505))
        axR.set_yticks(np.arange(0.0, np.pi/2 + np.pi/18 , np.pi/18))
        axR.set_yticklabels(np.arange(0, 100, 10))

        axR.legend(loc='upper right', frameon=False);
        figR.savefig("/Users/isa/Experiments/reg3d_eval/downtown_dan/R_error.pdf",
                   transparent=True)


        #********************Detail Plot***************************
        axT_detail.set_xlim((90,210) );
        axT_detail.set_xticks((100,200 ) );
        axT_detail.set_yticks(np.arange(0,25,3));
        axT_detail.set_ylim((0,25))
        figT_detail.savefig("/Users/isa/Experiments/reg3d_eval/downtown_dan/T_detail_error.pdf", transparent=True)


        axR_detail.set_xlim((90,210) );
        axR_detail.set_xticks((100,200 ) );
        axR_detail.set_yticks(np.arange(0.0, 7*np.pi/180 + 5*np.pi/180 , np.pi/180));
        axR_detail.set_yticklabels(np.arange(0, 7, 1))
        axR_detail.set_ylim((0,7*np.pi/180))
        figR_detail.savefig("/Users/isa/Experiments/reg3d_eval/downtown_dan/R_detail_error.pdf", transparent=True)

      # plt.show();


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
    # logger.debug("debug message")
    # logger.info("info message")
    # logger.warn("warn message")
    # logger.error("error message")
    # logger.critical("critical message")

    return logger

if __name__ == '__main__':

    # initialize the parser object:
    parser = argparse.ArgumentParser(description="Export PLY to PCD file")

    # define options here:
    parser.add_argument("-v", "--verbose",      action='store',    type = bool,   dest="verbose",   default=True,  help="Write debug log to log_file")
    parser.add_argument("-L", "--log", dest="logfile", help="write debug log to log_file")

    args = parser.parse_args(argv)

    # set up logging
    if args.verbose:
        status = main(args.logfile)
    else:
        status = main()

    sys.exit(status)
