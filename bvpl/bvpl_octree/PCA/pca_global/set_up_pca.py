#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14, 2011

@author:Isabel Restrepo

After the total mean and scatter has been computed, this script is used to compute PCA.
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
import glob

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
  parser = optparse.OptionParser(description='Combine Pairwise Statistics');

  parser.add_option('--pca_dir', action="store", dest="pca_dir");
  
  options, args = parser.parse_args();

  pca_dir = options.pca_dir;

  temp_results_dir = pca_dir + "/temp";
  pca_info_file = pca_dir + "/pca_global_info.xml";

  if not os.path.isdir(pca_dir +"/"):
    print "Invalid PCA Dir"
    sys.exit(-1);
    
  if not os.path.isdir(temp_results_dir +"/"):
    print "Invalid temp Dir"
    sys.exit(-1);
  
  
  #Begin multiprocessing
  start_time = time.time();


  nfiles_pass0 = len(glob.glob1(temp_results_dir, 'stats_pass_0*'));
  
  #Number of leyers in the binary (pairing) tree
  nlevels = int(ceil(log(nfiles_pass0)/log(2)))
    
  final_stats_file = temp_results_dir + "/stats_pass_" + str(nlevels)+ "_0.txt";
  bvpl_octree_batch.init_process("bvplGlobalPCAProcess");
  bvpl_octree_batch.set_input_string(0,pca_dir);
  bvpl_octree_batch.set_input_string(1,final_stats_file);
  bvpl_octree_batch.run_process();

  print ("Total running time: ");
  print(time.time() - start_time);
    