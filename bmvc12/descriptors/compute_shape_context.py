#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo
April 29, 2012
Compute the Spin Images. PCL has no OpenMP implementation for this feature and 
PCL/CUDA seem to run out of memory. So let's use Python's multiprocessing module. 
"""
import os
import sys
import glob
import multiprocessing
import Queue 
import time
import random
from optparse import OptionParser
from xml.etree.ElementTree import ElementTree

CONFIGURATION= "Release";
#CONFIGURATION= "Debug";

LEMS_PATH="/Projects/lemsvxl/bin/" + CONFIGURATION + "/lib";

sys.path.append(LEMS_PATH);
sys.path.append("/Projects/lemsvxl/src/contrib/dbrec_lib/dbrec3d/pyscripts");
sys.path.append("/Projects/voxels-at-lems-git/bmvc12/utils");

from dbrec3d_pcl_adaptor import *
from bmvc12_adaptor import *




#*******************Multiprocessing set up ************************#
class pcl_job():
  def __init__(self, file_in, file_out, radius):
    self.file_in = file_in;
    self.file_out = file_out;
    self.radius  = radius;
  

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
      
      dbrec3d_batch.set_stdout('logs/log_' + str(os.getpid())+ ".txt");
     
      #compute shape context descriptor
      compute_descriptor(job.file_in, job.file_out, radius*resolution, "ShapeContext");

      dbrec3d_batch.clear();
      dbrec3d_batch.reset_stdout();
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
  
  parser = OptionParser()
  parser.add_option("-s", "--site", action="store", type="int", dest="site", help="site number");
  parser.add_option("-r", "--radius", action="store", type="int", dest="radius", help="radius (multiple of resolution)");
  parser.add_option("-p", "--percent", action="store", type="int", dest="percentile", help="radius (multiple of resolution)");
  (opts, args) = parser.parse_args()
 
  #Begin multiprocessing
  job_list=[];
  #start_time = time.time();
  

  #define some feature parameters
  feature_type="ShapeContext";
  site= opts.site;
  radius = opts.radius;
  percentile = opts.percentile;
  num_cores = 8;
  

  #path to where all scenes are
  scenes_root_path="/data/helicopter_providence_3_12"
  experiments_root="/Users/isa/Experiments/shape_features_bmvc12"
  site_dir = scenes_root_path + "/site_" + str(site)  
  obj_dir = site_dir + "/objects_with_aux"
  
  if not os.path.exists(obj_dir + "/"):
    print "Error: Objects' DIR not found! ", obj_dir
    sys.exit(-1)
    
      
  #figure out the resolution from the scene _info.xml
  resolution = parse_scene_resolution(site_dir + "/scene_info.xml");  

  categories = glob.glob(obj_dir + "/*" + str(percentile));
      
        
  for cat in categories:
    
    if not os.path.isdir(cat):
      continue;
      
    objs = glob.glob(cat + "/*.ply");
    
    features_dir = experiments_root + "/site_" + str(site) + "/" + feature_type + "_" + str(radius) + "/" +os.path.basename(cat);
    
    if not os.path.exists(features_dir + "/"):
      print features_dir + "/"
      os.makedirs(features_dir + "/");
    
    for file_in in objs:
        #features get written to a .txt file for now -- PCL reader/writter doesn't handle variable length descriptos
        file_out= features_dir + "/" + os.path.basename(file_in);
        file_out = file_out[:-len(".ply")]   
        file_out = file_out  + ".txt";
        if True :
          print "Processing: "
          print file_in
          print "Saving to:"
          print file_out 

        #Enqueue jobs
        current_job = pcl_job(file_in, file_out, radius*resolution);
        job_list.append(current_job);
    
  execute_pcl_jobs(job_list, min(num_cores, len(job_list)));
  
  


