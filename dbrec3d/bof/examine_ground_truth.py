#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon March 24, 2011

@author:Isabel Restrepo

Script used to inspect the voxels contained in .ply objects
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

#  scene_in = "/Users/isa/Experiments/helicopter_providence/boxm_scenes/site6/mean_color_scene.xml";
#  ply_path = "/Users/isa/Experiments/helicopter_providence/ground_truth/site6/planes";
#  obj_name = "planes";
  
#  scene_in = "/Users/isa/Experiments/helicopter_providence/boxm_scenes/site8/mean_color_scene.xml";
#  ply_path = "/Users/isa/Experiments/helicopter_providence/ground_truth/site8/residential";
#  obj_name = "residential";
  
  scene_in = "/Users/isa/Experiments/helicopter_providence/boxm_scenes/site1/mean_color_scene.xml";
  ply_path = "/Users/isa/Experiments/helicopter_providence/ground_truth/site1/planes";
  obj_name = "planes";
  
  path_out = ply_path;
   
  if not os.path.isdir(path_out +"/drishti/"):
    os.mkdir(path_out + "/drishti/");
  
  start_time = time.time();
  
  print("Creating a Scene");
  dbrec3d_batch.init_process("boxmCreateSceneProcess");
  dbrec3d_batch.set_input_string(0, scene_in);
  dbrec3d_batch.run_process();
  (id, type) = dbrec3d_batch.commit_output(0);
  scene= dbvalue(id, type);
   
  dbrec3d_batch.init_process("bofExamineGroundTruthProcess");
  dbrec3d_batch.set_input_from_db(0,scene);
  dbrec3d_batch.set_input_string(1,ply_path);
  dbrec3d_batch.set_input_string(2,obj_name);
  dbrec3d_batch.set_input_string(3,path_out);
  dbrec3d_batch.run_process();
  (id, type) = dbrec3d_batch.commit_output(0);
  scene_out= dbvalue(id, type);
  
  print("Save Scene");
  dbrec3d_batch.init_process("boxmSaveSceneRawProcess");
  dbrec3d_batch.set_input_from_db(0,scene_out);
  dbrec3d_batch.set_input_string(1, path_out + "/drishti/labeled_scene_level0");
  dbrec3d_batch.set_input_unsigned(2,0);
  dbrec3d_batch.set_input_unsigned(3,1);
  dbrec3d_batch.run_process();

  print ("Total running time: ");
  print(time.time() - start_time);
    