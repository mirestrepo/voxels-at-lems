#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon March 24, 2011

@author:Isabel Restrepo

Script used to inspect the voxels contained in .ply objects
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
  bvpl_octree_batch.register_processes();
  bvpl_octree_batch.register_datatypes();

  scene_in = "/Users/isa/Experiments/BOF/helicopter_providence/harris_test/aux_dirs/site22/valid_scene_13.xml";
  path_out = "/Users/isa/Experiments/BOF/helicopter_providence/harris_test/aux_dirs/site22"
  
#  scene_in = "/Users/isa/Experiments/BOF/helicopter_providence/harris_test/aux_dirs/site22/harris_scene.xml";
#  path_out = "/Users/isa/Experiments/BOF/helicopter_providence/harris_test/aux_dirs/site22"
  
  
  if not os.path.isdir(path_out +"/drishti/"):
    os.mkdir(path_out + "/drishti/");
  
  start_time = time.time();
  
  print("Creating a Scene");
  bvpl_octree_batch.init_process("boxmCreateSceneProcess");
  bvpl_octree_batch.set_input_string(0, scene_in);
  bvpl_octree_batch.run_process();
  (id, type) = bvpl_octree_batch.commit_output(0);
  scene= dbvalue(id, type);
   
  
  print("Save Scene");
  bvpl_octree_batch.init_process("boxmSaveSceneRawProcess");
  bvpl_octree_batch.set_input_from_db(0,scene);
  bvpl_octree_batch.set_input_string(1, path_out + "/drishti/valid_scene");
  bvpl_octree_batch.set_input_unsigned(2,0);
  bvpl_octree_batch.set_input_unsigned(3,1);
  bvpl_octree_batch.run_process();

  print ("Total running time: ");
  print(time.time() - start_time);
    