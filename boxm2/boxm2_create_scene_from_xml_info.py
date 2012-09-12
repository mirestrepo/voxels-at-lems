#!/usr/bin/env python
# encoding: utf-8
#########################################################
# Author: Isabel Restrepo
# 2011
# Create scene.xml from info.xml such as
# *******sample scene_info.xml**************************
#<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
#<bwm_info_for_boxm2>
#<bbox maxx="-1235" maxy="-2703.5" maxz="-3184.6"
#      minx="-1275.3" miny="-2770.8" minz="-3246.1">
#</bbox>
#<resolution val="0.042808">
#</resolution>
#<ntrees ntrees_x="48" ntrees_y="48" ntrees_z="48">
#</ntrees>
#</bwm_info_for_boxm2> 
# **********end scene_info.xml**************************
#########################################################

import optparse
from xml.etree.ElementTree import ElementTree
import os, sys
from boxm2WriteSceneXML import *


#Parse inputs
parser = optparse.OptionParser(description='Create BOXM2 xml file');

parser.add_option('--scene_info', action="store", dest="scene_info");
parser.add_option('--boxm2_dir', action="store", dest="boxm2_dir");


options, args = parser.parse_args();

boxm2_dir = options.boxm2_dir;
scene_info = options.scene_info;
if not os.path.isdir(boxm2_dir + '/'):
    os.mkdir(boxm2_dir + '/');


print 'Parsing: ' 
print scene_info
print boxm2_dir

#parse xml file
tree = ElementTree();
tree.parse(scene_info);

#find scene dimensions
bbox_elm = tree.getroot().find('bbox');

if bbox_elm is None:
  print "Invalid info file: No bbox"
  sys.exit(-1);
  

minx = float(bbox_elm.get('minx'));
miny = float(bbox_elm.get('miny'));
minz = float(bbox_elm.get('minz'));
maxx = float(bbox_elm.get('maxx'));
maxy = float(bbox_elm.get('maxy'));
maxz = float(bbox_elm.get('maxz'));

#find scene resolution

res_elm = tree.getroot().find('resolution');

if res_elm is None:
  print "Invalid info file: No resolution"
  sys.exit(-1);
  
resolution = float(res_elm.get('val'));
  
print ("Resolution: " + str(resolution));

ntrees_elm = tree.getroot().find('ntrees');

#PARAMETERS
ntrees_x= int( ntrees_elm.get('ntrees_x') );
ntrees_y= int( ntrees_elm.get('ntrees_y') );
ntrees_z= int( ntrees_elm.get('ntrees_z') );

max_num_lvls=4
min_pt = [minx, miny, minz]
max_pt = [maxx, maxy, maxz]

writeSceneFromBox(boxm2_dir,resolution,min_pt,max_pt,ntrees_x, ntrees_y, ntrees_z, max_num_lvls);





