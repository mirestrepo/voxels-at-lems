#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Maria Isabel Restrepo
# @Date:   2014-01-19 12:36:19
# @Last Modified by:   Maria Isabel Restrepo
# @Last Modified time: 2014-01-19 13:23:03


import numpy as np
from numpy.linalg import inv
import sys, os
sys.path.append(os.pardir)
import reg3d_transformations as reg3d_T

reg_dir = "/Users/isa/Dropbox/MultiModalRegPaper"

sites = ["BH_2006", "BH_VSI", "capitol_2006", "capitol_2011", "downtown_2006", "downtown_2011"];
percent = 95;

for site in sites:

    for trial in range(0,5):

        print "Processing Site: " + site + " Trial: " + str(trial)

        noise_Tfile_base = reg_dir + "/ground_truth/rand_t/H_" + str(trial)
        inv_noise_Tfile_base = noise_Tfile_base + "_inv"

        noise_Tfile = noise_Tfile_base + ".txt"

        matrix_noise_Tfile = reg_dir + "/ground_truth/rand_t/H_" + str(trial) +"_matrix.txt"

        noise_Tform = reg3d_T.gt_transformation(noise_Tfile);

        #save as matrix
        noise_Tform.save_to_file(noise_Tfile_base)

        #inverse transformation
        inv_noise_Tform = reg3d_T.gt_transformation(inv(noise_Tform.Hs))
        inv_noise_Tform.save_to_file(inv_noise_Tfile_base)

        # S_inv = (1.0/noise_Tform.scale);
        # R_inv = noise_Tform.Rs.T;
        # T_inv =  R_inv.dot((noise_Tform.scale*noise_Tform.Ts));

        # print inv_noise_Tform.Hs
        # print S_inv
        # print R_inv
        # print T_inv

