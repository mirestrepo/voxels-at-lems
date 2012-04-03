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
import glob

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

         
#*******************The Main Algorithm ************************#
if __name__=="__main__":
  dbrec3d_batch.register_processes();
  dbrec3d_batch.register_datatypes();
  
  scene_in = "/Users/isa/Experiments/helicopter_providence/boxm_scenes/site1/mean_color_scene.xml";
  obj_name = "planes";
  
  ply_path_in ="/Users/isa/Experiments/helicopter_providence/ground_truth_original/site1/planes"
  ply_path_out="/Users/isa/Experiments/helicopter_providence/ground_truth_processed/site1/planes"
  scale = 1e3;
  start_time = time.time();
  
  if not os.path.isdir(ply_path_out +"/"):
    os.makedirs(ply_path_out + "/");
    
  if not os.path.isdir(ply_path_out +"/drishti/"):
    os.mkdir(ply_path_out + "/drishti/");
    
#  ply_files = glob.glob1(ply_path_in, "*.ply");
#  
#  print ply_files
#  
#  for file in ply_files:
#     
#    dbrec3d_batch.init_process("bofScalePLYProcess");
#    dbrec3d_batch.set_input_string(0,ply_path_in + '/' + file);
#    dbrec3d_batch.set_input_string(1,ply_path_out + '/' + file);
#    dbrec3d_batch.set_input_double(2,scale);
#    dbrec3d_batch.run_process();
    
  #*********** Save a scene labeling objects for debigging purposes **************#
  
  print("Creating a Scene");
  dbrec3d_batch.init_process("boxmCreateSceneProcess");
  dbrec3d_batch.set_input_string(0, scene_in);
  dbrec3d_batch.run_process();
  (id, type) = dbrec3d_batch.commit_output(0);
  scene= dbvalue(id, type);

  dbrec3d_batch.init_process("bofExamineGroundTruthProcess");
  dbrec3d_batch.set_input_from_db(0,scene);
  dbrec3d_batch.set_input_string(1,ply_path_out);
  dbrec3d_batch.set_input_string(2,obj_name);
  dbrec3d_batch.set_input_string(3,ply_path_out);
  dbrec3d_batch.run_process();
  (id, type) = dbrec3d_batch.commit_output(0);
  scene_out= dbvalue(id, type);

  print("Save Scene");
  dbrec3d_batch.init_process("boxmSaveSceneRawProcess");
  dbrec3d_batch.set_input_from_db(0,scene_out);
  dbrec3d_batch.set_input_string(1, ply_path_out + "/drishti/labeled_scene_level_0");
  dbrec3d_batch.set_input_unsigned(2,0);
  dbrec3d_batch.set_input_unsigned(3,1);
  dbrec3d_batch.run_process();

  print ("Total running time: ");
  print(time.time() - start_time);
    