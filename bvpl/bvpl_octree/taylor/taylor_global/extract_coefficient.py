#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon March 24, 2011

@author:Isabel Restrepo

Script used to extract taylor resposens for visual inspection
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

  print("**********Executing: extract_coefficient.py **********")
  bvpl_octree_batch.register_processes();
  bvpl_octree_batch.register_datatypes();

  #Parse inputs
  parser = optparse.OptionParser(description='Init taylor');

  parser.add_option('--taylor_dir', action="store", dest="taylor_dir");
  parser.add_option('--aux_scene_dir', action="store", dest="aux_scene_dir");
  
  options, args = parser.parse_args();

  taylor_dir = options.taylor_dir;
  aux_scene_dir = options.aux_scene_dir;


  temp_results_dir = taylor_dir + "/temp";

  if not os.path.isdir(taylor_dir +"/"):
    print "Invalid taylor Dir"
    sys.exit(-1);
  
  start_time = time.time();
   
  scene_id = 9;
  component = 3;
   
  bvpl_octree_batch.init_process("bvplExploreCoefficientSceneProcess");
  bvpl_octree_batch.set_input_string(0,taylor_dir);
  bvpl_octree_batch.set_input_int(1,scene_id);  #scene id
  bvpl_octree_batch.set_input_int(2,component);  #component
  bvpl_octree_batch.run_process();
  (id,type)= bvpl_octree_batch.commit_output(0);
  scene = dbvalue(id,type);
  
  print("Save Scene");
  bvpl_octree_batch.init_process("boxmSaveSceneRawProcess");
  bvpl_octree_batch.set_input_from_db(0,scene);
  bvpl_octree_batch.set_input_string(1, aux_scene_dir + "/scene" + str(scene_id) + "coeff" + str(component));
  bvpl_octree_batch.set_input_unsigned(2,0);
  bvpl_octree_batch.set_input_unsigned(3,1);
  bvpl_octree_batch.run_process();

  print ("Total running time: ");
  print(time.time() - start_time);