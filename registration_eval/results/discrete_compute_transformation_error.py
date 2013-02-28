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
The rotation error is computed as the half angle between the normalized
quaternions i.e acos(|<q1,q2>|) in [0, pi/2]
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

sys.path.append(os.pardir)
import reg3d

if __name__ == '__main__':

    # root_dir = "/Users/isa/Experiments/reg3d_eval/downtown_2006";
    # geo_tfile ="/data/lidar_providence/downtown_offset-1-financial-dan-Hs.txt"

    # root_dir = "/Users/isa/Experiments/reg3d_eval/capitol_2006";
    # geo_tfile ="/data/lidar_providence/capitol/capitol-dan_Hs.txt"

    # root_dir = "/Users/isa/Experiments/reg3d_eval/scili_3_12";
    # geo_tfile ="/data/lidar_providence/east_side/scili_3_12_Hs.txt"

    # root_dir = "/Users/isa/Experiments/reg3d_eval/res_east_side";
    # geo_tfile ="/data/lidar_providence/east_side/res_east_side_Hs.txt"

    root_dir = "/Users/isa/Experiments/reg3d_eval/res_middletown";
    geo_tfile ="/data/lidar_providence/middle_town_residential/residential_Hs.txt"


    # plot_errors = True
    # descriptors = ["FPFH", "SHOT"]
    # niter = [20, 50, 75, 100, 200, 500]

    plot_errors = False
    descriptors = ["SHOT"]
    niter = [500]

    radius = 30
    percentile = 99
    ntrials = 10

    if (plot_errors):
        colors = ['magenta','blue','green', 'red', 'black']
        markers = ['-o', '--*', '-s', '--^']
        figT = plt.figure()
        figR = plt.figure()
        axT = figT.add_subplot(111);
        axR = figR.add_subplot(111);
        figT_detail = plt.figure()
        figR_detail = plt.figure()
        axT_detail = figT_detail.add_subplot(111);
        axR_detail = figR_detail.add_subplot(111);

        plt.hold(True);
        plt.axis(tight=True);


    IA_error_mean= np.zeros((len(niter), 3));
    IA_error_min= np.zeros((len(niter), 3))
    IA_error_max= np.zeros((len(niter), 3))
    IA_error_median= np.zeros((len(niter), 3))

    ICP_error_mean= np.zeros((len(niter), 3));
    ICP_error_min= np.zeros((len(niter), 3))
    ICP_error_max= np.zeros((len(niter), 3))
    ICP_error_median= np.zeros((len(niter), 3))

    for d_idx in range(0, len(descriptors)):

        descriptor = descriptors[d_idx];
        print "Descriptor: ", descriptor

        for iter_idx in range(0,len(niter)):

            print "***** Iter: " , niter[iter_idx]

            IA_error = np.zeros((ntrials, 3));
            ICP_error = np.zeros((ntrials, 3));

            for trial in range(0,ntrials):

              trial_root_dir = root_dir + "/trial_" + str(trial)

              print "***** Trial: " , trial
              IA_error[trial,:], ICP_error[trial,:] = reg3d.transformation_error(root_dir = trial_root_dir,
                                                                                 descriptor_type = descriptor,
                                                                                 percentile = percentile,
                                                                                 nr_iterations = niter[iter_idx],
                                                                                 gt_fname = "Hs.txt",
                                                                                 geo_tfile = geo_tfile)

            print "IA:"
            print IA_error
            print "ICP Error:"
            print ICP_error

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
            axT.errorbar(niter, IA_error_median[:, 2],
                         yerr=[ IA_error_median[:, 2]-IA_error_min[:, 2],
                         IA_error_max[:, 2]- IA_error_median[:, 2]],
                         fmt=markers[2*d_idx], color=colors[2*d_idx],
                         label=descriptor + " FA", capsize=12);
            axT.errorbar(niter, ICP_error_median[:, 2],
                         yerr=[ ICP_error_median[:, 2]-ICP_error_min[:, 2],
                         ICP_error_max[:, 2]- ICP_error_median[:, 2]],
                         fmt=markers[2*d_idx+1], color=colors[2*d_idx+1],
                         label=descriptor + " FA+ICP", capsize=12, ms=14)

            axR.errorbar(niter, IA_error_median[:, 1],
                         yerr=[IA_error_median[:, 1]- IA_error_min[:, 1],
                         IA_error_max[:, 1]-IA_error_median[:, 1]],
                         fmt=markers[2*d_idx], color=colors[2*d_idx],
                         label=descriptor + " FA", capsize=12);
            axR.errorbar(niter, ICP_error_median[:, 1],
                         yerr=[ICP_error_median[:, 1] - ICP_error_min[:, 1],
                         ICP_error_max[:, 1]- ICP_error_median[:, 1]],
                         fmt=markers[2*d_idx+1], color=colors[2*d_idx+1],
                          label=descriptor + " FA+ICP", capsize=12, ms=14)

            #********************Detail Plot***************************
            axT_detail.plot(niter[3:6], IA_error_median[3:6, 2],
                            markers[2*d_idx], color=colors[2*d_idx],
                            label=descriptor + " FA");
            axT_detail.plot(niter[3:6], ICP_error_median[3:6, 2],
                            markers[2*d_idx+1], color=colors[2*d_idx+1],
                            label=descriptor + " FA+ICP", ms=14)

            axR_detail.plot(niter[3:6], IA_error_median[3:6, 1],
                            markers[2*d_idx], color=colors[2*d_idx],
                            label=descriptor + " FA");
            axR_detail.plot(niter[3:6], ICP_error_median[3:6, 1],
                            markers[2*d_idx+1], color=colors[2*d_idx+1],
                            label=descriptor + " FA+ICP", ms=14)


    if (plot_errors):
        axT.set_xlabel('Number of FA-RANSAC Iterations',fontsize= 20);
        axT.set_ylabel('Error (meters)',fontsize= 20);
        axT.set_xlim((0,505) );
        # axT.set_yticks(np.arange(0.0,250.0,20));
        # axT.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
        #             ncol=4, mode="expand", borderaxespad=0.)
        axT.legend(loc='upper right', frameon=False);

        figT.savefig( root_dir + "/T_error.pdf",
                   transparent=True, pad_inches=5)


        axR.set_xlabel('Number of FA-RANSAC Iterations',fontsize= 20)
        axR.set_ylabel('Error (degrees)', fontsize = 20)
        axR.set_xlim((0, 505))
        # axR.set_yticks(np.arange(0.0, np.pi/2 + np.pi/18 , np.pi/18))
        # axR.set_yticklabels(np.arange(0, 100, 10))

        axR.legend(loc='upper right', frameon=False);
        figR.savefig( root_dir + "/R_error.pdf",
                   transparent=True)


        #********************Detail Plot***************************
        axT_detail.set_xlim((90,510) );

        # axT_detail.set_xticks(np.arange(100,510,100) );
        # axT_detail.set_yticks(np.arange(0,25,3));
        # axT_detail.set_ylim((0,25))
        figT_detail.savefig( root_dir + "/T_detail_error.pdf", transparent=True)


        axR_detail.set_xlim((90,510) );
        axR_detail.set_xticks(np.arange(100,510,100) );
        # axR_detail.set_yticks(np.arange(0.0, 7*np.pi/180 + 5*np.pi/180 , np.pi/180));
        # axR_detail.set_yticklabels(np.arange(0, 7, 1))
        # axR_detail.set_ylim((0,7*np.pi/180))
        figR_detail.savefig( root_dir + "/R_detail_error.pdf", transparent=True)

    # plt.show()


