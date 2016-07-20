#!/usr/bin/env python

# -*- coding: utf-8 -*-
# @Author: Maria Isabel Restrepo
# @Date:   2014-01-08 14:34:42
# @Last Modified by:   Maria Isabel Restrepo
# @Last Modified time: 2014-01-15 10:20:14
#
# A file to generate rigid transformations

import rotations
import transformations as tf
import numpy as np

for trial in range(0,5):
    H_file = "/Users/isa/Dropbox/MultiModalRegPaper/ground_truth/rand_t/H_" + str(trial) + ".txt"
    max_angle = (np.pi/18.0) #max angular error 10 degrees
    max_t = 5 #max translation 5 meters
    # H = np.identity(4)
    R_rand = np.identity(3)
    scale = 1.0;

    #generate a random rotation angle smaller than max_angle
    rand_angle = rotations.random_rot_angle(max_angle)
    print "Random Angle: "
    print rand_angle

    #generate a random rotation matrix of fixed angle
    rotations.R_random_axis(R_rand, rand_angle)
    Q_rand = tf.quaternion_from_matrix(R_rand);
    Q_vxl = np.array([float(Q_rand[1]),
                     float(Q_rand[2]),
                     float(Q_rand[3]),
                     float(Q_rand[0])])

    # H[:3, :3]= R_rand
    print "Rotation Matrix: "
    print R_rand
    print Q_vxl


    #generate random translation
    T = (np.random.random(3) - 0.5)* 2.0 * max_t
    print "Translation : "
    print T


    #save
    Tfos = open(H_file, 'w')
    Tfos.write("1.0\n")
    # import pdb; pdb.set_trace();
    np.savetxt( Tfos , Q_vxl.reshape(1, Q_vxl.shape[0]), fmt='%.5f')
    np.savetxt( Tfos , T.reshape(1, T.shape[0]), fmt='%.5f')
    Tfos.close()


