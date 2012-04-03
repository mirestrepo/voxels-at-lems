#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14, 2011

@author:Isabel Restrepo

A script to run (fast) k-means on J sets of random subsamples
"""
import os;
import dbrec3d_batch
import multiprocessing
import Queue 
import time
import random
import optparse
import sys
import shutil
from math import log, ceil
from xml.etree.ElementTree import ElementTree
import re

#time.sleep(30);

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

           
                   
#*******************The Main Algorithm ************************#
if __name__=="__main__":
  dbrec3d_batch.register_processes();
  dbrec3d_batch.register_datatypes();


  #Parse inputs
  parser = optparse.OptionParser(description='bof choose minumum distortion FM_i means');

  parser.add_option('--init_k_means_dir', action="store", dest="init_k_means_dir");
  parser.add_option('--k_means_dir', action="store", dest="k_means_dir");

  
  options, args = parser.parse_args()

  init_k_means_dir = options.init_k_means_dir;   #path where all FM_i means are saved 
  k_means_dir = options.k_means_dir;

  if not os.path.isdir(init_k_means_dir +"/"):
    print "Invalid bof Dir"
    sys.exit(-1);
    
  FM_path = init_k_means_dir + "/FM";  
  if not os.path.isdir(FM_path +"/"):
    print "Invalid FM_path Dir"
    sys.exit(-1);
    
  if not os.path.isdir(k_means_dir +"/"):
    os.mkdir(k_means_dir +"/");
    
  #Begin
  start_time = time.time();

  mean_file_sfx = FM_path + "/FM_" ;
  dbrec3d_batch.init_process("bofChooseMinDistortionClusteringProcess");
  dbrec3d_batch.set_input_string(0, mean_file_sfx);
  dbrec3d_batch.run_process();
  (id, type) = dbrec3d_batch.commit_output(0);
  mean_idx_val = dbvalue(id, type);
  best_mean_file = dbrec3d_batch.get_output_string(mean_idx_val.id);
  dbrec3d_batch.clear();

  print "output string: " + str(best_mean_file)
  
  base_file =  re.sub('\_info$', '', best_mean_file)
  
  best_fm_file = FM_path + '/' + base_file + ".txt";
  kmeans_init_means_file = k_means_dir + "/sp_means.txt"
  shutil.copy (best_fm_file, kmeans_init_means_file)

  print ("Total running time: ");
  print(time.time() - start_time);

  
    