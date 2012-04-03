#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14, 2011

@author:Isabel Restrepo

Computes sample data mean and scatter. Each block is processed in a separate thread.
"""
import os;
import bvpl_octree_batch
import multiprocessing
import Queue 
import time
import random
import optparse
import sys
from numpy import log, ceil
import glob

#time.sleep(30);

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string
           
class pca_pairwise_job():
    def __init__(self, stats_file1, stats_file2, stats_file_out):
        self.stats_file1 = stats_file1;
        self.stats_file2 = stats_file2;     
        self.stats_file_out = stats_file_out;
        
def execute_pca_pairwise_jobs(jobs, num_procs=4):
    work_queue=multiprocessing.Queue();
    result_queue=multiprocessing.Queue();
    for job in jobs:
        work_queue.put(job)
    
    for i in range(num_procs):
        worker= pca_pairwise_worker(work_queue,result_queue)
        worker.start();
        print("worker with name ",worker.name," started!")
        
    # collect the results off the queue
    #important: having a result queue makes the execute_jobs wait for all jobs in the queue before exiting
    results = []
    while len(results) < len(jobs):
        result = result_queue.get()
        results.append(result)
 
    return results
        
        
class pca_pairwise_worker(multiprocessing.Process):
 
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
            
            bvpl_octree_batch.init_process("bvplCombinePairwiseStatisticsProcess");
            bvpl_octree_batch.set_input_string(0,job.stats_file1);
            bvpl_octree_batch.set_input_string(1,job.stats_file2);
            bvpl_octree_batch.set_input_string(2,job.stats_file_out);
            bvpl_octree_batch.run_process();
            
 
            print ("Runing time for worker:", self.name)
            print(time.time() - start_time);
            
            #output exit code in this case
            #important: having a result queue makes the execute_jobs wait for all jobs in the queue before exiting
            self.result_queue.put(0);



    
    
    
            
        
#*******************The Main Algorithm ************************#
if __name__=="__main__":
  bvpl_octree_batch.register_processes();
  bvpl_octree_batch.register_datatypes();

  #Parse inputs
  parser = optparse.OptionParser(description='Combine Pairwise Statistics');

  parser.add_option('--pca_dir', action="store", dest="pca_dir");
  parser.add_option('--num_cores', action="store", dest="num_cores", type="int", default=4);
  
  options, args = parser.parse_args();

  pca_dir = options.pca_dir;
  num_cores = options.num_cores;

  temp_results_dir = pca_dir + "/temp";
  pca_info_file = pca_dir + "/pca_global_info.xml";

  if not os.path.isdir(pca_dir +"/"):
    print "Invalid PCA Dir"
    sys.exit(-1);
    
  if not os.path.isdir(temp_results_dir +"/"):
    print "Invalid temp Dir"
    sys.exit(-1);
  
  
  #Begin multiprocessing
  start_time = time.time();

  prev_pass_files = glob.glob1(temp_results_dir, 'stats_pass_0*')
  nfiles_prev_pass = len(prev_pass_files);
  
  #Number of leyers in the binary (pairing) tree
  nlevels = int(ceil(log(nfiles_prev_pass)/log(2)))
  
  
  print (" Number of levels to process: " + str(nlevels))
     
  for level in range(0,nlevels):
       #reset job list
      job_list = []; 
      nfiles_this_pass = 0;
      print ("Number of files at current level: " + str(level) + ", is: " + str(nfiles_prev_pass))
      for file_idx  in range(0, nfiles_prev_pass, 2):
          
          stats_file1 = temp_results_dir + '/' + prev_pass_files[file_idx];
          if(file_idx==nfiles_prev_pass-1):
              stats_file2 = "na";
          else:
              stats_file2 = temp_results_dir + '/' + prev_pass_files[file_idx+1];

          stats_file_out = temp_results_dir + "/stats_pass_" + str(level+1)+ "_" + str(nfiles_this_pass) + ".txt";
          
          current_job = pca_pairwise_job(stats_file1, stats_file2, stats_file_out);
          job_list.append(current_job);
          nfiles_this_pass = nfiles_this_pass +1;
          

      print ("Start Executing ")

      results2=execute_pca_pairwise_jobs(job_list, num_cores);
      # dump results
      print results2;
      print ("Pass " + str(level+1) + " done")  
      this_pass_name = 'stats_pass_' + str(level+1) + '*';
      print('Looking for: ' + this_pass_name);
      prev_pass_files = glob.glob1(temp_results_dir, this_pass_name)
      nfiles_prev_pass = len(prev_pass_files);
      

  print ("Total running time: ");
  print(time.time() - start_time);
    