#!/usr/bin/env python
# encoding: utf-8
"""
corr_registration_tool

Created by Maria Isabel Restrepo on 2012-10-18.
Copyright (c) 2012 . All rights reserved.
Tools to
Pick pixels on 2 images.
Generate 3d point from expected exp_depth
Backproject 3d points onto images
"""
import sys
import os


import matplotlib
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import numpy as np


from boxm2_scene_adaptor import *
from boxm2_adaptor import *;
from boxm2_scene_adaptor import *;
from vpgl_adaptor import *;
from bbas_adaptor import *;
from vil_adaptor import *;
from boxm2_tools_adaptor import *;
# from matplotlib.widgets import Button

img_height = 720

class PointPicker:
    def __init__(self, points, im_ax, axis, p_file, im_idx):
        self.points = points
        self.xs = list(points.get_xdata())
        self.ys = list(points.get_ydata())
        self.labels = list()
        self.im_ax = im_ax
        self.ax = axis
        self.pFile = p_file
        self.im_idx = im_idx
        self.cid1 = points.figure.canvas.mpl_connect('button_press_event', self)
        self.cid2 = im_ax.figure.canvas.mpl_connect('key_press_event', self.key_press)
        self.glued = False  # once image is glued you can pick points
        self.point_mat = []

    def __call__(self, event):
        # print 'click', event
        # print 'button=%d, key=%s, x=%d, y=%d, xdata=%f, ydata=%f'%(
        # event.button, event.key, event.x, event.y, event.xdata, event.ydata)
        if event.inaxes != self.points.axes:
            return

        if self.glued == False:
            return

        #Add point - left click + a
        if event.button == 1 and event.key == 'a':
            self.xs.append(event.xdata)
            self.ys.append(event.ydata)
            self.points.set_data(self.xs, self.ys)
            l = self.ax.annotate(
            str(len(self.xs)),
            xy = (event.xdata, event.ydata), xytext = (-10, 10),
            bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            fontproperties= matplotlib.font_manager.FontProperties(family='Helvetica', size=8))
            self.labels.append(l)
            self.points.figure.canvas.draw()

        #remove last point - left click + r
        if event.button == 1 and event.key == 'r':
            self.xs.pop()
            self.ys.pop()
            self.points.set_data(self.xs, self.ys)
            to_remove = self.labels.pop()
            to_remove.remove()
            self.points.figure.canvas.draw()


    def key_press(self, event):
        # print 'click', event
        # print 'key=%s' % (event.key)

        if event.key == 'right' and self.glued == False:
            if self.im_idx < len(imgs) - 1:
                self.im_idx = self.im_idx + 1

            img_file = imgs[self.im_idx]
            img = mpimg.imread(img_file)

            #reset the image data
            self.im_ax.set_array(img)
            self.im_ax.figure.canvas.draw()

        if event.key == 'left' and self.glued == False:
            if self.im_idx > 0:
                self.im_idx = self.im_idx - 1

            img_file = imgs[self.im_idx]
            img = mpimg.imread(img_file)

            #reset the image data
            self.im_ax.set_array(img)
            self.im_ax.figure.canvas.draw()

        #glue the image - only at this point you can pick points
        if event.key == 'G':
            self.glued = True;

        #clear all points - left click + c
        # it also unglues the image
        if event.key == 'c':
            self.clear_points();
            self.glued = False;

        #save point to disk
        if event.key == 'd':
            self.save_points()

    def save_points(self):
        self.point_mat = np.zeros((len(self.xs), 2))
        # import pdb; pdb.set_trace()
        self.point_mat[:, 0] = self.xs
        self.point_mat[:, 1] = img_height*np.ones((len(self.ys))) -np.array(self.ys)
        header = (imgs[self.im_idx] + '\n' +
                  cams[self.im_idx] + '\n')
        fos = open(self.pFile, 'w')
        fos.write( header )
        np.savetxt(fos, self.point_mat, fmt='%.5f %.5f', delimiter=' ')
        fos.close()

    def clear_points(self):
        while len(self.xs) > 0:
            self.xs.pop()
            self.ys.pop()
            self.points.set_data(self.xs, self.ys)
            to_remove = self.labels.pop()
            to_remove.remove()
        self.points.figure.canvas.draw()


class SceneBackProjector:
    def __init__(self, points3d, labels, points_ax, im_ax,
                 axis, im_idx, imgs, cams):
        self.points3d = points3d
        self.points_ax = points_ax
        self.xs = list(points_ax.get_xdata())
        self.ys = list(points_ax.get_ydata())
        self.labels = labels
        self.im_ax = im_ax
        self.ax = axis
        self.im_idx = im_idx
        self.cid = im_ax.figure.canvas.mpl_connect('key_press_event', self.key_press)
        self.imgs = imgs
        self.cams = cams

    def key_press(self, event):
        # print 'click', event
        # print 'key=%s' % (event.key)

        if event.key == 'right':
            if self.im_idx < len(self.imgs) - 1:
                self.im_idx = self.im_idx + 1

            img_file = self.imgs[self.im_idx]
            img = mpimg.imread(img_file)
            print "Showing image: ", img_file

            #reset the point data
            self.backproject()
            #reset the image data
            self.im_ax.set_array(img)

            #refresh the canvas
            self.im_ax.figure.canvas.draw()
            self.points_ax.figure.canvas.draw()

        if event.key == 'left':
            if self.im_idx > 0:
                self.im_idx = self.im_idx - 1

            img_file = self.imgs[self.im_idx]
            img = mpimg.imread(img_file)
            print "Showing image: ", img_file

            #reset the point data
            self.backproject()
            #reset the image data
            self.im_ax.set_array(img)

            #refresh the canvas
            self.im_ax.figure.canvas.draw()
            self.points_ax.figure.canvas.draw()

    def backproject(self):
        cam = load_perspective_camera(self.cams[self.im_idx])
        print "Reading camera: ", self.cams[self.im_idx]

        self.clear_points()
        for i, point in zip(range(len(self.points3d)), self.points3d):
            imgPoint = project_point(cam, point[0], point[1], point[2])
            u = imgPoint[0]
            v = imgPoint[1]
            print "3d point", point
            print "2d point", imgPoint

            l = self.ax.annotate(
            str(i),
            xy = (u,v), xytext = (-10, 10),
            bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            fontproperties= matplotlib.font_manager.FontProperties(family='Helvetica', size=8))
            self.labels.append(l)
            self.xs.append(u)
            self.ys.append(v)
        self.points_ax.set_data(self.xs, self.ys)
        #cleanup
        remove_from_db(cam)

    def clear_points(self):
        while len(self.xs) > 0:
            self.xs.pop()
            self.ys.pop()
            self.points_ax.set_data(self.xs, self.ys)
            to_remove = self.labels.pop()
            to_remove.remove()
        self.points_ax.figure.canvas.draw()

class SceneProjector:

    def __init__(self, scene_root, scene_name, device, points2d, im_idx):
        self.points2d = points2d
        self.im_idx = im_idx
        self.points3d = np.zeros((len(points2d), 3))
        self.computed3d = False
        self.scene = self.init_scene(scene_root, scene_name, device)

    def init_scene(self, scene_file, scene_name, device):
        scene_path = scene_root + "/" + scene_name
        if not os.path.exists(scene_path):
            print "SCENE NOT FOUND! ", scene_path
            sys.exit(-1)
        scene = boxm2_scene_adaptor(scene_path, device)
        return scene

    def compute_3d_points(self):

        if self.computed3d:
            return

        for i, p2d in zip(range(len(points2d)), points2d):
            exp_depth, pt3d = self.get_point(int(p2d[0]), int(p2d[1]))
            self.points3d[i, :] = pt3d

        self.computed3d = True

    def get_point(self, u, v):
        cam = load_perspective_camera(cams[self.im_idx])
        len_array_1d = []
        alpha_array_1d = []
        vis_array_1d = []
        tabs_array_1d = []
        point_array_1d = []
        len_array_1d, alpha_array_1d, vis_array_1d, tabs_array_1d, point_array_1d, nelems = self.scene.get_info_along_ray(cam,u,v, "boxm2_mog3_grey");
        exp_depth = 0.0
        sum_weights = 0.0
        #print (point_array_1d)
        for i in range(0, len(len_array_1d)):
            weight = alpha_array_1d[i] * vis_array_1d[i]
            exp_depth = exp_depth + weight * tabs_array_1d[i]
            sum_weights = sum_weights + weight

        print weight
        pt =[0.0, 0.0, 0.0]
        pt[0],   pt[1], pt[2] = get_3d_from_depth(cam,u,v,exp_depth/sum_weights)
        return exp_depth,pt
