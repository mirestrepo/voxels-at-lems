#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo
May 2, 2012

Pickle all ascii descriptors - Is Pickle fast enough
"""
import multiprocessing
import time
import Queue

#*******************Multiprocessing set up ************************#
class pcl_job():
  def __init__(self, file_in, file_out):
    self.file_in = file_in;
    self.file_out = file_out;

class pcl_worker(multiprocessing.Process):
  
  def __init__(self,work_queue,result_queue):
    # base class initialization
    multiprocessing.Process.__init__(self)
    # job management stuff
    self.work_queue = work_queue
    self.result_queue = result_queue
    self.kill_received = False
  
  def run(self):
    while not self.kill_received:
      # get a task
      try:
        job = self.work_queue.get_nowait()
      except Queue.Empty:
        break
      
      start_time = time.time();
      descriptors = np.genfromtxt(job.file_in, skiprows=1);
      np.save(job.file_out, descriptors)
      print ("Runing time for worker:", self.name)
      
      print(time.time() - start_time);
      
def execute_pcl_jobs(jobs, num_procs=4):
  work_queue=multiprocessing.Queue();
  result_queue=multiprocessing.Queue();
  for job in jobs:
    work_queue.put(job)
  
  for i in range(num_procs):
    worker= pcl_worker(work_queue,result_queue)
    worker.start();
    print("worker with name ",worker.name," started!")


#*******************The Main Algorithm ************************#
if __name__=="__main__":
  
  import os
  import sys
  import numpy as np
  import pickle
  import random
  import glob
  

  #path to where all scenes are
  experiments_root="/Users/isa/Experiments/shape_features_bmvc12"
  verbose=False; #if set to False, the standard output is redirected to a .log file
  sites= [1,2,3,6,7,8,10,11,12,16,18,21,22,23,25,26,27];

  radius = 30;
  percentile = 90;
  descriptor_type= "FPFH";

  if (len(sites)!=17):
    print "Wrong number of sites"
    sys.exit(9);

  job_list = [];  
  
  num_planes = 0;
  num_cars=0;
  num_buildings=0;
  num_houses=0;
  num_parking=0
  
  num_planes_d = 0;
  num_cars_d=0;
  num_buildings_d=0;
  num_houses_d=0;
  num_parking_d=0
     
  for si in sites:  

    site_dir = experiments_root + "/site_" + str(si) 
    
    if not os.path.exists(site_dir + "/"):
      print "Error: Site' DIR not found! ", site_dir
      sys.exit(-1)
      
     
    categories = glob.glob(site_dir + "/"  + descriptor_type + "_" + str(radius) + "/*_" + str(percentile) );
    
      
    for cat in categories:
      
      if not os.path.isdir(cat):
        continue;
        
      objs = glob.glob(cat + "/*.txt");
      
      features_dir = site_dir + "/" + descriptor_type + "_" + str(radius) + "/" +os.path.basename(cat);
      
      if not os.path.exists(features_dir + "/"):
        print "Error: CAT DIR not found! ", features_dir
        sys.exit(-1)
      
      obj_class=os.path.basename(cat)[:-len("_90")] 
      
      if obj_class=="planes":    
         for file_in in objs:
           num_planes = num_planes+1;
           file_out= features_dir + "/" + os.path.basename(file_in);
           print file_out
           with open(file_out, 'r') as f:
              first_line = f.readline().split()
              print first_line 
#              num_planes_d= num_planes_d + n
#      if obj_class=="planes":
#         num_planes = num_planes+1;
#         file_out= features_dir + "/" + os.path.basename(file_in);
#         with open(file_out, 'r') as f:
#            first_line = f.readline()
#            num_planes_d= num_planes_d + int(first_line)

        
      
#      for file_in in objs:
#          #features get written to a .txt file for now -- PCL reader/writter doesn't handle variable length descriptos
#          file_out= features_dir + "/" + os.path.basename(file_in);
          
#          with open(file_out, 'r') as f:
#            first_line = f.readline()

         
  print "Done"

  sys.exit(0)
