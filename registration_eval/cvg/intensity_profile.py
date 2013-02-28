#!/usr/bin/env python
# encoding: utf-8
"""
corr_registration_tool

Created by Maria Isabel Restrepo on 2012-10-18.
Copyright (c) 2012 . All rights reserved.
A tool to:
Plot 3-d points in all cameras of a specified scene
Initially thought I would use it to plot intensity profile
but ended up picking intensities manually
"""
import sys
import os
from glob import glob
import argparse

import matplotlib
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# from boxm2_scene_adaptor import *
# from boxm2_adaptor import *;
# from boxm2_scene_adaptor import *;
import vpgl_adaptor as vpgl;
# from bbas_adaptor import *;
import vil_adaptor as vil;
# from boxm2_tools_adaptor import *;
import boxm2_gui_utils as boxm2_gui
# from matplotlib.widgets import Button


if __name__ == '__main__':

    # initialize the parser object:
    parser = argparse.ArgumentParser(description="Export PLY to PCD file")

    # define args here:

    parser.add_argument("-s", "--sceneroot", action="store",
                        type=str, dest="sceneroot",
                        help="root folder for this scene")
    parser.add_argument("-x", "--xmlfile", action="store",
                        type=str, dest="xml",
                        default="model/scene.xml",
                        help="scene file name eg model/scene.xml")
    parser.add_argument("-d", "--device",   action="store",
                        type=str, dest="device",
                        default="gpu1",
                        help="specify gpu (gpu0, gpu1, etc)")
    parser.add_argument("-t", "--imtype", action="store", type=str,
                        dest="itype", default="png",
                        help="specify image type (tif, png, tiff, TIF)")
    parser.add_argument("--idx",      action='store',
                        type=int,    dest="idx",
                        default=0,
                        help="start index of camera and inage to show")
    parser.add_argument("--points3d_file",      action='store',
                        type=str,    dest="points3d_file",
                        default="",
                        help="absolute path to ply file containing 3d points")
    parser.add_argument("--plot_profile",      action='store',
                        type=bool,    dest="plot_profile",
                        default=False,
                        help="show a plot with intensity profile")


    args = parser.parse_args()
    print args


    # handle inputs
    #scene is given as first arg, figure out paths
    scene_root = args.sceneroot
    # Set some update parameters
    scene_name = args.xml
    device = args.device
    img_height = 720

    #######################################################
    # Get list of imgs and cams
    #######################################################

    train_imgs = scene_root + "/imgs/*." + args.itype
    train_cams = scene_root + "/cams_krt/*.txt"
    exp_imgs_dir = scene_root + "/exp_imgs"

    if not os.path.isdir(scene_root + "/imgs/"):
        print "Expected image directory doesn't exist. \nPlease place images in: ! ", scene_root + "/imgs/"
        sys.exit(-1)

    if not os.path.isdir(scene_root + "/cams_krt/"):
        print "Expected camera directory doesn't exist. \nPlease place cameras in: ! ", scene_root + "/cams_krt/"
        sys.exit(-1)

    if not os.path.isdir(exp_imgs_dir + "/"):
        os.mkdir(exp_imgs_dir + "/")

    imgs = glob(train_imgs)
    cams = glob(train_cams)
    imgs.sort()
    cams.sort()
    if len(imgs) != len(cams):
        print "CAMS NOT ONE TO ONE WITH IMAGES"
        print "CAMS: ", len(cams), "  IMGS: ", len(imgs)
        sys.exit()

    points3d = None

    #read the 3-d points
    if not os.path.exists(args.points3d_file):
        print "Error: ", args.points3d_file , " -- does not exist"
        sys.exit()

    #this expects a PLY file with a header of 9 lines -- should be easy to change
    fid = open(args.points3d_file, 'r')
    points3d = np.genfromtxt(fid, dtype=float, delimiter=' ', skip_header=9);
    fid.close()

    print "Points read:"
    print points3d
    # points3d = np.array([[-575, -827, 648]])

    if points3d != None:

        if args.plot_profile:
            figProfile = plt.figure()
            axProfile = figProfile.add_subplot(111)
            axProfile.set_title('Intensity Profile')
            axProfile.hold(True)

            # project 3d point into each image, and gather intensities
            values = []
            idx = []
            # for point_idx, point in zip(range(len(points3d)),points3d):
            point_idx=4
            point=points3d[point_idx]
            for im_idx in range(len(imgs)):
                cam = vpgl.load_perspective_camera(cams[im_idx])
                imgView,ni,nj = vil.load_image(imgs[im_idx]) #vxl image view
                imgPoint = vpgl.project_point(cam, point[0], point[1], point[2])
                u = imgPoint[0]
                v = imgPoint[1]
                val = vil.pixel(imgView, imgPoint)
                if val > 0.0:  #2-d coordinates may fall outside of image
                    values.append(val)
                    idx.append(im_idx)

                axProfile.plot(idx,values, '--*')
            # print "Values: ", values

        im_idx = args.idx

        fig = plt.figure()
        plt.hold(True)

        img_file = imgs[im_idx]
        img = mpimg.imread(img_file)
        ax = fig.add_subplot(111)
        ax.set_title('Reprojection')
        im_ax = ax.imshow(img, origin='upper')
        plt.axis('Tight')

        #show the first image
        print "Showing image: ", img_file
        cam = vpgl.load_perspective_camera(cams[im_idx])
        x_data = []
        y_data = []
        labels = []
        for i, point in zip(range(len(points3d)),points3d):
            imgPoint = vpgl.project_point(cam, point[0], point[1], point[2])
            print imgPoint
            u = imgPoint[0]
            v = imgPoint[1]
            l = ax.annotate(
            str(i),
            xy=(u, v), xytext=(-10, 10),
            bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
            textcoords='offset points', ha='right', va='bottom',
            fontproperties=matplotlib.font_manager.FontProperties(size=8))
            labels.append(l)
            x_data.append(u)
            y_data.append(v)

        points_ax, = ax.plot(x_data, y_data, "s", color="magenta")  # empty line
        projector = boxm2_gui.SceneBackProjector(points3d, labels, points_ax, im_ax, ax, im_idx, imgs, cams)
        plt.show()

