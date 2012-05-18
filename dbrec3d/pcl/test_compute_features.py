#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo

"""
import os
import sys

from dbrec3d_pcl_adaptor import *

file_in = "/data/helicopter_providence_3_12/site_12/gauss_233_normals_t90_scili.ply"

resolution=0.0022;
radius=30*resolution;

#file_out = "/data/helicopter_providence_3_12/site_12/test_fpfh.pcd"
#compute_descriptor(file_in, file_out, radius, "FPFH");

#file_out = "/data/helicopter_providence_3_12/site_12/test_shot.txt"
#compute_descriptor(file_in, file_out, radius, "SHOT");

file_out = "/data/helicopter_providence_3_12/site_12/test_sc.txt"
compute_descriptor(file_in, file_out, radius, "ShapeContext");