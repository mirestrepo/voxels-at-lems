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

  #Parse inputs
  parser = optparse.OptionParser(description='Compute PCA Error Scene');

  parser.add_option('--model_dir', action="store", dest="model_dir");
  parser.add_option('--pca_dir', action="store", dest="pca_dir");
  parser.add_option('--num_cores', action="store", dest="num_cores", type="int", default=4);
  parser.add_option('--nblocks_x', action="store", dest="nblocks_x", type="int");
  parser.add_option('--nblocks_y', action="store", dest="nblocks_y", type="int");
  parser.add_option('--nblocks_z', action="store", dest="nblocks_z", type="int");

  options, args = parser.parse_args()

  model_dir = options.model_dir;
  pca_dir = options.pca_dir;
  nblocks_x = options.nblocks_x;
  nblocks_y = options.nblocks_y;
  nblocks_z = options.nblocks_z;
  num_cores = options.num_cores;

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
  pca_feature_dim = 125;
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


  #Enqueue jobs
  for dim in range(0,pca_feature_dim):
      for block_i in range(0,nblocks_x):
            for block_j in range(0,nblocks_y):
                for block_k in range(0,nblocks_z):
                    print("Computing Error Scene");
                    bvpl_octree_batch.init_process("bvplComputePCAErrorBlockProcess");
                    bvpl_octree_batch.set_input_string(0,pca_dir);
                    bvpl_octree_batch.set_input_from_db(1,pca_scenes);
                    bvpl_octree_batch.set_input_int(2, block_i);
                    bvpl_octree_batch.set_input_int(3, block_j);
                    bvpl_octree_batch.set_input_int(4, block_k);
                    bvpl_octree_batch.set_input_unsigned(5, dim);
                    bvpl_octree_batch.run_process();
            

    
    