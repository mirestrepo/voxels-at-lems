#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon March 24, 2011

@author:Isabel Restrepo

Script used to combined the category-distributions learnt by all scenes
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

  #Parse inputs
  print ("******************************Combining Quantization***************************")
  parser = optparse.OptionParser(description='Init Category info');

  parser.add_option('--bof_dir', action="store", dest="bof_dir");
  parser.add_option('--k_means_dir', action="store", dest="k_means_dir");
  parser.add_option('--class_histograms_dir', action="store", dest="class_histograms_dir");

  options, args = parser.parse_args();

  bof_dir = options.bof_dir;
  k_means_dir = options.k_means_dir;
  class_histograms_dir = options.class_histograms_dir;
 
  if not os.path.isdir(bof_dir +"/"):
    print "Invalid bof Dir"
    sys.exit(-1);
    
  if not os.path.isdir(class_histograms_dir +"/"):
    print "Invalid histogram Dir"
    sys.exit(-1);
    
  output_path = class_histograms_dir + "/all_scenes"  
  if not os.path.isdir(output_path +"/"):
    os.mkdir(output_path +"/");
  
  codebook_file = k_means_dir + "/lowest_sse_means.txt"

  start_time = time.time();
   
  dbrec3d_batch.init_process("bofCombineQuantizationProcess");
  dbrec3d_batch.set_input_string(0,bof_dir);
  dbrec3d_batch.set_input_string(1,class_histograms_dir + "/scene_");
  dbrec3d_batch.set_input_string(2,codebook_file);
  dbrec3d_batch.set_input_string(3,output_path);

  dbrec3d_batch.run_process();

  dbrec3d_batch.clear();
  
  print ("Total running time: ");
  print(time.time() - start_time);
    