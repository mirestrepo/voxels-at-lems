#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon March 24, 2011

@author:Isabel Restrepo

Script used to initiallize bof_info.xml file from a global taylor info file
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
  parser = optparse.OptionParser(description='Init BOF info');

  parser.add_option('--taylor_dir', action="store", dest="taylor_dir");
  parser.add_option('--bof_dir', action="store", dest="bof_dir");
  parser.add_option('--num_means', action="store", dest="num_means", type="int", default =50)

  
  options, args = parser.parse_args();

  taylor_dir = options.taylor_dir;
  bof_dir = options.bof_dir;
  num_means = options.num_means;

  if not os.path.isdir(taylor_dir +"/"):
    print "Invalid taylor Dir"
    sys.exit(-1);
    
  if not os.path.isdir(bof_dir +"/"):
    os.mkdir(bof_dir +"/");
  
  start_time = time.time();
   
  dbrec3d_batch.init_process("bofInitInfoFileProcess");
  dbrec3d_batch.set_input_string(0,taylor_dir);
  dbrec3d_batch.set_input_unsigned(1,num_means);
  dbrec3d_batch.set_input_string(2,bof_dir);

  dbrec3d_batch.run_process();

  print ("Total running time: ");
  print(time.time() - start_time);
    