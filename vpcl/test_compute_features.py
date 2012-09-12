#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo
July 27, 2012
"""
import os
import sys
import time

time.sleep(30)

sys.path.append("/Projects/vpcl/vpcl/pyscripts")
#sys.path.append("/Projects/vpcl/bin/lib/Debug")
sys.path.append("/Projects/vpcl/bin_make/Debug/lib")


from vpcl_adaptor import *

file_in = "/data/helicopter_providence_3_12/site_12/gauss_233_normals_t90_scili.ply"

resolution=0.0022;
radius=30*resolution;

file_out = "/data/helicopter_providence_3_12/site_12/test_vpcl_fpfh.pcd"
compute_descriptor(file_in, file_out, radius, "FPFH");

#file_out = "/data/helicopter_providence_3_12/site_12/test_vpcl_shot.txt"
#compute_descriptor(file_in, file_out, radius, "SHOT");

#file_out = "/data/helicopter_providence_3_12/site_12/test_vpcl_sc.txt"
#compute_descriptor(file_in, file_out, radius, "ShapeContext");