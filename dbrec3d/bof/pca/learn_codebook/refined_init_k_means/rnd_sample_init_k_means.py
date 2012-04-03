#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14, 2011

@author:Isabel Restrepo

Random sample features to initialize k-mean. Each block is processed in a separate thread.
"""
import os;
import dbrec3d_batch
import multiprocessing
import Queue 
import time
import random
import optparse
import sys
from numpy import log, ceil
from xml.etree.ElementTree import ElementTree

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
  parser = optparse.OptionParser(description='bof Statistics Pass 0');

  parser.add_option('--bof_dir', action="store", dest="bof_dir");
  parser.add_option('--init_k_means_dir', action="store", dest="init_k_means_dir");
  parser.add_option('--num_means', action="store", dest="num_means", type="int", default =0)
  
  options, args = parser.parse_args()

  bof_dir = options.bof_dir;
  num_means = options.num_means;
  init_k_means_dir = options.init_k_means_dir;

  if not os.path.isdir(bof_dir +"/"):
    print "Invalid bof Dir"
    sys.exit(-1);
    
  if not os.path.isdir(init_k_means_dir +"/"):
    os.mkdir(init_k_means_dir +"/");
    
    
  dbrec3d_batch.init_process("bofRndMeansProcess");
  dbrec3d_batch.set_input_string(0,bof_dir);
  dbrec3d_batch.set_input_int(1,num_means);
  dbrec3d_batch.set_input_string(2, init_k_means_dir + "/sp_means.txt");
  dbrec3d_batch.run_process();
  
  dbrec3d_batch.clear();

