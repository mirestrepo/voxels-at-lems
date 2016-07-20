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
icp_result_dir = reg_dir + "/icp_results/lidar-aerial2"
result_summary_file = icp_result_dir + "/summary.txt"

sites = ["BH_2006", "BH_VSI", "capitol_2006", "capitol_2011", "downtown_2006", "downtown_2011"];
l_sites = ["BH", "BH", "capitol", "capitol", "downtown", "downtown"]
percent = 95;
ntrials = 5
error = np.zeros((ntrials, 3, len(sites)));
inital_error = np.array([[ 0.0, 3.64969371,  3.881038  ],
                         [ 0.0, 3.71314362,  6.67001667],
                         [ 0.0, 3.71530045,  7.37906836],
                         [ 0.0, 4.11227278,  6.20087232],
                         [ 0.0, 3.84084958,  2.51475658]])

for site_idx in range(0, len(sites)):
    for trial in range(0,5):
        print 'Trial: ' + str(trial)
        results_dir = icp_result_dir + "/" + sites[site_idx ] + "/H_" + str(trial)

        t_fname = results_dir + "/icp_output_tform_" + str(percent) + ".txt"
        gt_fname = reg_dir + "/ground_truth/rand_t/H_" + str(trial) + ".txt"


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
    Tfos.write("Errors Reduction:\n")
    reduction_error = inital_error[:,:] - error[:,:,site_idx].reshape((ntrials, 3))
    mean_reduction_error = np.mean((reduction_error[:,:]), axis=0)
    std_reduction_error = np.std((reduction_error[:,:]), axis=0)
    np.savetxt( Tfos , reduction_error, fmt='%.7g')
    Tfos.write("Mean Reduction:\n")
    np.savetxt( Tfos , mean_reduction_error.reshape((1,3))  , fmt='%.7g', delimiter=' ')
    Tfos.write("Std Reduction:\n")
    np.savetxt( Tfos , std_reduction_error.reshape((1,3))  , fmt='%.7g', delimiter=' ')

Tfos.close()


