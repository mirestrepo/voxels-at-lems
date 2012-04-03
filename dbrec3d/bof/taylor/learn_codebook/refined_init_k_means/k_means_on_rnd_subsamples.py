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
from math import log, ceil
from xml.etree.ElementTree import ElementTree

#time.sleep(30);

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

class bof_job():
    def __init__(self, bof_path, starting_means_path, fraction, max_it, file_out):
        self.bof_path = bof_path;
        self.starting_means_path = starting_means_path;
        self.fraction = fraction;
        self.max_it = max_it;
        self.file_out = file_out;
        
   
def execute_bof_jobs(jobs, num_procs=4):
    work_queue=multiprocessing.Queue();
    result_queue=multiprocessing.Queue();
    for job in jobs:
        work_queue.put(job)
    
    for i in range(num_procs):
        worker= bof_worker(work_queue,result_queue)
        worker.start();
        print("worker with name ",worker.name," started!")
        time.sleep(1);   #This is needed because when random sampling is done the current time is taken as the seed
                            #if all processes start at the same time they all have the same rnd sequence
        
        
        
class bof_worker(multiprocessing.Process):
 
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
            dbrec3d_batch.init_process("bofKMeansSubsampleProcess");
            dbrec3d_batch.set_input_string(0, job.bof_path);
            dbrec3d_batch.set_input_string(1, job.starting_means_path);
            dbrec3d_batch.set_input_double(2, job.fraction);
            dbrec3d_batch.set_input_unsigned(3, job.max_it);
            dbrec3d_batch.set_input_string(4, job.file_out);
            dbrec3d_batch.run_process();
            
            dbrec3d_batch.clear();
            dbrec3d_batch.reset_stdout();
 
            print ("Runing time for worker:", self.name)
            print(time.time() - start_time);
          
        
#*******************The Main Algorithm ************************#
if __name__=="__main__":
  dbrec3d_batch.register_processes();
  dbrec3d_batch.register_datatypes();


  #Parse inputs
  parser = optparse.OptionParser(description='bof Statistics Pass 0');

  parser.add_option('--bof_dir', action="store", dest="bof_dir");
  parser.add_option('--init_k_means_dir', action="store", dest="init_k_means_dir");
  parser.add_option('--fraction_subsamples', action="store", dest="fraction_subsamples", type="float", default =0.001)
  parser.add_option('--num_subsamples', action="store", dest="num_subsamples", type="int", default=10);
  parser.add_option('--num_cores', action="store", dest="num_cores", type="int", default=4);
  parser.add_option('--max_it', action="store", dest="max_it", type="int", default=100);

  
  options, args = parser.parse_args()

  bof_dir = options.bof_dir;
  init_k_means_dir = options.init_k_means_dir;
  fraction_subsamples = options.fraction_subsamples;
  num_subsamples = options.num_subsamples;
  num_cores = options.num_cores;
  max_it = options.max_it;

  if not os.path.isdir(bof_dir +"/"):
    print "Invalid bof Dir"
    sys.exit(-1);
    
  if not os.path.isdir(init_k_means_dir +"/"):
    print "Invalid temp Dir"
    sys.exit(-1)
  
  
  #Begin multiprocessing
  job_list=[];
  start_time = time.time();

  #random initial satrting point means
  sp_file = init_k_means_dir + "/sp_means.txt"
  
  CM_path = init_k_means_dir + "/CM";  
  if not os.path.isdir(CM_path +"/"):
    os.mkdir(CM_path +"/");  


  #Enqueue jobs
  for j in range (0, num_subsamples):
      cm_file = CM_path + "/CM_" + str(j)+ ".txt";
      current_job = bof_job(bof_dir, sp_file , fraction_subsamples, max_it, cm_file);
      job_list.append(current_job);
                                
  execute_bof_jobs(job_list, num_cores);
    