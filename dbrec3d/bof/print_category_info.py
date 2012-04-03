#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 8, 2011

@author:Isabel Restrepo

Split (random) available ojects into test/train
"""

#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon March 24, 2011

@author:Isabel Restrepo

Script used to inspect the voxels contained in .ply objects
"""
import os;
import time
import optparse
import sys
import glob
from xml.etree.ElementTree import ElementTree

#function to parse and xml file containing the model directory and the xml_file_name (without the path)            
def parse_bof_info(file):
    
    print 'Parsing: ' + file
    
    #parse xml file
    bof_tree = ElementTree();
    bof_tree.parse(file);
    
#    scenes_elm = bof_tree.getroot().iterfind('object');
    planes = 0; houses=0; cars = 0; buildings =0; parkings = 0;
    
    for scenes in bof_tree.getroot().iterfind('scene'):
        for objects in scenes.iterfind('object'):
                category = objects.get("class_name");
                #print objects
                if(category=="car"):
                    cars = cars + 1;
                if(category=="plane"):
                    planes = planes + 1
                if(category=="building"):
                    buildings = buildings + 1
                if(category=="parking"):
                    parkings = parkings + 1
                if(category=="house"):
                    houses = houses + 1   
                    
                    
    print 'Number of planes: ' +  str(planes);
    print 'Number of cars: ' +  str(cars);
    print 'Number of houses: ' +  str(houses);
    print 'Number of buildings: ' +  str(buildings);
    print 'Number of parkings: ' +  str(parkings);

#    if scenes_elm is None:
#      print "Invalid bof info file: No scenes element"
#      sys.exit(-1);
#         
# 
#    #find scene paths
#    for s in range(0, len(scenes_elm)):
#        path = scenes_elm[s].get("output_dir");
#        ply_file = scenes_elm[s].get("ply_path");
#        
#        if path is None:
#            print "Invalid info file: Error parsing scene path"
#            sys.exit(-1);
#            
#        if ply_file is None:
#            print "Invalid info file: Error parsing ply_file"
#            sys.exit(-1);
#        
#        model_dirs.append(path); 
#        ply_paths.append(ply_file); 
         
#*******************The Main Algorithm ************************#
if __name__=="__main__":
  
 print '**********************************************' 
 file = '/Users/isa/Experiments/BOF/helicopter_providence/taylor/bof_cross_validation/trial_9/';
 parse_bof_info(file + 'bof_category_train_info.xml');
 parse_bof_info(file + 'bof_category_test_info.xml');

 

    