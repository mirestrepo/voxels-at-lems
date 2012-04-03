# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14, 2011

@author:Isabel Restrepo

Computes sample data mean and scatter. Each block is processed in a separate thread.
"""
import os;
import bvpl_octree_batch
import multiprocessing
import Queue 
import time
import random
import optparse
import sys

#time.sleep(30);

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

#*******************The Main Algorithm ************************#
if __name__=="__main__":
  bvpl_octree_batch.register_processes();
  bvpl_octree_batch.register_datatypes();

  #ideally inputs should be parsed from the pca_global_info.xml file
  pca_dir="/Users/isa/Experiments/BOF/learn_PCA/tests";
  pca_info_file = pca_dir + "/pca_global_info.xml";
  temp_results_dir = pca_dir + "/temp";

  if not os.path.isdir(pca_dir +"/"):
    print "Invalid PCA Dir"
    sys.exit(-1);
    
  if not os.path.isdir(temp_results_dir +"/"):
    os.mkdir(temp_results_dir +"/");
  
  #a list to keep the dimension (#of blocks) of each scene
  scene_blocks =[];
  
  #scene0 = CapitolBOXMSmall
  scene_blocks.append([0,1,1,1]);
  
  #scene1 = CapitolBOXMSmall
  scene_blocks.append([1,1,1,1]);
  
  #Begin multiprocessing
  work_queue=multiprocessing.Queue();
  job_list=[];
  num_cores = 1;


  #Enqueue jobs
  i = 0;
  for s_idx in range (0, len(scene_blocks)):
      nblocks = scene_blocks[s_idx];
      for block_i in range (0, nblocks[1]):
          for block_j in range (0, nblocks[2]):
              for block_k in range (0, nblocks[3]):
  
                  file_out = temp_results_dir + "/stats_pass_0_" + str(i) + ".txt";
                  idx = scene_blocks[i];
                  
                  bvpl_octree_batch.init_process("bvplPCAGlobalStatisticsProcess");
                  bvpl_octree_batch.set_input_string(0,pca_dir);
                  bvpl_octree_batch.set_input_int(1,s_idx);
                  bvpl_octree_batch.set_input_int(2,block_i);
                  bvpl_octree_batch.set_input_int(3,block_j);
                  bvpl_octree_batch.set_input_int(4,block_k);
                  bvpl_octree_batch.set_input_string(5, file_out);
                  bvpl_octree_batch.run_process();
                  
                  i=i+1;
                  
    