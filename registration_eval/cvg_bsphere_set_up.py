#!/usr/bin/env python
# encoding: utf-8
"""
Created by Maria Isabel Restrepo on 2012-12-6.
Copyright (c) 2012 . All rights reserved.

A script to set up a small "common bounding box for all CVG sites"
"""




import reg3d_transformations as reg3d_T
import numpy as np
from numpy import linalg as LA
import transformations as tf

import sys
PLY_UTIL = "/Projects/voxels-at-lems-git/ply_util"
VOXELS_AT_LEMS_VPCL = "/Projects/voxels-at-lems-git/vpcl"

sys.path.append(PLY_UTIL)
sys.path.append(VOXELS_AT_LEMS_VPCL)

import thresh_ply as ply_util
import vpcl_compute_omp_descriptors as vpcl_descriptors

cvg_root = "/Users/isa/Experiments/reg3d_eval/cvg_eo_data"
njobs=8
radius=30
percentile=99
# #******************** Site 1 ********************

# #Flight with smallest coverage area is f2
# #A good bounding box is given by
# thresh = True

# XF2 = [-2,2]
# YF2 = [-2,1.5]
# ZF2 = [-1,1]

# vi = 0
# bboxF2 = np.zeros((4,8))
# for i in range(0,len(XF2)):
#     for j in range(0,len(YF2)):
#         for k in range(0,len(ZF2)):
#             bboxF2[:,vi] = np.array([XF2[i],YF2[j],ZF2[k],1])
#             vi = vi+1

# maxF2 = np.max(bboxF2, axis=1)
# meanF2 = np.mean(bboxF2, axis=1)

# # import pdb; pdb.set_trace()

# #Load f4-f2
# f4_f2_file = cvg_root + "/flight4_sites/site_1/f4-f2_Hs.txt"
# f4_f2 = reg3d_T.gt_transformation(f4_f2_file)

# meanF4 = LA.inv(f4_f2.Hs).dot(meanF2)
# maxF4 = LA.inv(f4_f2.Hs).dot(maxF2)

# #Load f5-f2
# f5_f2_file = cvg_root + "/flight5_sites/site_1/f5-f2_Hs.txt"
# f5_f2 = reg3d_T.gt_transformation(f5_f2_file)

# meanF5 = LA.inv(f5_f2.Hs).dot(meanF2)
# maxF5 = LA.inv(f5_f2.Hs).dot(maxF2)


# #Crop and threshold f2
# sceneroot = cvg_root + "/flight2_sites/site_1";
# file_in = sceneroot + "/gauss_233_normals.ply";
# file_out = sceneroot + "/gauss_233_normals_bsphere.ply"
# # if thresh:
# #    ply_util.thresh_bsphere(file_in, file_out, meanF2, maxF2)

# file_in = sceneroot + "/gauss_233_normals_bsphere.ply";
# basename_out = sceneroot + "/gauss_233_normals_bsphere_cropped"
# if thresh:
#    ply_util.thresh_pvn(file_in, basename_out)
# else:
#     vpcl_descriptors.compute_omp_descriptors(sceneroot, "SHOT", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")
#     vpcl_descriptors.compute_omp_descriptors(sceneroot, "FPFH", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")

# #Crop and threshold f4
# sceneroot = cvg_root + "/flight4_sites/site_1";
# file_in = sceneroot + "/gauss_233_normals.ply";
# file_out = sceneroot + "/gauss_233_normals_bsphere.ply"
# if thresh:
#   ply_util.thresh_bsphere(file_in, file_out, meanF4, maxF4)

# file_in = sceneroot + "/gauss_233_normals_bsphere.ply";
# basename_out = sceneroot + "/gauss_233_normals_bsphere_cropped"
# if thresh:
#    ply_util.thresh_pvn(file_in, basename_out)
# else:
#     vpcl_descriptors.compute_omp_descriptors(sceneroot, "SHOT", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")
#     vpcl_descriptors.compute_omp_descriptors(sceneroot, "FPFH", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")

# #Crop and threshold f5
# sceneroot = cvg_root + "/flight5_sites/site_1";
# file_in = sceneroot + "/gauss_233_normals.ply";
# file_out = sceneroot + "/gauss_233_normals_bsphere.ply"
# if thresh:
#     ply_util.thresh_bsphere(file_in, file_out, meanF5, maxF5)

# file_in = sceneroot + "/gauss_233_normals_bsphere.ply";
# basename_out = sceneroot + "/gauss_233_normals_bsphere_cropped"
# if thresh:
#    ply_util.thresh_pvn(file_in, basename_out)
# else:
#     vpcl_descriptors.compute_omp_descriptors(sceneroot, "SHOT", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")
#     vpcl_descriptors.compute_omp_descriptors(sceneroot, "FPFH", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")

# #******************** Site 2 ********************

#Flight with smallest coverage area is f2
#A good bounding box is given by
thresh = True


XF2 = [-4,1.0]
YF2 = [-2,3]
ZF2 = [-0.5,3]

vi = 0
bboxF2 = np.zeros((4,8))
for i in range(0,len(XF2)):
    for j in range(0,len(YF2)):
        for k in range(0,len(ZF2)):
            bboxF2[:,vi] = np.array([XF2[i],YF2[j],ZF2[k],1])
            vi = vi+1

maxF2 = np.max(bboxF2, axis=1)
meanF2 = np.mean(bboxF2, axis=1)

# import pdb; pdb.set_trace()

#Load f4-f2
f4_f2_file = cvg_root + "/flight4_sites/site_2/f4-f2_Hs.txt"
f4_f2 = reg3d_T.gt_transformation(f4_f2_file)

meanF4 = LA.inv(f4_f2.Hs).dot(meanF2)
maxF4 = LA.inv(f4_f2.Hs).dot(maxF2)

#Load f5-f2
f5_f2_file = cvg_root + "/flight5_sites/site_2/f5-f2_Hs.txt"
f5_f2 = reg3d_T.gt_transformation(f5_f2_file)

meanF5 = LA.inv(f5_f2.Hs).dot(meanF2)
maxF5 = LA.inv(f5_f2.Hs).dot(maxF2)


#Crop and threshold f2
sceneroot = cvg_root + "/flight2_sites/site_2";
file_in = sceneroot + "/gauss_233_normals.ply";
file_out = sceneroot + "/gauss_233_normals_bsphere.ply"
if thresh:
   ply_util.thresh_bsphere(file_in, file_out, meanF2, maxF2)

file_in = sceneroot + "/gauss_233_normals_bsphere.ply";
basename_out = sceneroot + "/gauss_233_normals_bsphere_cropped"
if thresh:
   ply_util.thresh_pvn(file_in, basename_out)
else:
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "SHOT", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "FPFH", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")

#Crop and threshold f4
sceneroot = cvg_root + "/flight4_sites/site_2";
file_in = sceneroot + "/gauss_233_normals.ply";
file_out = sceneroot + "/gauss_233_normals_bsphere.ply"
if thresh:
  ply_util.thresh_bsphere(file_in, file_out, meanF4, maxF4)

file_in = sceneroot + "/gauss_233_normals_bsphere.ply";
basename_out = sceneroot + "/gauss_233_normals_bsphere_cropped"
if thresh:
   ply_util.thresh_pvn(file_in, basename_out)
else:
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "SHOT", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "FPFH", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")

#Crop and threshold f5
sceneroot = cvg_root + "/flight5_sites/site_2";
file_in = sceneroot + "/gauss_233_normals.ply";
file_out = sceneroot + "/gauss_233_normals_bsphere.ply"
if thresh:
    ply_util.thresh_bsphere(file_in, file_out, meanF5, maxF5)

file_in = sceneroot + "/gauss_233_normals_bsphere.ply";
basename_out = sceneroot + "/gauss_233_normals_bsphere_cropped"
if thresh:
   ply_util.thresh_pvn(file_in, basename_out)
else:
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "SHOT", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "FPFH", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")

#******************** Site 3 ********************

#Flight with smallest coverage area is f2
#A good bounding box is given by

thresh = True


XF2 = [-6,6]
YF2 = [-5,5]
ZF2 = [-4,4]

vi = 0
bboxF2 = np.zeros((4,8))
for i in range(0,len(XF2)):
    for j in range(0,len(YF2)):
        for k in range(0,len(ZF2)):
            bboxF2[:,vi] = np.array([XF2[i],YF2[j],ZF2[k],1])
            vi = vi+1

maxF2 = np.max(bboxF2, axis=1)
meanF2 = np.mean(bboxF2, axis=1)

# import pdb; pdb.set_trace()

#Load f4-f2
f4_f2_file = cvg_root + "/flight4_sites/site_3/f4-f2_Hs.txt"
f4_f2 = reg3d_T.gt_transformation(f4_f2_file)

meanF4 = LA.inv(f4_f2.Hs).dot(meanF2)
maxF4 = LA.inv(f4_f2.Hs).dot(maxF2)

#Load f5-f2
f5_f2_file = cvg_root + "/flight5_sites/site_3/f5-f2_Hs.txt"
f5_f2 = reg3d_T.gt_transformation(f5_f2_file)

meanF5 = LA.inv(f5_f2.Hs).dot(meanF2)
maxF5 = LA.inv(f5_f2.Hs).dot(maxF2)


#Crop and threshold f2
sceneroot = cvg_root + "/flight2_sites/site_3";
file_in = sceneroot + "/gauss_233_normals.ply";
file_out = sceneroot + "/gauss_233_normals_bsphere.ply"
if thresh:
   ply_util.thresh_bsphere(file_in, file_out, meanF2, maxF2)

file_in = sceneroot + "/gauss_233_normals_bsphere.ply";
basename_out = sceneroot + "/gauss_233_normals_bsphere_cropped"
if thresh:
   ply_util.thresh_pvn(file_in, basename_out)
else:
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "SHOT", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "FPFH", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")

#Crop and threshold f4
sceneroot = cvg_root + "/flight4_sites/site_3";
file_in = sceneroot + "/gauss_233_normals.ply";
file_out = sceneroot + "/gauss_233_normals_bsphere.ply"
if thresh:
  ply_util.thresh_bsphere(file_in, file_out, meanF4, maxF4)

file_in = sceneroot + "/gauss_233_normals_bsphere.ply";
basename_out = sceneroot + "/gauss_233_normals_bsphere_cropped"
if thresh:
   ply_util.thresh_pvn(file_in, basename_out)
else:
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "SHOT", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "FPFH", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")

#Crop and threshold f5
sceneroot = cvg_root + "/flight5_sites/site_3";
file_in = sceneroot + "/gauss_233_normals.ply";
file_out = sceneroot + "/gauss_233_normals_bsphere.ply"
if thresh:
    ply_util.thresh_bsphere(file_in, file_out, meanF5, maxF5)

file_in = sceneroot + "/gauss_233_normals_bsphere.ply";
basename_out = sceneroot + "/gauss_233_normals_bsphere_cropped"
if thresh:
   ply_util.thresh_pvn(file_in, basename_out)
else:
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "SHOT", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "FPFH", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")

#******************** Site 4 ********************

#Flight with smallest coverage area is f2
#A good bounding box is given by

thresh = True

XF2 = [-3,6]
YF2 = [-3,5]
ZF2 = [-1,4]

vi = 0
bboxF2 = np.zeros((4,8))
for i in range(0,len(XF2)):
    for j in range(0,len(YF2)):
        for k in range(0,len(ZF2)):
            bboxF2[:,vi] = np.array([XF2[i],YF2[j],ZF2[k],1])
            vi = vi+1

maxF2 = np.max(bboxF2, axis=1)
meanF2 = np.mean(bboxF2, axis=1)

# import pdb; pdb.set_trace()

#Load f4-f2
f4_f2_file = cvg_root + "/flight4_sites/site_4/f4-f2_Hs.txt"
f4_f2 = reg3d_T.gt_transformation(f4_f2_file)

meanF4 = LA.inv(f4_f2.Hs).dot(meanF2)
maxF4 = LA.inv(f4_f2.Hs).dot(maxF2)

#Load f5-f2
f5_f2_file = cvg_root + "/flight5_sites/site_4/f5-f2_Hs.txt"
f5_f2 = reg3d_T.gt_transformation(f5_f2_file)

meanF5 = LA.inv(f5_f2.Hs).dot(meanF2)
maxF5 = LA.inv(f5_f2.Hs).dot(maxF2)


#Crop and threshold f2
sceneroot = cvg_root + "/flight2_sites/site_4";
file_in = sceneroot + "/gauss_233_normals.ply";
file_out = sceneroot + "/gauss_233_normals_bsphere.ply"
if thresh:
   ply_util.thresh_bsphere(file_in, file_out, meanF2, maxF2)

file_in = sceneroot + "/gauss_233_normals_bsphere.ply";
basename_out = sceneroot + "/gauss_233_normals_bsphere_cropped"
if thresh:
   ply_util.thresh_pvn(file_in, basename_out)
else:
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "SHOT", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "FPFH", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")

#Crop and threshold f4
sceneroot = cvg_root + "/flight4_sites/site_4";
file_in = sceneroot + "/gauss_233_normals.ply";
file_out = sceneroot + "/gauss_233_normals_bsphere.ply"
if thresh:
  ply_util.thresh_bsphere(file_in, file_out, meanF4, maxF4)

file_in = sceneroot + "/gauss_233_normals_bsphere.ply";
basename_out = sceneroot + "/gauss_233_normals_bsphere_cropped"
if thresh:
   ply_util.thresh_pvn(file_in, basename_out)
else:
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "SHOT", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "FPFH", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")

#Crop and threshold f5
sceneroot = cvg_root + "/flight5_sites/site_4";
file_in = sceneroot + "/gauss_233_normals.ply";
file_out = sceneroot + "/gauss_233_normals_bsphere.ply"
if thresh:
    ply_util.thresh_bsphere(file_in, file_out, meanF5, maxF5)

file_in = sceneroot + "/gauss_233_normals_bsphere.ply";
basename_out = sceneroot + "/gauss_233_normals_bsphere_cropped"
if thresh:
   ply_util.thresh_pvn(file_in, basename_out)
else:
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "SHOT", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "FPFH", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")

#******************** Site 7 ********************

#Flight with smallest coverage area is f2
#A good bounding box is given by
thresh = True


XF2 = [-1.1,1]
YF2 = [-1.2,1]
ZF2 = [-0.5,0.8]

vi = 0
bboxF2 = np.zeros((4,8))
for i in range(0,len(XF2)):
    for j in range(0,len(YF2)):
        for k in range(0,len(ZF2)):
            bboxF2[:,vi] = np.array([XF2[i],YF2[j],ZF2[k],1])
            vi = vi+1

maxF2 = np.max(bboxF2, axis=1)
meanF2 = np.mean(bboxF2, axis=1)

# import pdb; pdb.set_trace()

#Load f4-f2
f4_f2_file = cvg_root + "/flight4_sites/site_7/f4-f2_Hs.txt"
f4_f2 = reg3d_T.gt_transformation(f4_f2_file)

meanF4 = LA.inv(f4_f2.Hs).dot(meanF2)
maxF4 = LA.inv(f4_f2.Hs).dot(maxF2)

#Load f5-f2
f5_f2_file = cvg_root + "/flight5_sites/site_7/f5-f2_Hs.txt"
f5_f2 = reg3d_T.gt_transformation(f5_f2_file)

meanF5 = LA.inv(f5_f2.Hs).dot(meanF2)
maxF5 = LA.inv(f5_f2.Hs).dot(maxF2)


#Crop and threshold f2
sceneroot = cvg_root + "/flight2_sites/site_7";
file_in = sceneroot + "/gauss_233_normals.ply";
file_out = sceneroot + "/gauss_233_normals_bsphere.ply"
if thresh:
   ply_util.thresh_bsphere(file_in, file_out, meanF2, maxF2)

file_in = sceneroot + "/gauss_233_normals_bsphere.ply";
basename_out = sceneroot + "/gauss_233_normals_bsphere_cropped"
if thresh:
   ply_util.thresh_pvn(file_in, basename_out)
else:
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "SHOT", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "FPFH", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")

#Crop and threshold f4
sceneroot = cvg_root + "/flight4_sites/site_7";
file_in = sceneroot + "/gauss_233_normals.ply";
file_out = sceneroot + "/gauss_233_normals_bsphere.ply"
if thresh:
  ply_util.thresh_bsphere(file_in, file_out, meanF4, maxF4)

file_in = sceneroot + "/gauss_233_normals_bsphere.ply";
basename_out = sceneroot + "/gauss_233_normals_bsphere_cropped"
if thresh:
   ply_util.thresh_pvn(file_in, basename_out)
else:
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "SHOT", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "FPFH", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")

#Crop and threshold f5
sceneroot = cvg_root + "/flight5_sites/site_7";
file_in = sceneroot + "/gauss_233_normals.ply";
file_out = sceneroot + "/gauss_233_normals_bsphere.ply"
if thresh:
    ply_util.thresh_bsphere(file_in, file_out, meanF5, maxF5)

file_in = sceneroot + "/gauss_233_normals_bsphere.ply";
basename_out = sceneroot + "/gauss_233_normals_bsphere_cropped"
if thresh:
   ply_util.thresh_pvn(file_in, basename_out)
else:
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "SHOT", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")
    vpcl_descriptors.compute_omp_descriptors(sceneroot, "FPFH", "gauss_233_normals_bsphere_cropped", radius, njobs, percentile, True, "descriptors_cropped")
