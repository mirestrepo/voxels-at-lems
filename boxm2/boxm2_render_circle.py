#!/usr/bin/env python
# encoding: utf-8
# Author : Andrew Miller
# Modifications: Isabel Restrepo

import random, os, sys;
from boxm2_scene_adaptor import *;
from vil_adaptor import *;
from vpgl_adaptor import *;
from bbas_adaptor import *;
from helpers import *;
from glob import glob
from optparse import OptionParser


#######################################################
# handle inputs                                       #
# scene is given as first arg, figure out paths       #
#######################################################

parser = OptionParser()
parser.add_option("-s", "--sceneroot", action="store", type="string", dest="sceneroot", help="root folder for this scene")
parser.add_option("-x", "--xmlfile", action="store", type="string", dest="xml", default="uscene.xml", help="scene.xml file name (model/uscene.xml, model_fixed/scene.xml, rscene.xml)")
parser.add_option("-t", "--imtype", action="store", type="string", dest="itype", default="png", help="specify image type (tif, png, tiff, TIF)")
parser.add_option("-g", "--gpu",   action="store", type="string", dest="gpu",   default="gpu1", help="specify gpu (gpu0, gpu1, etc)")
parser.add_option("-n", "--skipFrame", action="store", type="int", dest="skip", default=1, help="Specify how many images to use in each pass (1=every, 2=every other...)")
parser.add_option("-i", "--initFrame", action="store", type="int", dest="initFrame", default=0, help="Specify the first frame to start ")
parser.add_option("-p", "--printFile" , action="store", type="string", dest="std_file", default="", help="if given, the std out is redirected to this file")

(options, args) = parser.parse_args()
print options
print args

scene_root = options.sceneroot;

# Set some update parameters
SCENE_NAME = options.xml
GPU = options.gpu
SKIP_FRAME = options.skip;
INIT_FRAME = options.initFrame;

if options.std_file != "":
   saveout = sys.stdout   # save initial state of stdout
   print saveout
   print "STD_OUT is being redirected"
   set_stdout(options.std_file)




#######################################################
#Initialize a GPU
#######################################################

print "Initializing GPU"

os.chdir(scene_root)
scene_path = os.getcwd() + "/" + SCENE_NAME
if not os.path.exists(scene_path):
  print "SCENE NOT FOUND! ", scene_path
  sys.exit(-1)
scene = boxm2_scene_adaptor (scene_path, GPU);

#######################################################
# Get list of imgs and cams
#######################################################

train_imgs = os.getcwd() + "/imgs/*." + options.itype
train_cams = os.getcwd() + "/cams_krt/*.txt"
exp_imgs_dir = os.getcwd() + "/exp_imgs_360"

if not os.path.isdir(os.getcwd() + "/imgs/"):
   print "Expected image directory doesn't exist. \nPlease place images in: ! ", os.getcwd() + "/imgs/"
   sys.exit(-1)

if not os.path.isdir(os.getcwd() + "/cams_krt/"):
   print "Expected camera directory doesn't exist. \nPlease place cameras in: ! ", os.getcwd() + "/cams_krt/"
   sys.exit(-1)

if not os.path.isdir(exp_imgs_dir +"/"):
   os.mkdir(exp_imgs_dir + "/");

imgs = glob(train_imgs)
cams = glob(train_cams)
imgs.sort()
cams.sort()
if len(imgs) != len(cams) :
  print "CAMS NOT ONE TO ONE WITH IMAGES"
  print "CAMS: ", len(cams), "  IMGS: ", len(imgs)
  sys.exit();


frames = range(INIT_FRAME,len(imgs)-1, SKIP_FRAME);
print "Training with frames:"
print frames;


#######################################################
# Render circle
#######################################################
for idx, i in enumerate(frames):

    print "Iteration ", idx, " of ", len(frames) , " on chunk " , INIT_FRAME

    #load image and camera
    pcam        = load_perspective_camera(cams[i]);
    img, ni, nj = load_image (imgs[i]);
    exp_img_name = os.path.basename(cams[i])
    exp_img_name = exp_img_name[:-len(".txt")];
    exp_img_name = exp_img_name + ".tiff"
    exp_fname= exp_imgs_dir + "/" + exp_img_name;


    #render an expected image
    print "Viewing Camera", cams[i]
    exp_image = render_grey(scene.scene, scene.active_cache, pcam, ni, nj, scene.device);
    save_image(exp_image, exp_fname)

    #clean up
    remove_from_db([img, pcam, exp_image])
    scene.clear_cache();


#######################################################
#write and clear cache before exiting
#######################################################
scene.clear_cache();
boxm2_batch.clear();

if options.std_file != "":
   reset_stdout();
   print "STD_OUT is being reset"

print "Done"

sys.exit(0)

