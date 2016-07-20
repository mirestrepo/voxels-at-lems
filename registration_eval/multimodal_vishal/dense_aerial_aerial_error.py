#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Maria Isabel Restrepo
# @Date:   2014-01-17 16:38:15
# Script to find the average ICP alignment error



import os
import sys
import numpy as np
from scipy import stats
sys.path.append(os.pardir)
VOXELS_AT_LEMS_VPCL = "../../vpcl"
sys.path.append(VOXELS_AT_LEMS_VPCL)

import vpcl_setup_module
vpcl_setup_module.setUpPaths(configuration = 'Release')

import reg3d

reg_dir = "/Users/isa/Dropbox/MultiModalRegPaper"
results_dir = reg_dir + "/DenseResults/Aerial2Aerial"
gt_dir = reg_dir + "/ground_truth"

result_summary_file = results_dir + "/error_summary.txt"

Tfos = open(result_summary_file, 'w')



bh_fname =  results_dir + "/BH_vsi_06_finer.txt"
gt_bh_fname = gt_dir + "/aerial-aerial/bh_vsi_06_Hs.txt"
geo_bh_fname = gt_dir + "/aerial-lidar-demeaned/BH_2006/Hs_geo.txt"
error = reg3d.transformation_error_general(fname = bh_fname,
                                           gt_fname = gt_bh_fname,
                                           geo_fname = geo_bh_fname )

Tfos.write("-----------------------------------------------------\n")
Tfos.write("*********** Error BH_VSI_2006 ***********************\n")
Tfos.write("-----------------------------------------------------\n")
np.savetxt( Tfos , error.reshape((1,3))  , fmt='%.7g', delimiter=' ')



capitol_fname =  results_dir + "/capitol_11_06_finer.txt"
gt_capitol_fname = gt_dir + "/aerial-aerial/capitol_11_06_Hs.txt"
geo_capitol_fname = gt_dir + "/aerial-lidar-demeaned/capitol_2006/Hs_geo.txt"
error = reg3d.transformation_error_general(fname = capitol_fname,
                                           gt_fname = gt_capitol_fname,
                                           geo_fname = geo_capitol_fname )

Tfos.write("-----------------------------------------------------\n")
Tfos.write("*********** Error Capitol_11_06 Finer ***************\n")
Tfos.write("-----------------------------------------------------\n")
np.savetxt( Tfos , error.reshape((1,3))  , fmt='%.7g', delimiter=' ')


capitol_fname =  results_dir + "/capitol_11_06_coarser.txt"
error = reg3d.transformation_error_general(fname = capitol_fname,
                                           gt_fname = gt_capitol_fname,
                                           geo_fname = geo_capitol_fname )

Tfos.write("-----------------------------------------------------\n")
Tfos.write("*********** Error Capitol_11_06 Coarser *************\n")
Tfos.write("-----------------------------------------------------\n")
np.savetxt( Tfos , error.reshape((1,3))  , fmt='%.7g', delimiter=' ')


downtown_fname =  results_dir + "/downtown_finer_11_06.txt"
gt_downtown_fname = gt_dir + "/aerial-aerial/downtown_11_06_Hs.txt"
geo_downtown_fname = gt_dir + "/aerial-lidar-demeaned/downtown_2006/Hs_geo.txt"
error = reg3d.transformation_error_general(fname = downtown_fname,
                                           gt_fname = gt_downtown_fname,
                                           geo_fname = geo_downtown_fname )
Tfos.write("-----------------------------------------------------\n")
Tfos.write("*********** Error Downtown_11_06 Finer ***************\n")
Tfos.write("-----------------------------------------------------\n")
np.savetxt( Tfos , error.reshape((1,3))  , fmt='%.7g', delimiter=' ')


downtown_fname =  results_dir + "/downtown_coarser_11_06.txt"
error = reg3d.transformation_error_general(fname = downtown_fname,
                                           gt_fname = gt_downtown_fname,
                                           geo_fname = geo_downtown_fname )
Tfos.write("-----------------------------------------------------\n")
Tfos.write("*********** Error Downtown_11_06 Coarser ************\n")
Tfos.write("-----------------------------------------------------\n")
np.savetxt( Tfos , error.reshape((1,3))  , fmt='%.7g', delimiter=' ')

Tfos.close()


