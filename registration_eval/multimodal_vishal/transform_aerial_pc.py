#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Maria Isabel Restrepo
# @Date:   2014-01-08 17:41:46
# @Last Modified by:   Maria Isabel Restrepo
# @Last Modified time: 2014-01-19 13:06:44
# A file to transform the aerial point clouds such that they are
# a "small" random transformation away from the LiDAR point cloud

import numpy as np
import sys, os
sys.path.append(os.pardir)
import reg3d_transformations as reg3d_T

reg_dir = "/Users/isa/Dropbox/MultiModalRegPaper"

sites = ["BH_2006", "BH_VSI", "capitol_2006", "capitol_2011", "downtown_2006", "downtown_2011"];
percent = 95;

for site in sites:

    for trial in range(0,5):

        print "Processing Site: " + site + " Trial: " + str(trial)

        pc_aerial_file = reg_dir + "/data/point_clouds_aerial/" + site + "/gauss_233_normals_pvn_cropped_"+ str(percent)+ ".ply"
        geo_Tfile  = reg_dir + "/ground_truth/aerial-lidar-demeaned/" + site + "/Hs_geo.txt"
        noise_Tfile = reg_dir + "/ground_truth/rand_t/H_" + str(trial) +".txt"
        dir_out = file_out = reg_dir + "/data/point_clouds_aerial_geo_noise/" + site + "/H_" + str(trial)

        if not os.path.exists(dir_out):
          print "Output dir not found - creating one ", dir_out
          os.makedirs(dir_out)

        file_out = dir_out + "/gauss_233_normals_pvn_cropped_"+ str(percent)+ ".ply"
        tform_file_out = dir_out +"/Hs"

        GEO_Tform = reg3d_T.gt_transformation(geo_Tfile);
        noise_Tform = reg3d_T.gt_transformation(noise_Tfile);

        final_Hs = noise_Tform.Hs.dot(GEO_Tform.Hs)

        final_Tform = reg3d_T.gt_transformation(final_Hs)

        #save the transform
        final_Tform.save_to_file(tform_file_out);

        #Load original corrs .ply
        fid = open(pc_aerial_file, 'r')
        pc_aerial = np.genfromtxt(fid, dtype=float, delimiter=' ',
                                skip_header=16,
                                usecols={0, 1, 2});
        fid.close()

        npoints = len(pc_aerial)

        print "Read: " + str(npoints) + " points"

        pc_aerial = np.hstack((pc_aerial, np.ones([npoints, 1])))

        pc_aerial = final_Tform.transform_points((pc_aerial).T)

        # import pdb; pdb.set_trace()

        #save the transformed points to a .ply file
        header = ('ply\n' +
        'format ascii 1.0\n' +
        'element vertex ' + str(npoints) + '\n' +
        'property float x\nproperty float y\nproperty float z\n' +
        'end_header\n');

        fid = open( file_out , 'w' )
        fid.write( header )
        np.savetxt( fid , pc_aerial[:3,:].T , fmt='%.5f %.5f %.5f', delimiter=' ')
        fid.close()

        print "Done transforming cloud"


