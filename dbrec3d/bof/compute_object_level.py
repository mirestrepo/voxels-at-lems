#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22, 2011

@author:Isabel Restrepo

Save the level of the smallest cell entirely containing the object
"""

import os;
import dbrec3d_batch
import time
import optparse
import sys
import glob

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

         
#*******************The Main Algorithm ************************#
if __name__=="__main__":
  dbrec3d_batch.register_processes();
  dbrec3d_batch.register_datatypes();
  
  #Parse inputs
  print ("******************************Compute Object level***************************")
  parser = optparse.OptionParser(description='Init Category info');
  parser.add_option('--bof_dir', action="store", dest="bof_dir");
  
  options, args = parser.parse_args();

  bof_dir = options.bof_dir;
 
  if not os.path.isdir(bof_dir +"/"):
    print "Invalid bof Dir"
    sys.exit(-1);
    
  #load category info 
  dbrec3d_batch.init_process("bofLoadCategoryInfoProces");
  dbrec3d_batch.set_input_string(0, bof_dir);
  dbrec3d_batch.set_input_string(1, "bof_info_train.xml")
  dbrec3d_batch.set_input_string(2, "bof_category_info_old.xml")
  dbrec3d_batch.run_process();
  (id, type) = dbrec3d_batch.commit_output(0);
  categories= dbvalue(id, type);
  
  #load category info 
  dbrec3d_batch.init_process("bof_object_level_process");
  dbrec3d_batch.set_input_from_db(0, categories);
  dbrec3d_batch.run_process();



    