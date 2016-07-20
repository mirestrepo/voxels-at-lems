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
from os import path



class gt_transformation(object):


    def __init__(self, T):

        if ( type(T) == str):
            print "Loading Transformation from file: " + T

            Tfile = T
            #Load transformation
            Tfis = open(Tfile, 'r')
            lines = []
            lines = Tfis.readlines()
            format = len(lines)
            Tfis.seek(0) #reset file pointer

            if not (format==3 or format==4 or format==5) :
                raise ValueError("Wrong number of lines in file")
            # import code; code.interact(local=locals())


            if format == 3:
                """Handles processing a ground truth transfomation
                File saved using vxl format
                x' = s *(Rx + T)
                scale
                quaternion
                translation """
                print("Reading format 3")
                self.scale = float(lines[0])
                self.Ss = tf.scale_matrix(self.scale)
                quat_line = lines[1].split(" ")
                self.quat = tf.unit_vector(np.array([float(quat_line[3]),
                                                float(quat_line[0]),
                                                float(quat_line[1]),
                                                float(quat_line[2])]))
                self.Hs = tf.quaternion_matrix(self.quat)
                trans_line = lines[2].split(" ")
                self.Ts = np.array([float(trans_line[0]),
                               float(trans_line[1]),
                               float(trans_line[2])])
                Tfis.close()
                self.Rs = self.Hs.copy()[:3, :3]
                self.Hs[:3, 3] = self.Ts[:3]

                self.Hs = self.Ss.dot(self.Hs)  # to add again

            if format == 4 :
                """If the transformation was saved as:
                H (4x4) - = [S*R|S*T]
                """
                print("Reading format 4")

                self.Hs = np.genfromtxt(Tfile, usecols={0, 1, 2, 3})
                Tfis.close()
                scale, shear, angles, trans, persp = tf.decompose_matrix(self.Hs)
                self.scale = scale[0]  # assuming isotropic scaling

                self.Rs = self.Hs[:3, :3] * (1.0 / self.scale)
                self.Ts = self.Hs[:3, 3] * (1.0 / self.scale)
                self.quat = tf.quaternion_from_euler(angles[0], angles[1], angles[2])

            if format==5:
                """If the transformation was saved as:
                scale
                H (4x4) - = [S*R|S*T]
                """
                print("Reading format 5")
                self.Hs = np.genfromtxt(Tfis, skip_header=1, usecols={0, 1, 2, 3})
                Tfis.close()
                Tfis = open(Tfile, 'r')
                self.scale = np.genfromtxt(Tfis, skip_footer=4, usecols={0})
                Tfis.close()
                self.Rs = self.Hs[:3, :3] * (1.0 / self.scale)
                self.Ts = self.Hs[:3, 3] * (1.0 / self.scale)


                scale, shear, angles, trans, persp = tf.decompose_matrix(self.Hs)
                self.quat = tf.quaternion_from_euler(angles[0], angles[1], angles[2])

                print "Debugging translation:"
                print self.Ts
                print trans/self.scale




        elif (type(T) == np.ndarray):
            print "Loading Transformation array"
            self.Hs = T
            scale, shear, angles, trans, persp = tf.decompose_matrix(T)

            self.scale =scale[0]
            self.Rs = self.Hs[:3, :3] * (1.0 / self.scale)
            self.Ts = self.Hs[:3, 3] * (1.0 / self.scale)
            self.quat = tf.quaternion_from_euler(angles[0], angles[1], angles[2])

            print "Debugging translation:"
            print self.Ts
            print trans/self.scale

            # self.Rs = tf.quaternion_matrix(self.quat)
            # self.Ts = trans / self.scale


        print self.Hs


    def transform_points(self, points):
        return self.Hs.dot(points)

    def save_to_file(self, basename):
        T_file = basename + ".txt"
        T_file_mat = basename + "_matrix.txt"

        if  (path.exists(T_file)):
            print "Warning: Transformation file exists, it won't be overwritten"
        if  (path.exists(T_file_mat)):
            print "Warning: Matrix file exists, it won't be overwritten"

        if not (path.exists(T_file)):
            Tfos = open(T_file, 'w')
            np.savetxt( Tfos, np.array([self.scale]), fmt='%.7g')
            vxl_quat = np.array((self.quat[1],self.quat[2],self.quat[3],self.quat[0]))
            np.savetxt( Tfos , vxl_quat.reshape((1,4)) , fmt='%.7g', delimiter=' ')
            np.savetxt( Tfos , self.Ts.reshape((1,3))  , fmt='%.7g', delimiter=' ')
            Tfos.close()
        if not (path.exists(T_file_mat)):
            Tfos = open(T_file_mat, 'w')
            np.savetxt( Tfos, np.array([self.scale]), fmt='%.7g')
            np.savetxt( Tfos , self.Hs, fmt='%.7g')
            Tfos.close()


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

    def __init__(self, ia_Tfile, icp_Tfile, force_icp_unit_scale=True):

        #Load IA transformation
        Tfis = open(ia_Tfile, 'r')
        lines = Tfis.readlines()
        format = len(lines)
        Tfis.seek(0) #reset file pointer


        if format==5:
            """If the transformation was saved as
            -----IA-------------
            scale
            H (4x4) - = [S*R|S*T]
            """
            self.Hs_ia = np.genfromtxt(Tfis, skip_header=1, usecols={0, 1, 2, 3})
            Tfis.close()
            Tfis = open(ia_Tfile, 'r')
            self.scale_ia = np.genfromtxt(Tfis, skip_footer=4, usecols={0})
            Tfis.close()
            self.Rs_ia = self.Hs_ia[:3, :3] * (1.0 / self.scale_ia)
            self.Ts_ia = self.Hs_ia[:3, 3] * (1.0 / self.scale_ia)

        if format==4:
            """If the transformation was saved as
            -----IA-------------
            H (4x4) - = [S*R|S*T]
            """
            self.Hs_ia = np.genfromtxt(Tfis, usecols={0, 1, 2, 3})
            Tfis.close()
            scale, shear, angles, trans, persp = tf.decompose_matrix(self.Hs_ia)
            self.scale_ia = scale[0]  # assuming isotropic scaling

            self.Rs_ia = self.Hs_ia[:3, :3] * (1.0 / self.scale_ia)
            self.Ts_ia = self.Hs_ia[:3, 3] * (1.0 / self.scale_ia)

        #Load ICP transformation
        Tfis = open(icp_Tfile, 'r')
        self.Hs_icp = np.genfromtxt(Tfis, usecols={0, 1, 2, 3})
        Tfis.close()

        if np.isnan(np.sum(self.Hs_icp)):
            self.Hs_icp = np.identity(4)

        if force_icp_unit_scale:
            print "ICP assuming unit scale"
            self.scale_icp = 1.0;
        else:
            scale, shear, angles, trans, persp = tf.decompose_matrix(self.Hs_icp)
            self.scale_icp = scale[0]  # assuming isotropic scaling

        self.Hs_icp = self.Hs_icp.dot(self.Hs_ia)
        self.Rs_icp = self.Hs_icp[:3, :3] * (1.0 / (self.scale_ia * self.scale_icp))
        self.Ts_icp = self.Hs_icp[:3, 3] * (1.0 / (self.scale_ia * self.scale_icp))

        # scale, shear, angles, trans, persp = tf.decompose_matrix(self.Hs_ia)
        # self.Rs_ia = tf.euler_matrix(*angles)

        # scale, shear, angles, trans, persp = tf.decompose_matrix(self.Hs_icp.dot(self.Hs_ia))
        # self.Rs_icp = tf.euler_matrix(*angles)

        # import pdb; pdb.set_trace()


        print "Loaded IA Transformation: "
        print self.Hs_ia

        print "Loaded ICP Transformation: "
        print self.Hs_icp

        print "Loaded IA-ICP Scales: "
        print self.scale_ia, self.scale_icp

    def transform_points_ia(self, points):
        return self.Hs_ia.dot(points)

    def transform_points_icp(self, points):
        return self.Hs_icp.dot(points)
