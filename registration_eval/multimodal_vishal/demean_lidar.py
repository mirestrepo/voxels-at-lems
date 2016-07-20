#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Maria Isabel Restrepo
# @Date:   2014-01-15 16:59:11
# Demean the LiDAR files

import os
import numpy as np

l_sites = ["BH", "capitol", "downtown"]

for site in l_sites:

    cloud_in = "/Users/isa/Dropbox/MultiModalRegPaper/data/LiDAR/" + site + "/" + site  + "_lidar.ply"
    dir_out = "/Users/isa/Dropbox/MultiModalRegPaper/data/LiDAR_demeaned" + "/" + site

    if not os.path.exists(dir_out):
      print "Output dir not found - creating one ", dir_out
      os.makedirs(dir_out)

    cloud_out = dir_out + "/" + site  + "_lidar.ply"
    c_file_out = dir_out + "/" + site  + "_centroid.txt"

    #Load original corrs .ply
    fid = open(cloud_in, 'r')
    pc_lidar = np.genfromtxt(fid, dtype=float, delimiter=' ',
                             skip_header=10,
                             usecols={0, 1, 2});
    fid.close()

    npoints = len(pc_lidar)

    print "Read: " + str(npoints) + " points"

    centroid = np.mean(pc_lidar, axis=0)
    pc_lidar = pc_lidar - centroid

    print "Centroid: "
    print centroid

    #save the transformed points to a .ply file
    header = ('ply\n' +
    'format ascii 1.0\n' +
    'element vertex ' + str(npoints) + '\n' +
    'property float x\nproperty float y\nproperty float z\n' +
    'end_header\n');

    fid = open( cloud_out , 'w' )
    fid.write( header )
    np.savetxt( fid , pc_lidar , fmt='%.5f %.5f %.5f', delimiter=' ')
    fid.close()

    fid = open( c_file_out , 'w' )
    np.savetxt( fid , centroid[:3].reshape(1, centroid[:3].shape[0]), fmt='%.5f')
    fid.close()

