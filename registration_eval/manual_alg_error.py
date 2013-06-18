#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo
Script to find the average alignment error of manual registrationπ
"""
import os
import sys
import numpy as np
from scipy import stats
import reg3d

ntrials = 31
error = np.zeros((ntrials-1, 3));

for trial in range(1,ntrials):
    print 'Trial: ' + str(trial)
    fname = "/data/lidar_providence/manual_error/Hs" + str(trial) + ".txt"
    gt_fname = "/data/lidar_providence/manual_error/Hs-identity.txt"
    error[trial-1,:] = reg3d.transformation_error_general(fname = fname,
                                                        gt_fname = gt_fname)

print 'Errors:'
print error

print 'Mean:'
print np.mean(abs(error), axis=0)
print 'Std:'
print np.std(abs(error), axis=0)

