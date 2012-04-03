#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon March 24, 2011

@author:Isabel Restrepo

Script used to initiallize bof_info.xml file from a global pca info file
"""
import os;
import dbrec3d_batch
import time
import optparse
import sys

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

         
#*******************The Main Algorithm ************************#
if __name__=="__main__":
  dbrec3d_batch.register_processes();
  dbrec3d_batch.register_datatypes();

  #Parse inputs
  print ("******************************Init Category Info***************************")
  parser = optparse.OptionParser(description='Init Category info');

  parser.add_option('--bof_dir', action="store", dest="bof_dir");
  
  options, args = parser.parse_args();

  bof_dir = options.bof_dir;
 
  if not os.path.isdir(bof_dir +"/"):
    print "Invalid bof Dir"
    sys.exit(-1);
  
  start_time = time.time();
   
  dbrec3d_batch.init_process("bofInitCategoryInfoProcess");
  dbrec3d_batch.set_input_string(0,bof_dir);
  dbrec3d_batch.run_process();

  dbrec3d_batch.clear();
  
  print ("Total running time: ");
  print(time.time() - start_time);
    