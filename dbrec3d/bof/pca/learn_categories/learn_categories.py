#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14, 2011

@author:Isabel Restrepo

A script quantize keypoints for categories
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

class bof_job():
    def __init__(self, bof_dir, codebook , scene_id, path_out):
        self.bof_dir = bof_dir;
        self.codebook = codebook;
        self.scene_id = scene_id;
        self.path_out = path_out;
        
   
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
#    results = []
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

            dbrec3d_batch.init_process("bofLearnCategoriesProcess");
            dbrec3d_batch.set_input_from_db(0, job.codebook);
            dbrec3d_batch.set_input_int(1, job.scene_id);
            dbrec3d_batch.set_input_string(2, job.bof_dir);
            dbrec3d_batch.set_input_string(3, job.path_out);
            dbrec3d_batch.run_process();
            
            dbrec3d_batch.clear();
            dbrec3d_batch.reset_stdout();
            print ("Runing time for worker:", self.name)
            print(time.time() - start_time);
            #output exit code in this case
            #important: having a result queue makes the execute_jobs wait for all jobs in the queue before exiting
            #self.result_queue.put(0);
            
                   
        
def parse_bof_info(bof_info_file):
    
    print 'Parsing: ' + bof_info_file
    
    #parse xml file
    bof_tree = ElementTree();
    bof_tree.parse(bof_info_file);
    
    #find scene paths
    scenes_elm = bof_tree.getroot().findall('scene');
    
    if scenes_elm is None:
      print "Invalid bof info file: No scenes element"
      sys.exit(-1);
    
    return len(scenes_elm);
        
#*******************The Main Algorithm ************************#
if __name__=="__main__":
  dbrec3d_batch.register_processes();
  dbrec3d_batch.register_datatypes();


  #Parse inputs
  parser = optparse.OptionParser(description='bof Statistics Pass 0');

  parser.add_option('--bof_dir', action="store", dest="bof_dir");
  parser.add_option('--k_means_dir', action="store", dest="k_means_dir");
  parser.add_option('--class_histograms_dir', action="store", dest="class_histograms_dir");
  parser.add_option('--num_cores', action="store", dest="num_cores", type="int", default=4);
  
  options, args = parser.parse_args()

  bof_dir = options.bof_dir;
  k_means_dir = options.k_means_dir;
  class_histograms_dir = options.class_histograms_dir;
  num_cores = options.num_cores;


  if not os.path.isdir(bof_dir +"/"):
    print "Invalid bof Dir"
    sys.exit(-1);
    
  if not os.path.isdir(k_means_dir +"/"):
    print "Invalid k-means Dir"
    sys.exit(-1)
  
  if not os.path.isdir(class_histograms_dir +"/"):
    os.mkdir(class_histograms_dir +"/")
 
  #parse the number of scenes
  bof_info_file = bof_dir + "/bof_info.xml";
  nscenes = parse_bof_info(bof_info_file);
  print "Number of Scenes:"
  print nscenes
  
  #Begin multiprocessing
  job_list=[];
  start_time = time.time();

  #initial satrting point means
  codebook_file = k_means_dir + "/lowest_sse_means.txt"
  dbrec3d_batch.init_process("bofInitCodebookProcess");
  dbrec3d_batch.set_input_string(0,codebook_file);
  dbrec3d_batch.run_process();
  (id, type) = dbrec3d_batch.commit_output(0);
  codebook= dbvalue(id, type);
  

  #Enqueue jobs
  for scene_id in range (0, nscenes):
      histogram_path = class_histograms_dir + "/scene_" + str(scene_id);
      if not os.path.isdir(histogram_path +"/"):
         os.mkdir(histogram_path +"/")
         
      current_job = bof_job(bof_dir, codebook , scene_id, histogram_path);
      job_list.append(current_job);
                                
  execute_bof_jobs(job_list, num_cores);
  
    