#!/usr/bin/env python
# encoding: utf-8
"""
compute_transformation_error.py

Created by Maria Isabel Restrepo on 2012-09-24.
Copyright (c) 2012 . All rights reserved.
This script computes the distances betweeen an estimated similarity transformation and its ground trutrransformation is used to transform a "source" coordinate system into a "target coordinate system"
To compute the error between the translations, the L2 norm diference translation vectors in the
"source coordinate system" is computed. Since distances are preserved under R and T, only scale is applied.
The rotation error is computed as the half angle between the normalized queternions i.e acos(|<q1,q2>|) in [0, pi/2]
This script was intended to use with Vishal's results
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

    # fname = "/Users/isa/Dropbox/data/registration_for_vj/capitol_2011/original/2011-2006_Hs_matrix_vj_dense.txt"
    # gt_fname = "/Users/isa/Dropbox/data/registration_for_vj/capitol_2011/original/2011-2006_Hs.txt"
    # geo_fname ="/Users/isa/Dropbox/data/registration_for_vj/capitol_2006/original/Hs_geo.txt"
    # error = reg3d.transformation_error_general(fname = fname,
    #                                            gt_fname = gt_fname,
    #                                            geo_fname = geo_fname )

    # # Error (S,R,T) 1.39523511977e-06 0.802221070301 2.98789826592

    # fname = "/Users/isa/Dropbox/data/registration_for_vj/downtown_2006/original/2006-2011_Hs_matrix_vj_dense.txt"
    # gt_fname = "/Users/isa/Dropbox/data/registration_for_vj/downtown_2006/original/2006-2011_Hs.txt"
    # geo_fname ="/Users/isa/Dropbox/data/registration_for_vj/capitol_2011/original/Hs_geo.txt"
    # error = reg3d.transformation_error_general(fname = fname,
    #                                            gt_fname = gt_fname,
    #                                            geo_fname = geo_fname )

    # # Error (S,R,T) 5.31970689721e-08 0.808909241082 4.83449482984

    # fname = "/Users/isa/Dropbox/data/registration_for_vj/BH_VSI/original/f4-2006_Hs_matrix_vj_dense.txt"
    # gt_fname = "/Users/isa/Dropbox/data/registration_for_vj/BH_VSI/original/f4-2006_Hs.txt"
    # geo_fname ="/Users/isa/Dropbox/data/registration_for_vj/BH_2006/original/Hs_geo.txt"
    # error = reg3d.transformation_error_general(fname = fname,
    #                                            gt_fname = gt_fname,
    #                                            geo_fname = geo_fname )

    # # Error (S,R,T) 2.57980939389e-07 0.763324882652 4.79257669203