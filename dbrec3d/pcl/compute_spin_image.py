#!/bin/python

#  comput_fpfh.py
#  voxels-at-lems
#
#  Created by Maria Isabel Restrepo on 11/8/11.
#  Copyright (c) 2011 Brown University. All rights reserved.



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

class pcl_job():
  def __init__(self, pcl_dir, object_id, radius, width, sup_angle, num_neighbors, radial, angular):
    self.pcl_dir = pcl_dir;
    self.radius  = radius;
    self.object_id = object_id;
    self.radius = radius;
    self.width = width;
    self.sup_angle = sup_angle;
    self.num_neighbors = num_neighbors;
    self.radial = radial;
    self.angular = angular;
    
    

def execute_pcl_jobs(jobs, num_procs=4):
  work_queue=multiprocessing.Queue();
  result_queue=multiprocessing.Queue();
  for job in jobs:
    work_queue.put(job)
  
  for i in range(num_procs):
    worker= pcl_worker(work_queue,result_queue)
    worker.start();
    print("worker with name ",worker.name," started!")

# collect the results off the queue
#important: having a result queue makes the execute_jobs wait for all jobs in the queue before exiting
#    results = []
#    while len(results) < len(jobs):
#        result = result_queue.get()
#        results.append(result)
# 
#    return results



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
      #dbrec3d_batch.set_stdout('logs/log_' + str(os.getpid())+ ".txt");
      
#      file_in = str(job.pcl_dir) + "/object_" + str(job.object_id) + ".pcd"; 
#      file_out = str(job.pcl_dir) + "/fpfh_object_" + str(job.object_id) + ".pcd";
    
#      file_in = str(job.pcl_dir) + "/boxm_scili.pcd"; 
#      file_out = str(job.pcl_dir) + "/fpfh_boxm_scili.pcd"; 
#      file_in="/Projects/pcl_dev/pcl/trunk/test/bun0.pcd"
      file_in = str(job.pcl_dir) + "/mesh_0.ply"; 
      file_out = str(job.pcl_dir) + "/spin_mesh_0.pcd"; 

      dbrec3d_batch.init_process("pcl_compute_spin_image_process");
      dbrec3d_batch.set_input_string(0, file_in);
      dbrec3d_batch.set_input_double(1, job.radius);
      dbrec3d_batch.set_input_int(2, job.width);
      dbrec3d_batch.set_input_double(3, job.sup_angle);
      dbrec3d_batch.set_input_int(4, job.num_neighbors);
      dbrec3d_batch.set_input_bool(5, job.radial);
      dbrec3d_batch.set_input_bool(6, job.angular);
      dbrec3d_batch.set_input_string(7, file_out);
      dbrec3d_batch.run_process();
      
      dbrec3d_batch.clear();
      #dbrec3d_batch.reset_stdout();
      print ("Runing time for worker:", self.name)
      print(time.time() - start_time);

      #output exit code in this case
      #important: having a result queue makes the execute_jobs wait for all jobs in the queue before exiting
      #self.result_queue.put(0);


#*******************The Main Algorithm ************************#
if __name__=="__main__":
  dbrec3d_batch.register_processes();
  dbrec3d_batch.register_datatypes();
 
  #Begin multiprocessing
  job_list=[];
  #start_time = time.time();
  
  #local variables
  #cell_length = 1;
  #radius = 7.5 * cell_length;
  
  resolution = 1;
  radius = 30;
  width = 16;
  sup_angle = 0.5;
  num_neighbors =8;
  radial = 0;
  angular = 0;
  

  
  #pcl_dir = "/Users/isa/Experiments/pcl/tests/site12_objects";
  pcl_dir = "/Users/isa/Experiments/pcl/site12/buildings"
  nobjects = 1;
  num_cores = 1;
  
  #Enqueue jobs
  #for object_id in range (0, nobjects):
  current_job = pcl_job(pcl_dir, 0, radius, width, sup_angle, num_neighbors, radial, angular);
  job_list.append(current_job);
  
  execute_pcl_jobs(job_list, num_cores);


