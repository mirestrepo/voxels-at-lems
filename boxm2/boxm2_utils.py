#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo
Set of common utilities for boxm2
"""

from xml.etree.ElementTree import ElementTree


def parse_scene_resolution(scene_info_file):
  
    print 'Parsing: ' + scene_info_file
    
    #parse xml file
    scene_info_tree = ElementTree();
    scene_info_tree.parse(scene_info_file);
    
    #find scene paths
    res_elm = scene_info_tree.getroot().find('resolution');
    
    if res_elm is None:
      print "Invalid scene info file: No resolution element"
      sys.exit(-1);
      
    res = res_elm.get('val');
    
    return float(res);