#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo
August 1, 2012
"""
import os, sys, shutil, random
from optparse import OptionParser
from glob import glob


#*****************************************************
# handle inputs                                       
#*****************************************************
parser = OptionParser()
parser.add_option("--inDir", action="store", type="string", dest="inDir", help="root folder containing images and cameras")
parser.add_option("--outDir", action="store", type="string", dest="outDir", help="root folder for output images and cameras")
parser.add_option("-k", action="store", type="int", dest="k", default=100, help="number of training set")

(opts, args) = parser.parse_args()
print opts
print args


if not os.path.exists(opts.inDir + "/"):
  print "Error: Input dir not found! ", opts.inDir
  sys.exit(5)

#*****************************************************
# Get list of imgs and cams
#*****************************************************
train_imgs = opts.inDir + "/frames_grey/*.tif"
train_cams = opts.inDir + "/cameras_KRT/*.txt"

if not os.path.isdir(opts.inDir + "/frames_grey/"):
   print "Image directory doesn't exist. \nPlease place images in: ! ", opts.inDir+ "/imgs/"
   sys.exit(5)

if not os.path.isdir(opts.inDir + "/cameras_KRT/"):
   print "Camera directory doesn't exist. \nPlease place cameras in: ! ", opts.inDir + "/cams_krt/"
   sys.exit(5)
  
imgs = glob(train_imgs)
cams = glob(train_cams)
imgs.sort()
cams.sort() 
if len(imgs) != len(cams) :
  print "Error: CAMS NOT ONE TO ONE WITH IMAGES"
  print "CAMS: ", len(cams), "  IMGS: ", len(imgs)
  sys.exit(5);
  
samples = random.sample(xrange(len(imgs)), opts.k);

if not os.path.exists(opts.outDir):
  print "Output dir not found - creating one ", opts.outDir
  os.makedirs(opts.outDir)
  os.mkdir(opts.outDir + "/imgs/")
  os.mkdir(opts.outDir + "/original_cams_krt/")


for s in samples:
  cam_in = cams[s];
  img_in = imgs[s];
  cam_out= opts.outDir + "/original_cams_krt/" + os.path.basename(cam_in);
  img_out = opts.outDir + "/imgs/" + os.path.basename(img_in);
  shutil.copyfile(cam_in, cam_out);
  shutil.copyfile(img_in, img_out);

#  print "CamIn: ", cam_in, ", CamOut: ", cam_out;
#  print "ImgIn: ", img_in, ", ImgOut: ", img_out;

