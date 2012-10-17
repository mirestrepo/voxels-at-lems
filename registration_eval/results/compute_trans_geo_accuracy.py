#!/usr/bin/env python
# encoding: utf-8
"""
compute_transformation_error.py

Created by Maria Isabel Restrepo on 2012-09-24.
Copyright (c) 2012 . All rights reserved.
This script computes the distances betweeen an estimated similarity transformation and its ground truth
The transformation is used to transform a "source" coordinate system into a "target coordinate system"
To compute the error between the translations, the L2 norm diference translation vectors in the
"source coordinate system" is computed. Since distances are preserved under R and T, only scale is applied.
The rotation error is computed as the half angle between the normalized queternions i.e acos(|<q1,q2>|) in [0, pi/2]
"""
import os
import sys
import logging
import argparse
import vpcl_adaptor as vpcl
import numpy as np
from numpy import linalg as LA
import transformations as tf
import math
import matplotlib.pyplot as plt

sys.path.append(os.pardir)
import reg3d_transformations as reg3d_T

LOG = None


"""Compute the accuracy between the LIDAR fiducial points
and corresponding geo-register correspondances"""
def compute_ref_accuracy(fid_path, original_corrs_path,
                         geo_tform):

    #Load fiducial .ply
    fid = open(fid_path, 'r')
    fid_points = np.genfromtxt(fid, dtype=float, delimiter=' ',
                                skip_header=9)
    fid.close()
    #Load original corrs .ply
    fid = open(original_corrs_path, 'r')
    original_corrs = np.genfromtxt(fid, dtype=float,
                                    delimiter=' ', skip_header=9)
    fid.close()

    #Load transformation
    #************GEO**************"
    Tfis = open(geo_tform, 'r')
    lines = []
    lines = Tfis.readlines()
    scale_geo = float(lines[0])
    Ss_geo = tf.scale_matrix(scale_geo)
    quat_line = lines[1].split(" ")
    quat_geo = np.array([float(quat_line[3]), float(quat_line[0]),
                         float(quat_line[1]), float(quat_line[2])])
    Rs_geo = tf.quaternion_matrix(quat_geo)
    trans_line = lines[2].split(" ")
    trans_geo = np.array([float(trans_line[0]), float(trans_line[1]),
                          float(trans_line[2])])
    Tfis.close()
    Hs_geo = Rs_geo.copy()
    Hs_geo[:3, 3] = trans_geo[:3]
    Hs_geo = Ss_geo.dot(Hs_geo)

    LOG.debug("\n******Geo***** \n Scale: \n%s \nR:\n%s \nT:\n%s \nH:\n%s",
        Ss_geo, Rs_geo, trans_geo, Hs_geo)

    #Compute the "reference error"
    #i.e. fiducial points - geo registered correspondances
    npoints, c = fid_points.shape
    if npoints != 30:
        LOG.warn("Number of fiducial point is NOT 30")
    if c != 3:
        LOG.error("Fiducial points has the wrong number of dimensions")
    # import code; code.interact(local=locals())

    fid_points_hom = np.hstack((fid_points, np.ones([npoints, 1]))).T
    original_corrs_hom = np.hstack((original_corrs, np.ones([npoints, 1]))).T
    geo_corrs_hom = Hs_geo.dot(original_corrs_hom)
    geo_ref_diff = geo_corrs_hom - fid_points_hom

    # import pdb; pdb.set_trace()

    delta_z = np.sqrt(geo_ref_diff[2, :] * geo_ref_diff[2, :])
    delta_r = np.sqrt(geo_ref_diff[0, :] * geo_ref_diff[0, :] +
                      geo_ref_diff[1, :] * geo_ref_diff[1, :])

    return delta_z, delta_r


def compute_geo_accuracy(fid_path, original_corrs_path,
                         geo_tform, trials_root, desc_name,
                         niter, ntrials, percentile=99):

    #Load fiducial .ply
    fid = open(fid_path, 'r')
    fid_points = np.genfromtxt(fid, delimiter=' ',
                                skip_header=9)
    fid.close()

    #Load original corrs .ply
    fid = open(original_corrs_path, 'r')
    original_corrs = np.genfromtxt(fid, delimiter=' ', skip_header=9)
    fid.close()

    #load the geo tranformation
    GEO = reg3d_T.geo_transformation(geo_tform);

    #Compute the "reference error"
    #i.e. fiducial points - geo registered correspondances
    npoints, c = fid_points.shape
    if npoints != 30:
        LOG.warn("Number of fiducial point is NOT 30")
    if c != 3:
        LOG.error("Fiducial points has the wrong number of dimensions")
    # import code; code.interact(local=locals())

    fid_points_hom = np.hstack((fid_points, np.ones([npoints, 1]))).T
    original_corrs_hom = np.hstack((original_corrs, np.ones([npoints, 1]))).T
    geo_corrs_hom = GEO.transform_points(original_corrs_hom)
    geo_ref_diff = geo_corrs_hom - fid_points_hom

    # import pdb; pdb.set_trace()

    delta_z = (geo_ref_diff[2, :] **2) ** (1./2.)
    delta_r = (geo_ref_diff[0, :] **2 + geo_ref_diff[1, :] **2 )** (1./2.)

    delta_z_ia = np.zeros([ntrials, npoints])
    delta_r_ia = np.zeros([ntrials, npoints])
    delta_z_icp = np.zeros([ntrials, npoints])
    delta_r_icp = np.zeros([ntrials, npoints])

    for trial in range(0, ntrials):

        print "********Trial", trial, "**********"

        #Load the transformations for this trial

        #************Hs**************#
        #read source to target "Ground Truth" Transformation
        Tfile = trials_root + "/trial_" + str(trial) + "/Hs_inv.txt"
        GT_Tform = reg3d_T.gt_transformation(Tfile)

        src_features_dir = (trials_root + "/trial_" + str(trial) +
                            "/" + desc_name)

        Tfile_ia = (src_features_dir + "/ia_transformation_" +
                    str(percentile) + "_" + str(niter) + ".txt")
        Tfile_icp = (src_features_dir + "/icp_transformation_" +
                     str(percentile) + "_" + str(niter) + ".txt")

        REG_Tform = reg3d_T.pcl_transformation(Tfile_ia, Tfile_icp)
        Hs_ia_error = REG_Tform.Hs_ia.dot(GT_Tform.Hs)
        Hs_icp_error = REG_Tform.Hs_icp.dot(GT_Tform.Hs)

        # transform the points with the residual transformations
        ia_corrs_hom = Hs_ia_error.dot(original_corrs_hom)
        icp_corrs_hom = Hs_icp_error.dot(original_corrs_hom)
        # geo-register
        geo_ia_corrs_hom = GEO.transform_points(ia_corrs_hom)
        geo_icp_corrs_hom = GEO.transform_points(icp_corrs_hom)
        # distances
        geo_ia_ref_diff = geo_ia_corrs_hom - fid_points_hom
        geo_icp_ref_diff = geo_icp_corrs_hom - fid_points_hom

        delta_z_ia[trial, :] = np.sqrt(geo_ia_ref_diff[2, :] ** 2)
        delta_r_ia[trial, :] = np.sqrt(geo_ia_ref_diff[0, :] ** 2 +
                                       geo_ia_ref_diff[1, :] ** 2 )


        delta_z_icp[trial, :] = np.sqrt(geo_icp_ref_diff[2, :] ** 2)
        delta_r_icp[trial, :] = np.sqrt(geo_icp_ref_diff[0, :] ** 2 +
                                        geo_icp_ref_diff[1, :] ** 2)

        # import pdb; pdb.set_trace()

    return delta_z, delta_r,\
           delta_z_ia, delta_r_ia, \
           delta_z_icp, delta_r_icp

def main(logfile=None):

    global LOG
    LOG = setlogging(logfile)

    descriptors = ["FPFH_30", "SHOT_30"]
    niter = 500;
    ntrials = 10;
    plot_errors = True;
    if (plot_errors):
      colors = ['magenta','green'];
      markers = ['o', 's', '*', '+', '^', 'v']
    fid_path = "/data/lidar_providence/downtown_offset-1-financial-dan-pts1.ply"
    original_corrs_path = "/data/lidar_providence/downtown_offset-1-financial-dan-pts0.ply"
    trials_root = "/Users/isa/Experiments/reg3d_eval/downtown_dan";
    geo_tform = "/data/lidar_providence/downtown_offset-1-financial-dan-Hs.txt"
    for d_idx in range(0, len(descriptors)):
        desc_name = descriptors[d_idx]

        delta_z, delta_r, \
        delta_z_ia, delta_r_ia, \
        delta_z_icp, delta_r_icp = compute_geo_accuracy(fid_path,
                                    original_corrs_path,
                                    geo_tform, trials_root, desc_name,
                                    niter, ntrials)

        #sort errors for all trials to get the 70 80 90 % errors
        delta_z_ia.sort(axis=0)
        delta_r_ia.sort(axis=0)

        delta_z_icp.sort(axis=0)
        delta_r_icp.sort(axis=0)

        CE_70_ia = delta_r_ia[int(0.7 * ntrials) - 1, :]
        CE_80_ia = delta_r_ia[int(0.8 * ntrials) - 1, :]
        CE_90_ia = delta_r_ia[int(0.9 * ntrials) - 1, :]

        LE_70_ia = delta_z_ia[int(0.7 * ntrials) - 1, :]
        LE_80_ia = delta_z_ia[int(0.8 * ntrials) - 1, :]
        LE_90_ia = delta_z_ia[int(0.9 * ntrials) - 1, :]

        CE_70_icp = delta_r_icp[int(0.7 * ntrials) - 1, :]
        CE_80_icp = delta_r_icp[int(0.8 * ntrials) - 1, :]
        CE_90_icp = delta_r_icp[int(0.9 * ntrials) - 1, :]

        LE_70_icp = delta_z_icp[int(0.7 * ntrials) - 1, :]
        LE_80_icp = delta_z_icp[int(0.8 * ntrials) - 1, :]
        LE_90_icp = delta_z_icp[int(0.9 * ntrials) - 1, :]


        if (plot_errors):
        #Plot CE and LE
            fig_ia_CE = plt.figure()
            ax_ia_CE = fig_ia_CE.add_subplot(111);
            plt.hold(True);
            plt.axis(tight=True);
            ax_ia_CE.plot(CE_70_ia, "--s", color="green", label= "CE_70");
            ax_ia_CE.plot(CE_80_ia, "--^", color="magenta", label= "CE_80");
            ax_ia_CE.plot(CE_90_ia, "--*", color="blue", label= "CE_90");
            ax_ia_CE.plot( delta_r, "--o", color="cyan", label=  "GT");
            ax_ia_CE.set_xlabel('Fiducial Marker (index)',fontsize= 20);
            ax_ia_CE.set_ylabel('Error (meters)',fontsize= 20);
            ax_ia_CE.legend(loc='best', frameon=False);
            # ax_ia_CE.set_title('IA CE')
            fname = trials_root + "/GEO_results/IA_CE_" + desc_name + ".pdf"
            fig_ia_CE.savefig(fname, transparent=True, pad_inches=5)



            fig_ia_LE = plt.figure()
            ax_ia_LE = fig_ia_LE.add_subplot(111);
            plt.hold(True);
            plt.axis(tight=True);
            ax_ia_LE.plot(LE_70_ia, "--s", color="green", label= "LE_70");
            ax_ia_LE.plot(LE_80_ia, "--^", color="magenta", label= "LE_80");
            ax_ia_LE.plot(LE_90_ia, "--*", color="blue", label= "LE_90");
            ax_ia_LE.plot( delta_z, "--o", color="cyan", label=  "GT");
            ax_ia_LE.set_xlabel('Fiducial Marker (index)',fontsize= 20);
            ax_ia_LE.set_ylabel('Error (meters)',fontsize= 20);
            ax_ia_LE.legend(loc='best', frameon=False);
            # ax_ia_LE.set_title('IA LE')
            fname = trials_root + "/GEO_results/IA_LE_" + desc_name + ".pdf"
            fig_ia_LE.savefig(fname, transparent=True, pad_inches=5)

            fig_icp_CE = plt.figure()
            ax_icp_CE = fig_icp_CE.add_subplot(111);
            plt.hold(True);
            plt.axis(tight=True);
            ax_icp_CE.plot(CE_70_icp, "--s", color="green", label= "CE_70");
            ax_icp_CE.plot(CE_80_icp, "--^", color="magenta", label= "CE_80");
            ax_icp_CE.plot(CE_90_icp, "--*", color="blue", label= "CE_90");
            ax_icp_CE.plot( delta_r, "--o", color="cyan", label=  "GT");
            ax_icp_CE.set_xlabel('Fiducial Marker (index)',fontsize= 20);
            ax_icp_CE.set_ylabel('Error (meters)',fontsize= 20);
            ax_icp_CE.legend(loc='best', frameon=False);
            # ax_icp_CE.set_title('ICP CE')
            fname = trials_root + "/GEO_results/ICP_CE_" + desc_name + ".pdf"
            fig_icp_CE.savefig(fname, transparent=True, pad_inches=5)


            fig_icp_LE = plt.figure()
            ax_icp_LE = fig_icp_LE.add_subplot(111);
            plt.hold(True);
            plt.axis(tight=True);
            ax_icp_LE.plot(LE_70_icp, "--s", color="green", label= "LE_70");
            ax_icp_LE.plot(LE_80_icp, "--^", color="magenta", label= "LE_80");
            ax_icp_LE.plot(LE_90_icp, "--*", color="blue", label= "LE_90");
            ax_icp_LE.plot( delta_z, "--o", color="cyan", label=  "GT");
            ax_icp_LE.set_xlabel('Fiducial Marker (index)',fontsize= 20);
            ax_icp_LE.set_ylabel('Error (meters)',fontsize= 20);
            ax_icp_LE.legend(loc='best', frameon=False);
            # ax_icp_LE.set_title('ICP LE')
            fname = trials_root + "/GEO_results/ICP_LE_" + desc_name + ".pdf"
            fig_icp_LE.savefig(fname, transparent=True, pad_inches=5)


            # axT.set_xlim((0,505) );
            # axT.set_yticks(np.arange(0.0,250.0,20));
            # # axT.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
            # #             ncol=4, mode="expand", borderaxespad=0.)
            #
            # figT.savefig("/Users/isa/Experiments/reg3d_eval/downtown_dan/T_error.pdf", transparent=True, pad_inches=5)

            # plt.show();

    # import pdb; pdb.set_trace()



def setlogging(logfile=None):
    level = logging.DEBUG
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    # create formatter and add it to the handlers
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)

    # create file handler which logs error messages
    if logfile:
        print "Logging to file"
        fh = logging.FileHandler(logfile)
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

     #test logging
    logger.debug("debug message")
    logger.info("info message")
    logger.warn("warn message")
    logger.error("error message")
    logger.critical("critical message")

    return logger

if __name__ == '__main__':

    # initialize the parser object:
    parser = argparse.ArgumentParser(description="Export PLY to PCD file")

    # define options here:
    parser.add_argument("-v", "--verbose",      action='store',    type = bool,   dest="verbose",   default=True,  help="Write debug log to log_file")
    parser.add_argument("-L", "--log", dest="logfile", help="write debug log to log_file")

    args = parser.parse_args(argv)

    # set up logging
    if args.verbose:
        status = main(args.logfile)
    else:
        status = main()

    sys.exit(status)
