#!/usr/bin/env python
# encoding: utf-8
"""
Created by Maria Isabel Restrepo on 2013-1-6.
Copyright (c) 2012 . All rights reserved.

A script to set up a small "common bounding box"
"""


import sys
import os
sys.path.append(os.pardir)

import reg3d_transformations as reg3d_T
import numpy as np
from numpy import linalg as LA
import transformations as tf

PLY_UTIL = "/Projects/voxels-at-lems-git/ply_util"
VOXELS_AT_LEMS_VPCL = "/Projects/voxels-at-lems-git/vpcl"

sys.path.append(PLY_UTIL)
sys.path.append(VOXELS_AT_LEMS_VPCL)

import thresh_ply as ply_util
import vpcl_compute_omp_descriptors as vpcl_descriptors

njobs=8
radius=30
percentile=99


#******************** BH ********************
cvg_root = "/Users/isa/Experiments/reg3d_eval/BH_CVG/original"

#Smallest coverage area is f2
#A good bounding box is given by
thresh = False


XCVGF4 = [-5.0,5.0]
YCVGF4 = [-4,4]
ZCVGF4 = [-2,2.3]

vi = 0
bboxCVGF4 = np.zeros((4,8))
for i in range(0,len(XCVGF4)):
    for j in range(0,len(YCVGF4)):
        for k in range(0,len(ZCVGF4)):
            bboxCVGF4[:,vi] = np.array([XCVGF4[i],YCVGF4[j],ZCVGF4[k],1])
            vi = vi+1

minCVGF4 = np.min(bboxCVGF4, axis=1)
maxCVGF4 = np.max(bboxCVGF4, axis=1)

print "CVGF4"
print minCVGF4
print maxCVGF4

#Load f4-CVGF4
f4_2006_file = cvg_root + "/f4-2006_Hs.txt"
f4_2006 = reg3d_T.gt_transformation(f4_2006_file)

bbox2006 = (f4_2006.Hs).dot(bboxCVGF4)

min2006 = np.min(bbox2006, axis=1)
max2006 = np.max(bbox2006, axis=1)

print "2006"
print bbox2006
print bbox2006

#Crop and threshold CVGF4
sceneroot = cvg_root;
file_in = sceneroot + "/gauss_233_normals.ply";
file_out = sceneroot + "/gauss_233_normals_cropped.ply"
if thresh:
    ply_util.thresh_bbox(file_in, file_out, minCVGF4, maxCVGF4)

file_in = sceneroot + "/gauss_233_normals_cropped.ply";
basename_out = sceneroot + "/gauss_233_normals_pvn_cropped"
if thresh:
    ply_util.thresh_pvn(file_in, basename_out)
else:
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "SHOT", "gauss_233_normals_pvn_cropped", radius, njobs, percentile, True, "descriptors_cropped")
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "FPFH", "gauss_233_normals_pvn_cropped", radius, njobs, percentile, True, "descriptors_cropped")

#Crop and threshold 2006
sceneroot = "/Users/isa/Experiments/reg3d_eval/BH_2006/original";
file_in = sceneroot + "/gauss_233_normals.ply";
file_out = sceneroot + "/gauss_233_normals_cropped.ply"
if thresh:
    ply_util.thresh_bbox(file_in, file_out, min2006, max2006)

file_in = sceneroot + "/gauss_233_normals_cropped.ply";
basename_out = sceneroot + "/gauss_233_normals_pvn_cropped"
if thresh:
    ply_util.thresh_pvn(file_in, basename_out)
else:
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "SHOT", "gauss_233_normals_pvn_cropped", radius, njobs, percentile, True, "descriptors_cropped")
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "FPFH", "gauss_233_normals_pvn_cropped", radius, njobs, percentile, True, "descriptors_cropped")


# ******************** Downtown ********************
root2006 = "/Users/isa/Experiments/reg3d_eval/downtown_dan/original"
rootCVG = "/Users/isa/Experiments/reg3d_eval/downtown_CVG/original"
root2011 = "/Users/isa/Experiments/reg3d_eval/downtown_2011/original"


#Smallest coverage area is f2
#A good bounding box is given by
thresh = False


X_2006 = [-1500,1600]
Y_2006 = [-1500,1500]
Z_2006 = [-200,1200]

vi = 0
bbox_2006 = np.zeros((4,8))
for i in range(0,len(X_2006)):
    for j in range(0,len(Y_2006)):
        for k in range(0,len(Z_2006)):
            bbox_2006[:,vi] = np.array([X_2006[i],Y_2006[j],Z_2006[k],1])
            vi = vi+1

min_2006 = np.min(bbox_2006, axis=1)
max_2006 = np.max(bbox_2006, axis=1)

print "Downtown 2006"
print min_2006
print max_2006

#Load CVG-2006
cvg_2006_file = rootCVG + "/f5-2006_Hs.txt"
cvg_2006 = reg3d_T.gt_transformation(cvg_2006_file)

bbox_cvg = LA.inv(cvg_2006.Hs).dot(bbox_2006)

min_cvg = np.min(bbox_cvg, axis=1)
max_cvg = np.max(bbox_cvg, axis=1)

print "Downtown CVG"
print min_cvg
print max_cvg

#Load 2011-2006
down_2011_2006_file = root2011 + "/2011-2006_Hs.txt"
down_2011_2006 = reg3d_T.gt_transformation(down_2011_2006_file)

bbox_down_2011 = LA.inv(down_2011_2006.Hs).dot(bbox_2006)

min_2011 = np.min(bbox_down_2011, axis=1)
max_2011 = np.max(bbox_down_2011, axis=1)

print "Downtown down_2011"
print min_2011
print max_2011


#Crop and threshold 2006
sceneroot = root2006;
file_in = sceneroot + "/gauss_233_normals.ply";
file_out = sceneroot + "/gauss_233_normals_cropped.ply"
if thresh:
    ply_util.thresh_bbox(file_in, file_out, min_2006, max_2006)

file_in = sceneroot + "/gauss_233_normals_cropped.ply";
basename_out = sceneroot + "/gauss_233_normals_pvn_cropped"
if thresh:
    ply_util.thresh_pvn(file_in, basename_out)
else:
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "SHOT", "gauss_233_normals_pvn_cropped", radius, njobs, percentile, True, "descriptors_cropped")
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "FPFH", "gauss_233_normals_pvn_cropped", radius, njobs, percentile, True, "descriptors_cropped")

#Crop and threshold 2011
sceneroot = root2011;
file_in = sceneroot + "/gauss_233_normals.ply";
file_out = sceneroot + "/gauss_233_normals_cropped.ply"
if thresh:
    ply_util.thresh_bbox(file_in, file_out, min_2011, max_2011)

file_in = sceneroot + "/gauss_233_normals_cropped.ply";
basename_out = sceneroot + "/gauss_233_normals_pvn_cropped"
if thresh:
    ply_util.thresh_pvn(file_in, basename_out)
else:
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "SHOT", "gauss_233_normals_pvn_cropped", radius, njobs, percentile, True, "descriptors_cropped")
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "FPFH", "gauss_233_normals_pvn_cropped", radius, njobs, percentile, True, "descriptors_cropped")

#Crop and threshold CVG
sceneroot = rootCVG;
file_in = sceneroot + "/gauss_233_normals.ply";
file_out = sceneroot + "/gauss_233_normals_cropped.ply"
if thresh:
    ply_util.thresh_bbox(file_in, file_out, min_cvg, max_cvg)

file_in = sceneroot + "/gauss_233_normals_cropped.ply";
basename_out = sceneroot + "/gauss_233_normals_pvn_cropped"
if thresh:
    ply_util.thresh_pvn(file_in, basename_out)
else:
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "SHOT", "gauss_233_normals_pvn_cropped", radius, njobs, percentile, True, "descriptors_cropped")
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "FPFH", "gauss_233_normals_pvn_cropped", radius, njobs, percentile, True, "descriptors_cropped")


# ******************** Capitol ********************
root2006 = "/Users/isa/Experiments/reg3d_eval/capitol_dan/original"
root2011 = "/Users/isa/Experiments/reg3d_eval/capitol_2011/original"


#Smallest coverage area is f2
#A good bounding box is given by
thresh = False


X_2006 = [-0.48,0.48]
Y_2006 = [-0.48,0.48]
Z_2006 = [-0.007,0.35]

vi = 0
bbox_2006 = np.zeros((4,8))
for i in range(0,len(X_2006)):
    for j in range(0,len(Y_2006)):
        for k in range(0,len(Z_2006)):
            bbox_2006[:,vi] = np.array([X_2006[i],Y_2006[j],Z_2006[k],1])
            vi = vi+1

min_2006 = np.min(bbox_2006, axis=1)
max_2006 = np.max(bbox_2006, axis=1)

print "Capitol 2006"
print min_2006
print max_2006


#Load 2011-2006
down_2011_2006_file = root2011 + "/2011-2006_Hs.txt"
down_2011_2006 = reg3d_T.gt_transformation(down_2011_2006_file)

bbox_2011 = LA.inv(down_2011_2006.Hs).dot(bbox_2006)

min_2011 = np.min(bbox_2011, axis=1)
max_2011 = np.max(bbox_2011, axis=1)

print "Capitol 2011"
print min_2011
print max_2011


#Crop and threshold 2006
sceneroot = root2006;
file_in = sceneroot + "/gauss_233_normals.ply";
file_out = sceneroot + "/gauss_233_normals_cropped.ply"
if thresh:
    ply_util.thresh_bbox(file_in, file_out, min_2006, max_2006)

file_in = sceneroot + "/gauss_233_normals_cropped.ply";
basename_out = sceneroot + "/gauss_233_normals_pvn_cropped"
if thresh:
    ply_util.thresh_pvn(file_in, basename_out)
else:
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "SHOT", "gauss_233_normals_pvn_cropped", radius, njobs, percentile, True, "descriptors_cropped")
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "FPFH", "gauss_233_normals_pvn_cropped", radius, njobs, percentile, True, "descriptors_cropped")

#Crop and threshold 2011
sceneroot = root2011;
file_in = sceneroot + "/gauss_233_normals.ply";
file_out = sceneroot + "/gauss_233_normals_cropped.ply"
if thresh:
    ply_util.thresh_bbox(file_in, file_out, min_2011, max_2011)

file_in = sceneroot + "/gauss_233_normals_cropped.ply";
basename_out = sceneroot + "/gauss_233_normals_pvn_cropped"
if thresh:
    ply_util.thresh_pvn(file_in, basename_out)
else:
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "SHOT", "gauss_233_normals_pvn_cropped", radius, njobs, percentile, True, "descriptors_cropped")
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "FPFH", "gauss_233_normals_pvn_cropped", radius, njobs, percentile, True, "descriptors_cropped")