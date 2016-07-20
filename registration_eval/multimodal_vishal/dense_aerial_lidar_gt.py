#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Maria Isabel Restrepo
# @Date:   2014-01-23 16:10:10
# @Last Modified by:   Maria Isabel Restrepo
# @Last Modified time: 2014-01-23 16:47:08
# Script to assemble the ground truth as run by Vishal


import numpy as np
import sys, os
sys.path.append(os.pardir)
import reg3d_transformations as reg3d_T
from numpy.linalg import inv

reg_dir = "/Users/isa/Dropbox/MultiModalRegPaper"

sites = ["BH_2006", "BH_VSI", "capitol_2006", "capitol_2011", "downtown_2006", "downtown_2011"];
percent = 95;

for site in sites:

    for trial in range(0,5):

        print "Processing Site: " + site + " Trial: " + str(trial)

        geo_Tfile  = reg_dir + "/ground_truth/aerial-lidar-demeaned/" + site + "/Hs_geo.txt"
        noise_Tfile = reg_dir + "/ground_truth/rand_t/H_" + str(trial) +".txt"
        dir_out = file_out = reg_dir + "/ground_truth/DenseResults/Aerial2Lidar/" + site

        if not os.path.exists(dir_out):
          print "Output dir not found - creating one ", dir_out
          os.makedirs(dir_out)

        tform_file_out = dir_out + "/H" + str(trial)

        GEO_Tform = reg3d_T.gt_transformation(geo_Tfile);
        noise_Tform = reg3d_T.gt_transformation(noise_Tfile);

        final_Hs = (noise_Tform.Hs.dot(GEO_Tform.Hs))

        final_Tform = reg3d_T.gt_transformation(final_Hs)

        #save the transform
        final_Tform.save_to_file(tform_file_out);




