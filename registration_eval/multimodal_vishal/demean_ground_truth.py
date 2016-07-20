#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Maria Isabel Restrepo
# @Date:   2014-01-15 17:25:18
# File to demean the aerial2LiDAR ground truth after the LiDAR clouds
# were demeaned

import os, sys
import numpy as np
sys.path.append(os.pardir)
import reg3d_transformations as reg3d_T

reg_dir = "/Users/isa/Dropbox/MultiModalRegPaper"

sites = ["BH_2006", "BH_VSI", "capitol_2006", "capitol_2011", "downtown_2006", "downtown_2011"];
l_sites = ["BH", "BH", "capitol", "capitol", "downtown", "downtown"]

for site_idx in range(1, len(sites)):

    print "Processing Site: " + sites[site_idx]

    lidar_dir = reg_dir + "/data/LiDAR_demeaned" + "/" + l_sites[site_idx]

    lidar_cloud = lidar_dir + "/" + l_sites[site_idx]  + "_lidar.ply"
    centroid_file = lidar_dir + "/" + l_sites[site_idx]  + "_centroid.txt"

    geo_Tfile  = reg_dir + "/ground_truth/aerial-lidar/" + sites[site_idx] + "/Hs_geo.txt"

    dir_out =  reg_dir + "/ground_truth/aerial-lidar-demeaned/" + sites[site_idx]

    if not os.path.exists(dir_out):
      print "Output dir not found - creating one ", dir_out
      os.makedirs(dir_out)



    #read the centroid
    fid = open(centroid_file, 'r')
    centroid = np.genfromtxt(fid);
    fid.close()
    print "Centroid: "
    print centroid


    #read the GEO transfomation
    tform_file_out = dir_out + "/Hs_geo"
    GEO_Tform = reg3d_T.gt_transformation(geo_Tfile);

    print "Initial Translation: "
    print GEO_Tform.Ts
    print "Initial scale: "
    print GEO_Tform.scale

    GEO_Tform.Ts = GEO_Tform.Ts - centroid/GEO_Tform.scale
    print "Demeaned Translation: "
    print GEO_Tform.Ts


    GEO_Tform.Hs[:3, 3] = GEO_Tform.Hs[:3, 3] - centroid

    print "Demeaned Transfomation: "
    print GEO_Tform.Hs

    GEO_Tform.save_to_file(tform_file_out)







