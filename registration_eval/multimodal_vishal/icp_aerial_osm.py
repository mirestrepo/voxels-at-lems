#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Maria Isabel Restrepo
# @Date:   2014-02-28 12:18:57
# @Last Modified by:   Maria Isabel Restrepo
# @Last Modified time: 2014-02-28 14:50:40


import sys, os

VOXELS_AT_LEMS_VPCL = "../../vpcl"
sys.path.append(VOXELS_AT_LEMS_VPCL)

import vpcl_setup_module
vpcl_setup_module.setUpPaths(configuration = 'Release')
import vpcl_adaptor
from vpcl_register import py_vpcl

reg_dir = "/Users/isa/Dropbox/MultiModalRegPaper"

sites = [ "downtown_2006", "downtown_2011"];
l_sites = ["downtown", "downtown"]
percent = 95;

for site_idx in range(0, len(sites)):

    for trial in range(0,5):

        src_fname = reg_dir + "/data/Osm/downtown_roads_demeaned.ply"
        tgt_fname = reg_dir + "/data/point_clouds_aerial_geo_noise/" + sites[site_idx ] + "/H_" + str(trial) + "/gauss_233_normals_pvn_cropped_" + str(percent) + ".ply"

        dir_out = reg_dir + "/icp_results/osm-aerial/" + sites[site_idx ] + "/H_" + str(trial)


        if not os.path.exists(dir_out):
          print "Output dir not found - creating one ", dir_out
          os.makedirs(dir_out)

        output_cloud_fname = dir_out+ "/icp_output_cloud_" + str(percent) + ".ply"
        tform_fname = dir_out + "/icp_output_tform_" + str(percent) + ".txt"

        cloud_res = 1 #1 meter
        max_dist = 5 * cloud_res;
        translation_threshold = 0.001 * cloud_res #used to be 0.1
        rotation_threshold = 0.001; #degree
        nr_iterations = 500

        vpcl_adaptor.register_icp(   srcFname     = src_fname,
                                     tgtFname     = tgt_fname,
                                     outCloud     = output_cloud_fname,
                                     tformFname   = tform_fname,
                                     maxCorrDist  = max_dist,
                                     epsTrans     = translation_threshold,
                                     epsRot       = rotation_threshold,
                                     numIter      = nr_iterations,
                                     rejectNormals = False,
                                     computeScale = False);

