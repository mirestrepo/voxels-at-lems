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

sys.path.append(os.pardir)
import reg3d



if __name__ == '__main__':

    # site = "BH"
    # flights = [["CVG","2006"]]
    # geo_tfile = "/Users/isa/Experiments/reg3d_eval/BH_2006/original/Hs_geo.txt"


    # site = "downtown"
    # flights = [["2011","2006"],["CVG","2006"]]
    # geo_tfile = "/data/lidar_providence/downtown_offset-1-financial-dan-Hs.txt"


    site = "capitol"
    flights = [["2011","2006"]]
    geo_tfile = "/data/lidar_providence/capitol/capitol-dan_Hs.txt"
    # flights = [["2006","2011"]]
    # geo_tfile = "/Users/isa/Experiments/reg3d_eval/capitol_2011/original/Hs_geo.txt"


    root_dir = "/Users/isa/Experiments/reg3d_eval";
    radius = 30
    nr_iter = 500
    cropped = True


    IA_errors_R = np.zeros((3, len(flights)*2));
    IA_errors_T = np.zeros((3, len(flights)*2));
    ICP_errors_R = np.zeros((3, len(flights)*2));
    ICP_errors_T = np.zeros((3, len(flights)*2));



    for f in range(0, len(flights)):

        flight = flights[f][0]
        gt_flight = flights[f][1]
        trial_root_dir = root_dir + "/" + site + "_" +  flight + "/original"
        gt_root_dir = root_dir + "/" + site + "_" +  gt_flight + "/original"
        gt_fname = flight + "-" + gt_flight + "_Hs.txt"

        if cropped:
          descriptor_string = "descriptors_cropped"
          # aux_output_string = flight + "-" + gt_flight + "-cropped"
          #Note: when I run the experiment the output files were labeled by mistake src-src
          aux_output_string = flight + "-" + flight + "-cropped"


        else:
          descriptor_string = "descriptors"
          aux_output_string = flight + "-" + gt_flight

        IA_error_FPFH_99, ICP_error_FPFH_99 = reg3d.transformation_error(root_dir = trial_root_dir,
                                                         descriptor_type = "FPFH",
                                                         percentile = 99,
                                                         nr_iterations = nr_iter,
                                                         aux_output_string = aux_output_string,
                                                         gt_fname = gt_fname,
                                                         geo_tfile = geo_tfile)
        IA_error_FPFH_95, ICP_error_FPFH_95 = reg3d.transformation_error(root_dir = trial_root_dir,
                                                         descriptor_type = "FPFH",
                                                         percentile = 95,
                                                         nr_iterations = nr_iter,
                                                         aux_output_string = aux_output_string,
                                                         gt_fname = gt_fname,
                                                         geo_tfile = geo_tfile)
        IA_error_FPFH_90, ICP_error_FPFH_90 = reg3d.transformation_error(root_dir = trial_root_dir,
                                                         descriptor_type = "FPFH",
                                                         percentile = 90,
                                                         nr_iterations = nr_iter,
                                                         aux_output_string = aux_output_string,
                                                         gt_fname = gt_fname,
                                                         geo_tfile = geo_tfile)
        IA_error_SHOT_99, ICP_error_SHOT_99 = reg3d.transformation_error(root_dir = trial_root_dir,
                                                         descriptor_type = "SHOT",
                                                         percentile = 99,
                                                         nr_iterations = nr_iter,
                                                         aux_output_string = aux_output_string,
                                                         gt_fname = gt_fname,
                                                         geo_tfile = geo_tfile)
        IA_error_SHOT_95, ICP_error_SHOT_95 = reg3d.transformation_error(root_dir = trial_root_dir,
                                                         descriptor_type = "SHOT",
                                                         percentile = 95,
                                                         nr_iterations = nr_iter,
                                                         aux_output_string = aux_output_string,
                                                         gt_fname = gt_fname,
                                                         geo_tfile = geo_tfile)
        IA_error_SHOT_90, ICP_error_SHOT_90 = reg3d.transformation_error(root_dir = trial_root_dir,
                                                         descriptor_type = "SHOT",
                                                         percentile = 90,
                                                         nr_iterations = nr_iter,
                                                         aux_output_string = aux_output_string,
                                                         gt_fname = gt_fname,
                                                         geo_tfile = geo_tfile)


        IA_errors_R[0][f*2] = IA_error_FPFH_99[1]
        IA_errors_T[0][f*2] = IA_error_FPFH_99[2]
        ICP_errors_R[0][f*2] = ICP_error_FPFH_99[1]
        ICP_errors_T[0][f*2] = ICP_error_FPFH_99[2]

        IA_errors_R[1][f*2] = IA_error_FPFH_95[1]
        IA_errors_T[1][f*2] = IA_error_FPFH_95[2]
        ICP_errors_R[1][f*2] = ICP_error_FPFH_95[1]
        ICP_errors_T[1][f*2] = ICP_error_FPFH_95[2]

        IA_errors_R[2][f*2] = IA_error_FPFH_90[1]
        IA_errors_T[2][f*2] = IA_error_FPFH_90[2]
        ICP_errors_R[2][f*2] = ICP_error_FPFH_90[1]
        ICP_errors_T[2][f*2] = ICP_error_FPFH_90[2]

        IA_errors_R[0][f*2 + 1] = IA_error_SHOT_99[1]
        IA_errors_T[0][f*2 + 1] = IA_error_SHOT_99[2]
        ICP_errors_R[0][f*2 + 1] = ICP_error_SHOT_99[1]
        ICP_errors_T[0][f*2 + 1] = ICP_error_SHOT_99[2]

        IA_errors_R[1][f*2 + 1] = IA_error_SHOT_95[1]
        IA_errors_T[1][f*2 + 1] = IA_error_SHOT_95[2]
        ICP_errors_R[1][f*2 + 1] = ICP_error_SHOT_95[1]
        ICP_errors_T[1][f*2 + 1] = ICP_error_SHOT_95[2]

        IA_errors_R[2][f*2 + 1] = IA_error_SHOT_90[1]
        IA_errors_T[2][f*2 + 1] = IA_error_SHOT_90[2]
        ICP_errors_R[2][f*2 + 1] = ICP_error_SHOT_90[1]
        ICP_errors_T[2][f*2 + 1] = ICP_error_SHOT_90[2]

print "Site: ", site
print "Rotation errors "

print " \\\\\n".join([" & ".join(map(str,line)) for line in IA_errors_R])

print "Rotation errors ICP "

print " \\\\\n".join([" & ".join(map(str,line)) for line in ICP_errors_R])

print "Translation errors "
print " \\\\\n".join([" & ".join(map(str,line)) for line in IA_errors_T])

print "Translation errors ICP"
print " \\\\\n".join([" & ".join(map(str,line)) for line in ICP_errors_T])


# print " \\\\\n\\hline \\\n".join(["\\rowcolor{white} \\\n \\multirow{2}{*}{Site }&FA &" + " & ".join(map(str,line1) ) + "\\\\\n \\cline{2-5}\\\n &FA+ICP & " + " & ".join(map(str,line2) ) for line1, line2 in zip(IA_errors_R*(180/np.pi), ICP_errors_R*(180/np.pi))])


# print "Translation errors "

# print " \\\\\n\\hline \\\n".join(["\\rowcolor{white} \\\n \\multirow{2}{*}{Site}&FA &" + " & ".join(map(str,line1) ) + "\\\\\n \\cline{2-5}\\\n &FA+ICP & " + " & ".join(map(str,line2) ) for line1, line2 in zip(IA_errors_T, ICP_errors_T)])



