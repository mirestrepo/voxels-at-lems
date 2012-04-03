#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon March 24, 2011

@author:Isabel Restrepo

Script used to initiallize auxiliary scenes and information
All it does is write out necessay scene.xml files and compute finest cell lenghts.
"""
import os;
import bvpl_octree_batch
import time
import optparse
import sys

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

         
#*******************The Main Algorithm ************************#
if __name__=="__main__":

  print("**********Executing init_global_taylor.py **********")
  
  bvpl_octree_batch.register_processes();
  bvpl_octree_batch.register_datatypes();

  #Parse inputs
  parser = optparse.OptionParser(description='Init taylor');

  parser.add_option('--taylor_dir', action="store", dest="taylor_dir");
  parser.add_option('--dimension', action="store", dest="dimension", type ="int", default=10);

  options, args = parser.parse_args();

  taylor_dir = options.taylor_dir;
  dimension = options.dimension;

  temp_results_dir = taylor_dir + "/temp";

  if not os.path.isdir(taylor_dir +"/"):
    print "Invalid taylor Dir"
    sys.exit(-1);
  
  start_time = time.time();
   
  bvpl_octree_batch.init_process("bvplInitGlobalTaylorProcess");
  bvpl_octree_batch.set_input_string(0,taylor_dir);
  bvpl_octree_batch.set_input_int(1, dimension);
  bvpl_octree_batch.run_process();

  print ("Total running time: ");
  print(time.time() - start_time);