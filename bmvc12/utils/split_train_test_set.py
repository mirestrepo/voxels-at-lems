#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo
May 1, 2012
A scrit to randomly split the train/test samples
"""
import os
import sys
import random
import glob

from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring
import xmlpp

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


#*******************The Main Algorithm ************************#
if __name__=="__main__":
  #percentile = opts.percentile;
  #trial = opts.trial;

  percentile = 90;

  #path to where all scenes are
  scenes_root_path="/data/helicopter_providence_3_12"
  bof_experiments_root="/Users/isa/Experiments/bof_bmvc12"
  
  verbose=False; #if set to False, the standard output is redirected to a .log file
  sites= [1,2,3,6,7,8,10,11,12,16,18,21,22,23,25,26,27];


  if (len(sites)!=17):
    print "Wrong number of sites"
    sys.exit(9);

  
  for trial in range(0,5):  
    
    trial_dir = bof_experiments_root + "/trial_" + str(trial)

    train_file = trial_dir + "/bof_category_train_info.xml"
    test_file = trial_dir + "/bof_category_test_info.xml"


    info_root_train = Element("bof_category_info")
    info_root_test = Element("bof_category_info") 

    if not os.path.exists(trial_dir + "/"):
      os.makedirs(trial_dir + "/")

    
    for si in sites:  

      site_name ="site_"+str(si);
      scene_elm_train = SubElement(info_root_train,"scene", {'site_name':site_name});
      scene_elm_test = SubElement(info_root_test, "scene", {'site_name':site_name});

      site_dir = scenes_root_path + "/site_" + str(si)  
      obj_dir = site_dir + "/objects_with_aux"
      
      if not os.path.exists(obj_dir + "/"):
        print "Error: Objects' DIR not found! ", obj_dir
        sys.exit(-1)
        
      categories = glob.glob(obj_dir + "/*" + str(percentile));
          
      for cat in categories:
        
        if not os.path.isdir(cat):
          continue;
        category_name =  os.path.basename( cat)
        category_name = category_name[:-3]
        objs = glob.glob(cat + "/*.ply");

        for file_in in objs:
            #features get written to a .txt file for now -- PCL reader/writter doesn't handle variable length descriptos
            obj_name = os.path.basename(file_in);
            obj_name = obj_name[:-len(".ply")]  
            
            if (random.randint(0,1) == 1):          
              SubElement(scene_elm_train, "object", {'class_name':category_name,'ply_name':obj_name}) 
            else :
              SubElement(scene_elm_test, "object", {'class_name':category_name,'ply_name':obj_name}) 

            
    train_tree = ElementTree(info_root_train) ;   
    test_tree = ElementTree(info_root_test) ;   

   
    outputfile= open(train_file, 'w')
#    string_train = "<xml>" +  + "</xml>"
    xmlpp.pprint(tostring(info_root_train, 'UTF-8'), outputfile)
    outputfile.close()  
    
    outputfile= open(test_file, 'w')
#    string_test = "<xml>" +  + "</xml>"
    xmlpp.pprint(tostring(info_root_test, 'UTF-8'), outputfile)
    outputfile.close()         
       
  print "Done"

  sys.exit(0)
