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
from numpy import log, ceil
from xml.etree.ElementTree import ElementTree
import glob

#time.sleep(30);

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

class bof_job():
    def __init__(self, cm_i_file, CM_set, max_it, fm_i_file):
        self.cm_i_file = cm_i_file;
        self.CM_set = CM_set;
        self.max_it = max_it;
        self.fm_i_file = fm_i_file;
        
   
def execute_bof_jobs(jobs, num_procs=4):
    work_queue=multiprocessing.Queue();
    result_queue=multiprocessing.Queue();
    for job in jobs:
        work_queue.put(job)
    
    for i in range(num_procs):
        worker= bof_worker(work_queue,result_queue)
        worker.start();
        print("worker with name ",worker.name," started!")
        
    # collect the results off the queue
    #important: having a result queue makes the execute_jobs wait for all jobs in the queue before exiting
    #results = []
#    while len(results) < len(jobs):
#        result = result_queue.get()
#        results.append(result)
# 
#    return results
        
        
        
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

            dbrec3d_batch.init_process("bofKMeansOnVectorProcess");
            dbrec3d_batch.set_input_string(0, job.cm_i_file);
            dbrec3d_batch.set_input_from_db(1, job.CM_set);
            dbrec3d_batch.set_input_unsigned(2, job.max_it);
            dbrec3d_batch.set_input_string(3, job.fm_i_file);
            dbrec3d_batch.run_process();
            
            dbrec3d_batch.clear();
            dbrec3d_batch.reset_stdout();
            print ("Runing time for worker:", self.name)
            print(time.time() - start_time);
            #output exit code in this case
            #important: having a result queue makes the execute_jobs wait for all jobs in the queue before exiting
            #self.result_queue.put(0);
            
                   
#*******************The Main Algorithm ************************#
if __name__=="__main__":
  dbrec3d_batch.register_processes();
  dbrec3d_batch.register_datatypes();


  #Parse inputs
  parser = optparse.OptionParser(description='bof Statistics Pass 0');

  parser.add_option('--k_means_dir', action="store", dest="k_means_dir");
  parser.add_option('--num_cores', action="store", dest="num_cores", type="int", default=4);
  parser.add_option('--max_it', action="store", dest="max_it", type="int", default=100);

  
  options, args = parser.parse_args()

  k_means_dir = options.k_means_dir;   #path where all CM_i means are saved and where the ouput FM_i will be written to
  num_cores = options.num_cores;
  max_it = options.max_it;

  if not os.path.isdir(k_means_dir +"/"):
    print "Invalid init_k_means Dir"
    sys.exit(-1);
    
 
  CM_path = k_means_dir + "/CM";  
  if not os.path.isdir(CM_path +"/"):
    print "Invalid CM Dir"
    sys.exit(-1);
    
  CM_files = glob.glob1(CM_path, 'CM*');
 
    
  FM_path = k_means_dir + "/FM";  
  if not os.path.isdir(FM_path +"/"):
    os.mkdir(FM_path +"/");   

  start_time = time.time();


  #Combine all CM_i means into one set CM to be passed for k-means
  mean_file_sfx = CM_path + "/CM_" ;
  dbrec3d_batch.init_process("bofCombineMeansProcess");
  dbrec3d_batch.set_input_string(0, mean_file_sfx);
  dbrec3d_batch.run_process();
  (id, type) = dbrec3d_batch.commit_output(0);
  CM_set= dbvalue(id, type);


  #Begin multiprocessing
  job_list=[];
  
  #Enqueue jobs
  for CM_file in CM_files:
      cm_file = CM_path + "/" + CM_file;
      fm_file = FM_path + "/FM" + CM_file.strip('CM');
      current_job = bof_job(cm_file, CM_set, max_it, fm_file);
      job_list.append(current_job);
                                
  execute_bof_jobs(job_list, num_cores);
    