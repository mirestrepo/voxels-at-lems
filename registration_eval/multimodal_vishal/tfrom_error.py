#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Maria Isabel Restrepo
# @Date:   2014-01-17 16:38:15
# Script to find the average ICP alignment error



import os
import sys
import numpy as np
from scipy import stats
sys.path.append(os.pardir)
VOXELS_AT_LEMS_VPCL = "../../vpcl"
sys.path.append(VOXELS_AT_LEMS_VPCL)

import vpcl_setup_module
vpcl_setup_module.setUpPaths(configuration = 'Release')

import reg3d

reg_dir = "/Users/isa/Dropbox/MultiModalRegPaper"
result_summary_file = reg_dir + "/icp_results/aerial-lidar/summary.txt"

sites = ["BH_2006", "BH_VSI", "capitol_2006", "capitol_2011", "downtown_2006", "downtown_2011"];
l_sites = ["BH", "BH", "capitol", "capitol", "downtown", "downtown"]
percent = 95;
ntrials = 5
error = np.zeros((ntrials, 3, len(sites)));

for site_idx in range(0, len(sites)):
    for trial in range(0,5):
        print 'Trial: ' + str(trial)
        results_dir = reg_dir + "/icp_results/aerial-lidar/" + sites[site_idx ] + "/H_" + str(trial)

        t_fname = results_dir + "/icp_output_tform_" + str(percent) + ".txt"
        gt_fname = reg_dir + "/ground_truth/rand_t/H_" + str(trial) + "_inv.txt"


        error[trial,:, site_idx ] = reg3d.transformation_error_general(fname = t_fname,
                                                                         gt_fname = gt_fname)


Tfos = open(result_summary_file, 'w')


for site_idx in range(0, len(sites)):
    print "-----------------------------------------------------"
    print "*********** Errors " + sites[site_idx] + " *************"
    print "-----------------------------------------------------"

    print error[:,:,site_idx]

    print 'Mean:'
    mean_error = np.mean(abs(error[:,:,site_idx]), axis=0)
    print mean_error
    print 'Std:'
    std_error = np.std(abs(error[:,:,site_idx]), axis=0)
    print std_error

    Tfos.write("-----------------------------------------------------\n")
    Tfos.write("*********** Errors " + sites[site_idx] + " *************\n")
    Tfos.write("-----------------------------------------------------\n")
    np.savetxt( Tfos , error[:,:,site_idx], fmt='%.7g')
    Tfos.write("Mean:\n")
    np.savetxt( Tfos , mean_error.reshape((1,3))  , fmt='%.7g', delimiter=' ')
    Tfos.write("Std:\n")
    np.savetxt( Tfos , std_error.reshape((1,3))  , fmt='%.7g', delimiter=' ')


Tfos.close()


