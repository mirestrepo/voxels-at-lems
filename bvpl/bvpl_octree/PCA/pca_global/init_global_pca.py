#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon March 24, 2011

@author:Isabel Restrepo

Script used to initiallize auxiliary scenes and information
All it does is write out necessay scene.xml files and compute finest cell lenghts.
"""
import os;
import bvpl_octree_batch;
import time
import random
import optparse
import sys
import multiprocessing
import Queue 
from xml.etree.ElementTree import ElementTree


class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string
    
     
class pca_job():
    def __init__(self, pca_dir, scene_id):
        self.pca_dir = pca_dir;
        self.scene_id = scene_id;     
        
   
def execute_pca_jobs(jobs, num_procs=4):
    work_queue=multiprocessing.Queue();
    result_queue=multiprocessing.Queue();
    for job in jobs:
        work_queue.put(job)
    
    for i in range(num_procs):
        worker= pca_worker(work_queue,result_queue)
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
              
        
class pca_worker(multiprocessing.Process):
 
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
            
            bvpl_octree_batch.init_process("bvplInitGlobalPCAProcess");
            bvpl_octree_batch.set_input_string(0,job.pca_dir);
            bvpl_octree_batch.set_input_unsigned(1, job.scene_id);
            bvpl_octree_batch.run_process();
            
            bvpl_octree_batch.clear();

 
            print ("Runing time for worker:", self.name)
            print(time.time() - start_time);
            
def parse_pca_info(pca_info_file):
    
    print 'Parsing: ' + pca_info_file
    
    #parse xml file
    pca_tree = ElementTree();
    pca_tree.parse(pca_info_file);
    
    #find number of scenes
    prop_elm = pca_tree.getroot().find('properties');
    
    if prop_elm is None:
      print "Invalid pca info file: No properties"
      sys.exit(-1);
      
    nscenes = prop_elm.get('nscenes')
    if nscenes is None:
      print "Invalid pca info file: No nscenes"
      sys.exit(-1);
      
    return int(nscenes);
         
#*******************The Main Algorithm ************************#
if __name__=="__main__":
  bvpl_octree_batch.register_processes();
  bvpl_octree_batch.register_datatypes();

  #Parse inputs
  parser = optparse.OptionParser(description='Init PCA');

  parser.add_option('--pca_dir', action="store", dest="pca_dir");
  parser.add_option('--num_cores', action="store", dest="num_cores", type="int", default=4);

  
  options, args = parser.parse_args();

  pca_dir = options.pca_dir;
  num_cores = options.num_cores;

  if not os.path.isdir(pca_dir +"/"):
    print "Invalid PCA Dir"
    sys.exit(-1);
  
  #ideally inputs should be parsed from the pca_global_info.xml file
  pca_info_file = pca_dir + "/pca_global_info.xml";

  nscenes=parse_pca_info(pca_info_file);
  print ("Number of scenes: " + str(nscenes));
   
  #Begin multiprocessing
  job_list=[];
  
  #Enqueue jobs
  for s_idx in range (0,nscenes):
      current_job = pca_job(pca_dir, s_idx);
      job_list.append(current_job);
      
  execute_pca_jobs(job_list, num_cores);

