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
from numpy import log, ceil

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
  
  #scene2 = CapitolBOXMSmall
  scene_blocks.append([2,1,1,1]);
  
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
  
               
  nfiles_prev_pass = i;
  #Number of leyers in the binary (pairing) tree
  nlevels = int(ceil(log(nfiles_prev_pass)/log(2)))
    
  print (" Number of levels to process: " + str(nlevels))
     
  for level in range(0,nlevels):
      nfiles_this_pass = 0;
      print (" Number of files at current level: " + str(level) + ", is: " + str(nfiles_prev_pass))
      for file_idx  in range(0, nfiles_prev_pass, 2):
          
          stats_file1 = temp_results_dir + "/stats_pass_" + str(level)+ "_" + str(file_idx) + ".txt";
          stats_file2 = temp_results_dir + "/stats_pass_" + str(level)+ "_" + str(file_idx+1) + ".txt";

          stats_file_out = temp_results_dir + "/stats_pass_" + str(level+1)+ "_" + str(nfiles_this_pass) + ".txt";
          
          bvpl_octree_batch.init_process("bvplCombinePairwiseStatisticsProcess");
          bvpl_octree_batch.set_input_string(0,stats_file1);
          bvpl_octree_batch.set_input_string(1,stats_file2);
          bvpl_octree_batch.set_input_string(2,stats_file_out);
          bvpl_octree_batch.run_process();
          
          nfiles_this_pass = nfiles_this_pass +1;
          
      nfiles_prev_pass = nfiles_this_pass;

    