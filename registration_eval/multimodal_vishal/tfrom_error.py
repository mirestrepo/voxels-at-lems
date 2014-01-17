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


site_idx = 0;

reg_dir = "/Users/isa/Dropbox/MultiModalRegPaper"

sites = ["BH_2006", "BH_VSI", "capitol_2006", "capitol_2011", "downtown_2006", "downtown_2011"];
l_sites = ["BH", "BH", "capitol", "capitol", "downtown", "downtown"]
percent = 95;
ntrials = 5
error = np.zeros((ntrials-1, 3));

for trial in range(0,1):
    print 'Trial: ' + str(trial)
    results_dir = reg_dir + "/icp_results/aerial-lidar/" + sites[site_idx ] + "/H_" + str(trial)

    t_fname = results_dir + "/icp_output_tform_" + str(percent) + ".txt"
    gt_fname = reg_dir + "/ground_truth/rand_t/H_" + str(trial) + ".txt"


    error[trial-1,:] = reg3d.transformation_error_general(fname = t_fname,
                                                          gt_fname = gt_fname)

print 'Errors:'
print error

print 'Mean:'
print np.mean(abs(error), axis=0)
print 'Std:'
print np.std(abs(error), axis=0)
