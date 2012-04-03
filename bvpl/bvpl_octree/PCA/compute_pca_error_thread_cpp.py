# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14, 2011

@author:Isabel Restrepo

Compuets PCA reconstruction error. Each block is processed in a separate thread.
This script assumes that the pca basis has been computed as gone by extract_pca_kernels.py
"""
import os;
import bvpl_octree_batch
import multiprocessing
import Queue 
import time
import random
import optparse

#time.sleep(30);

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

            
#*******************The Main Algorithm ************************#
if __name__=="__main__":
  bvpl_octree_batch.register_processes();
  bvpl_octree_batch.register_datatypes();

  model_dir="/Users/isa/Experiments/CapitolBOXM_6_4_4";
  model_name="capitol_scene";
  pca_dir="/Users/isa/Experiments/PCA/CapitolBOXM_6_4_4/thread_test";
 

  if not os.path.isdir(model_dir +"/"):
      print "Invalid Model Dir"
      sys.exit(-1);

  if not os.path.isdir(pca_dir +"/"):
      print "Invalid PCA Dir"
      sys.exit(-1);


  print("Loading Data Scene");
  bvpl_octree_batch.init_process("boxmCreateSceneProcess");
  bvpl_octree_batch.set_input_string(0,  model_dir +"/mean_color_scene.xml");
  bvpl_octree_batch.run_process();
  (scene_id, scene_type) = bvpl_octree_batch.commit_output(0);
  data_scene= dbvalue(scene_id, scene_type);

  #Load pca scenes
  pca_feature_dim = 1;
  print("Loading PCA Error Scenes");
  bvpl_octree_batch.init_process("bvplLoadPCAErrorSceneProcess");
  bvpl_octree_batch.set_input_from_db(0, data_scene);
  bvpl_octree_batch.set_input_string(1, pca_dir);
  bvpl_octree_batch.set_input_unsigned(2, pca_feature_dim); #dimension pca feature
  bvpl_octree_batch.run_process();
  (id, type) = bvpl_octree_batch.commit_output(0);
  pca_scenes = dbvalue(id, type);

  #Begin multiprocessing
  work_queue=multiprocessing.Queue();
  job_list=[];


  #For each dimension
  for dim in range(0,1):
      print("Computing Error Scene");
      bvpl_octree_batch.init_process("bvplComputePCAErrorSceneProcess");
      bvpl_octree_batch.set_input_string(0,pca_dir);
      bvpl_octree_batch.set_input_from_db(1,pca_scenes);
      bvpl_octree_batch.set_input_unsigned(2, dim);
      bvpl_octree_batch.run_process();
            

    
    