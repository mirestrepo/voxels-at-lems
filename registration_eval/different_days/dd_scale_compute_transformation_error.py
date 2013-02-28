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
    # flight_string = [["CVG","2006"]]
    # geo_tfile = "/Users/isa/Experiments/reg3d_eval/BH_2006/original/Hs_geo.txt"


    # site = "downtown"
    # flight_string = [["2011","2006"]]
    # geo_tfile = "/data/lidar_providence/downtown_offset-1-financial-dan-Hs.txt"


    site = "capitol"
    # flight_string = [["2011","2006"]]
    # geo_tfile = "/data/lidar_providence/capitol/capitol-dan_Hs.txt"

    flight_string = [["2006","2011"]]
    geo_tfile = "/Users/isa/Experiments/reg3d_eval/capitol_2011/original/Hs_geo.txt"



    root_dir = "/Users/isa/Experiments/reg3d_eval";
    radius = 30
    nr_iter = 500
    cropped = True
    sample_distance = [1,5,10]

    nsamples = [3,6,10]
    compute_scale = True
    bound_scale = True
    bound_percentile = 20



    IA_errors_S = np.zeros((len(sample_distance), len(nsamples)*2));
    IA_errors_R = np.zeros((len(sample_distance), len(nsamples)*2));
    IA_errors_T = np.zeros((len(sample_distance), len(nsamples)*2));
    ICP_errors_S = np.zeros((len(sample_distance), len(nsamples)*2));
    ICP_errors_R = np.zeros((len(sample_distance), len(nsamples)*2));
    ICP_errors_T = np.zeros((len(sample_distance), len(nsamples)*2));



    for fs in range(0, len(flight_string)):

        src_str = flight_string[fs][0]
        tgt_str = flight_string[fs][1]
        trial_root_dir = root_dir + "/" + site + "_" +  src_str + "/original"
        gt_root_dir = root_dir + "/" + site + "_" +  tgt_str + "/original"
        gt_fname = src_str + "-" + tgt_str + "_Hs.txt"



        descriptor_string = "descriptors"
        aux_output_string = src_str + "-" + src_str
        # aux_output_string = src_str + "-" + src_str #+ "_" +  str(nsamples) + "_" + str(sample_distance)
        #Note: when I run the experiment the output files were labeled by mistake src-src
        # this is the correct name

        for sd in range(0, len(sample_distance)):

            for ns in range(0, len(nsamples)):


                if compute_scale:
                    aux_output_string = src_str + "-" + tgt_str + "_" +  str(nsamples[ns]) + "_" + str(sample_distance[sd])

                if cropped:
                    descriptor_string = descriptor_string + "_cropped"
                    aux_output_string = aux_output_string + "-cropped"


                if compute_scale:
                    aux_output_string = aux_output_string + "_scale"
                    if bound_scale:
                        aux_output_string = aux_output_string + "_bound_" + str(bound_percentile)

                print descriptor_string, aux_output_string

                IA_error_FPFH, ICP_error_FPFH = reg3d.transformation_error( root_dir = trial_root_dir,
                                                                            descriptor_type = "FPFH",
                                                                            percentile = 99,
                                                                            nr_iterations = nr_iter,
                                                                            aux_output_string = aux_output_string,
                                                                            gt_fname = gt_fname,
                                                                            geo_tfile = geo_tfile,
                                                                            nsamples          = nsamples[ns],
                                                                            sample_distance   = sample_distance[sd],
                                                                            compute_scale     = True)

                IA_error_SHOT, ICP_error_SHOT = reg3d.transformation_error( root_dir = trial_root_dir,
                                                                            descriptor_type = "SHOT",
                                                                            percentile = 99,
                                                                            nr_iterations = nr_iter,
                                                                            aux_output_string = aux_output_string,
                                                                            gt_fname = gt_fname,
                                                                            geo_tfile = geo_tfile,
                                                                            nsamples          = nsamples[ns],
                                                                            sample_distance   = sample_distance[sd],
                                                                            compute_scale     = True)
                IA_errors_S[sd][ns*2] = IA_error_FPFH[0]
                IA_errors_R[sd][ns*2] = IA_error_FPFH[1]
                IA_errors_T[sd][ns*2] = IA_error_FPFH[2]

                ICP_errors_S[sd][ns*2] = ICP_error_FPFH[0]
                ICP_errors_R[sd][ns*2] = ICP_error_FPFH[1]
                ICP_errors_T[sd][ns*2] = ICP_error_FPFH[2]

                IA_errors_S[sd][ns*2 + 1] = IA_error_SHOT[0]
                IA_errors_R[sd][ns*2 + 1] = IA_error_SHOT[1]
                IA_errors_T[sd][ns*2 + 1] = IA_error_SHOT[2]

                ICP_errors_S[sd][ns*2 + 1] = ICP_error_SHOT[0]
                ICP_errors_R[sd][ns*2 + 1] = ICP_error_SHOT[1]
                ICP_errors_T[sd][ns*2 + 1] = ICP_error_SHOT[2]


        print "Site: ", site
        print "Flight: ", (src_str + "-" + tgt_str)

        print "Scale errors "

        print " \\\\\n".join([" & ".join(map(str,line)) for line in IA_errors_S])

        print "Scale errors ICP "

        print " \\\\\n".join([" & ".join(map(str,line)) for line in ICP_errors_S])

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



