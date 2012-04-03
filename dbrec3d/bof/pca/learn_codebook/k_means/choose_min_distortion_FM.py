#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14, 2011

@author:Isabel Restrepo

A script to chose the k-means that minimize distortion/sse over all group-means(FM) 
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
from numpy import log, ceil
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

  parser.add_option('--k_means_dir', action="store", dest="k_means_dir");

  
  options, args = parser.parse_args()

  k_means_dir = options.k_means_dir;   #path where all k means results are saved

  if not os.path.isdir(k_means_dir +"/"):
    print "Invalid bof Dir"
    sys.exit(-1);
    
  FM_path = k_means_dir + "/FM";  
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
  
  print "In python output string: " + str(best_mean_file)
  
  base_file =  re.sub('\_info$', '', best_mean_file)
  
  best_fm_file = FM_path + '/' + base_file + ".txt";
  print "In python best_fm_file: " + best_fm_file

  lowest_sse_file = k_means_dir + "/lowest_sse_means.txt"
  shutil.copy (best_fm_file, lowest_sse_file)

  best_fm_info_file =  FM_path + '/' + best_mean_file + ".xml";
  lowest_sse_info_file = k_means_dir + "/lowest_sse_means_info.xml"
  shutil.copy (best_fm_info_file, lowest_sse_info_file)

  print ("Total running time: ");
  print(time.time() - start_time);
  
    