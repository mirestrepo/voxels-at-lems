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
  from optparse import OptionParser

  
  parser = OptionParser()
  parser.add_option("-r", "--radius", action="store", type="int", dest="radius", help="radius (multiple of resolution)");
  parser.add_option("-p", "--percent", action="store", type="int", dest="percentile", help="radius (multiple of resolution)");
  parser.add_option("-d", "--descriptor", action="store", type="string", dest="descriptor_type", help="name of the descriptor i.e FPFH");
  parser.add_option("-j", "--jobs", action="store", type="int", dest="njobs", default=8, help="number of jobs");
  
  (opts, args) = parser.parse_args()

  percentile = 90;

  #path to where all scenes are
  experiments_root="/Users/isa/Experiments/shape_features_bmvc12"
  verbose=False; #if set to False, the standard output is redirected to a .log file
  sites= [1,2,3,6,7,8,10,11,12,16,18,21,22,23,25,26,27];

  radius = opts.radius;
  percentile = opts.percentile;
  descriptor_type= opts.descriptor_type;
  num_cores=opts.njobs;

  if (len(sites)!=17):
    print "Wrong number of sites"
    sys.exit(9);

  job_list = [];  
     
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
      
      for file_in in objs:
          #features get written to a .txt file for now -- PCL reader/writter doesn't handle variable length descriptos
          file_out= features_dir + "/" + os.path.basename(file_in);
          file_out = file_out[:-len(".txt")]   
          file_out = file_out  + ".npy";
          if verbose :
            print "Processing: "
            print file_in
            print "Saving to:"
            print file_out 
          current_job = pcl_job(file_in, file_out);
          job_list.append(current_job);
                
  execute_pcl_jobs(job_list, num_cores);
         
  print "Done"

  sys.exit(0)
