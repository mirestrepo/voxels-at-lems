#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Maria Isabel Restrepo
# @Date:   2014-02-28 11:04:16
# @Last Modified by:   Maria Isabel Restrepo
# @Last Modified time: 2014-02-28 11:19:29

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
random_dir = reg_dir + "/ground_truth/rand_t"
result_summary_file = random_dir + "/summary.txt"

ntrials = 5
error = np.zeros((ntrials, 3));

for trial in range(0,5):
    print 'Trial: ' + str(trial)

    t_fname = random_dir + "/H_" + str(trial) + ".txt"
    gt_fname = random_dir + "/H_identity_matrix.txt"


    error[trial,:] = reg3d.transformation_error_general(fname = t_fname,
                                                        gt_fname = gt_fname)


Tfos = open(result_summary_file, 'w')


print "-----------------------------------------------------"
print "*********** Errors *************"
print "-----------------------------------------------------"

print error[:,:]

print 'Mean:'
mean_error = np.mean(abs(error[:,:]), axis=0)
print mean_error
print 'Std:'
std_error = np.std(abs(error[:,:]), axis=0)
print std_error

Tfos.write("-----------------------------------------------------\n")
Tfos.write("*********** Errors  *************\n")
Tfos.write("-----------------------------------------------------\n")
np.savetxt( Tfos , error[:,:], fmt='%.7g')
Tfos.write("Mean:\n")
np.savetxt( Tfos , mean_error.reshape((1,3))  , fmt='%.7g', delimiter=' ')
Tfos.write("Std:\n")
np.savetxt( Tfos , std_error.reshape((1,3))  , fmt='%.7g', delimiter=' ')


Tfos.close()


