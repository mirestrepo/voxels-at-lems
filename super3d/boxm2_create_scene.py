#THIS IS /helicopter_providence/middletown_3_29_11/site1_planes/boxm2_site1_1/boxm2_create_scene.py
from boxm2WriteSceneXML import *
import optparse
from xml.etree.ElementTree import ElementTree
import os, sys


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

#PARAMETERS
ntrees=32
max_num_lvls=4
min_pt = [minx, miny, minz]
max_pt = [maxx, maxy, maxz]

writeSceneFromBox(boxm2_dir,resolution,min_pt,max_pt,ntrees,max_num_lvls);





