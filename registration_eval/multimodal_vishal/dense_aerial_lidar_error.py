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
dense_dir = reg_dir + "/DenseResults/aerial2lidar/no_scale"
result_summary_file = dense_dir + "/summary.txt"

sites_vj = ["BH_06", "BH_VSI", "Capitol_06", "Capitol_11", "Downtown_06", "Downtown_11"];
sites_isa = ["BH_2006", "BH_VSI", "capitol_2006", "capitol_2011", "downtown_2006", "downtown_2011"];

file_base = ["06_lidar_est", "VSI_lidar_est", "capitol06_lidar_est", "capitol11_lidar_est", "downtown06_lidar_est", "downtown11_lidar_est"]
percent = 95;
ntrials = 5
error = np.zeros((ntrials, 3, len(sites_vj)));
inital_error = np.array([[ 0.0, 3.64969371,  3.881038  ],
                         [ 0.0, 3.71314362,  6.67001667],
                         [ 0.0, 3.71530045,  7.37906836],
                         [ 0.0, 4.11227278,  6.20087232],
                         [ 0.0, 3.84084958,  2.51475658]])

for site_idx in range(0, len(sites_vj)):
    for trial in range(0,5):
        print 'Trial: ' + str(trial)
        results_dir = dense_dir + "/" + sites_vj[site_idx ]

        t_fname = results_dir + "/" + file_base[site_idx] + "_H" + str(trial) + ".txt"
        gt_fname = reg_dir + "/ground_truth/aerial-lidar-demeaned/" + sites_isa[site_idx] + "/Hs_geo_matrix.txt"


        error[trial,:, site_idx ] = reg3d.transformation_error_general(fname = t_fname,
                                                                       gt_fname = gt_fname)


Tfos = open(result_summary_file, 'w')


for site_idx in range(0, len(sites_vj)):
    print "-----------------------------------------------------"
    print "*********** Errors " + sites_vj[site_idx] + " *************"
    print "-----------------------------------------------------"

    print error[:,:,site_idx]

    print 'Mean:'
    mean_error = np.mean(abs(error[:,:,site_idx]), axis=0)
    print mean_error
    print 'Std:'
    std_error = np.std(abs(error[:,:,site_idx]), axis=0)
    print std_error

    Tfos.write("-----------------------------------------------------\n")
    Tfos.write("*********** Errors " + sites_vj[site_idx] + " *************\n")
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


