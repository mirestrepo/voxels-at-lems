#!/usr/bin/env python
# encoding: utf-8
"""
reg3d_transformations.py

Created by Maria Isabel Restrepo on 2012-10-03.
Copyright (c) 2012 . All rights reserved.
Trhough out these experiments the transfomations were saved by
vxl or PCL. This file contains utilities to read them and use them
to transform points
"""

import numpy as np
import transformations as tf


class gt_transformation(object):
    """Handels processing a groud truth tranfomation
   File saved using vxl format
   x' = s *(Rx + T)
   scale
   quaternion
   translation """

    def __init__(self, Tfile):

        #Load transformation
        Tfis = open(Tfile, 'r')
        lines = []
        lines = Tfis.readlines()
        self.scale = float(lines[0])
        self.Ss = tf.scale_matrix(self.scale)
        quat_line = lines[1].split(" ")
        quat = tf.unit_vector(np.array([float(quat_line[3]),
                                        float(quat_line[0]),
                                        float(quat_line[1]),
                                        float(quat_line[2])]))
        self.Hs = tf.quaternion_matrix(quat)
        trans_line = lines[2].split(" ")
        self.Ts = np.array([float(trans_line[0]),
                       float(trans_line[1]),
                       float(trans_line[2])])
        Tfis.close()
        self.Rs = self.Hs.copy()[:3, :3]
        self.Hs[:3, 3] = self.Ts[:3]
        # import pdb; pdb.set_trace()

        self.Hs[:3, 3] = np.zeros((3));
        self.Hs = self.Ss.dot(self.Hs)

        self.Rs = self.Rs
        self.Ts = self.Ts

        print "Loaded Ground Truth Transformation: "
        print self.Hs

    def transform_points(self, points):
        return self.Hs.dot(points)


class geo_transformation(object):
    """Handels processing a geo tranfomation
    File saved using vxl format
    x' = s *(Rx + T)
    scale
    quaternion
    translation """

    def __init__(self, geo_tform):

        #Load transformation
        Tfis = open(geo_tform, 'r')
        lines = []
        lines = Tfis.readlines()
        self.scale_geo = float(lines[0])
        self.Ss_geo = tf.scale_matrix(self.scale_geo)
        quat_line = lines[1].split(" ")
        quat_geo = np.array([float(quat_line[3]), float(quat_line[0]),
                             float(quat_line[1]), float(quat_line[2])])
        self.Rs_geo = tf.quaternion_matrix(quat_geo)
        trans_line = lines[2].split(" ")
        self.trans_geo = np.array([float(trans_line[0]), float(trans_line[1]),
                              float(trans_line[2])])
        Tfis.close()
        self.Hs_geo = self.Rs_geo.copy()
        self.Hs_geo[:3, 3] = self.trans_geo[:3]
        self.Hs_geo = self.Ss_geo.dot(self.Hs_geo)

        print "Loaded GeoTransformation: "
        print self.Hs_geo

    def transform_points(self, points):
        return self.Hs_geo.dot(points)





class pcl_transformation(object):
    """Handels processing a Initial Alignment and ICP tranfomation
    File saved using PCL format
    -----IA-------------
    scale
    H (4x4) - = [S*R|S*T]
    -----ICP -----------
    File saved using PCL format
    H (4x4) - = [R|T]
    """

    def __init__(self, ia_Tfile, icp_Tfile):

        #Load IA transformation
        Tfis = open(ia_Tfile, 'r')
        self.Hs_ia = np.genfromtxt(Tfis, skip_header=1, usecols={0, 1, 2, 3})
        Tfis.close()
        Tfis = open(ia_Tfile, 'r')
        self.Ss_ia = np.genfromtxt(Tfis, skip_footer=4, usecols={0})
        Tfis.close()
        self.Rs_ia = self.Hs_ia[:3, :3] * (1.0 / self.Ss_ia)
        self.Ts_ia = self.Hs_ia[:3, 3] * (1.0 / self.Ss_ia)

        #Load ICP transformation
        Tfis = open(icp_Tfile, 'r')
        self.Hs_icp = np.genfromtxt(Tfis, usecols={0, 1, 2, 3})
        Tfis.close()
        self.Hs_icp = self.Hs_icp.dot(self.Hs_ia)
        self.Rs_icp = self.Hs_icp[:3, :3] * (1.0 / self.Ss_ia)
        self.Ts_icp = self.Hs_icp[:3, 3] * (1.0 / self.Ss_ia)

        self.Hs_ia[:3, 3] = np.zeros((3))
        self.Hs_icp[:3, 3] = np.zeros((3))
        print "Loaded IA Transformation: "
        print self.Hs_ia

        print "Loaded ICP Transformation: "
        print self.Hs_icp

    def transform_points_ia(self, points):
        return self.Hs_ia.dot(points)

    def transform_points_icp(self, points):
        return self.Hs_icp.dot(points)
