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
from xml.etree.ElementTree import ElementTree

#time.sleep(30);

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

class pca_project_job():
    def __init__(self, global_pca, scene_id, block_i, block_j, block_k):
        self.global_pca = global_pca;
        self.scene_id = scene_id;     
        self.block_i = block_i;
        self.block_j = block_j;
        self.block_k = block_k;
        
   
def execute_pca_jobs(jobs, num_procs=4):
    work_queue=multiprocessing.Queue();
    result_queue=multiprocessing.Queue();
    for job in jobs:
        work_queue.put(job)
    
    for i in range(num_procs):
        worker= pca_project_worker(work_queue,result_queue)
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
        
        
        
class pca_project_worker(multiprocessing.Process):
 
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
            
            bvpl_octree_batch.init_process("bvplPCAProjectProcess");
            bvpl_octree_batch.set_input_from_db(0,job.global_pca);
            bvpl_octree_batch.set_input_int(1, job.scene_id);
            bvpl_octree_batch.set_input_int(2, job.block_i);
            bvpl_octree_batch.set_input_int(3, job.block_j);
            bvpl_octree_batch.set_input_int(4, job.block_k);
            bvpl_octree_batch.run_process();
            
            bvpl_octree_batch.clear();
 
            print ("Runing time for worker:", self.name)
            print(time.time() - start_time);
            #output exit code in this case
            #important: having a result queue makes the execute_jobs wait for all jobs in the queue before exiting
            #self.result_queue.put(0);
            
                   
        
def parse_scene(scene_file, blocks):
    #parse xml file
    tree = ElementTree();
    tree.parse(scene_file);
    
    #find number of scenes
    blocks_elm = tree.getroot().find('blocks');
    
    if blocks_elm is None:
      print "Error parsing boxm scene: No blocks_elm"
      sys.exit(-1);
      
    x = blocks_elm.get('x_dimension');
    y = blocks_elm.get('y_dimension');
    z = blocks_elm.get('z_dimension');
    
    if x is None or y is None or z is None:
      print "Error parsing boxm scene: Incorrect dimensions"
      sys.exit(-1);
      
    blocks.append(int(x));
    blocks.append(int(y));
    blocks.append(int(z));



def parse_pca_info(pca_info_file, scene_blocks):
    
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
      
    print ("Number of scenes: " + str(nscenes));
    
    #find scene paths
    scenes_elm = pca_tree.getroot().findall('scene');
    
    if scenes_elm is None:
      print "Invalid pca info file: No scenes element"
      sys.exit(-1);
    
    for s in range(0, len(scenes_elm)):
    
        scene_name = scenes_elm[s].get("path")
        
        if scene_name is None:
            print "Invalid pca info file: Error parsing scenes"
            sys.exit(-1);
        
        blocks = []; 
        blocks.append(s);       
        parse_scene(scene_name, blocks);
        scene_blocks.append(blocks);
        
        
#*******************The Main Algorithm ************************#
if __name__=="__main__":
  bvpl_octree_batch.register_processes();
  bvpl_octree_batch.register_datatypes();


  #Parse inputs
  parser = optparse.OptionParser(description='PCA Statistics Pass 0');

  parser.add_option('--pca_dir', action="store", dest="pca_dir");
  parser.add_option('--num_cores', action="store", dest="num_cores", type="int", default=4);
  
  options, args = parser.parse_args()

  pca_dir = options.pca_dir;
  num_cores = options.num_cores;

  #ideally inputs should be parsed from the pca_global_info.xml file
  pca_info_file = pca_dir + "/pca_global_info.xml";

  if not os.path.isdir(pca_dir +"/"):
    print "Invalid PCA Dir"
    sys.exit(-1);
    
  
  #a list to keep the dimension (#of blocks) of each scene
  scene_blocks =[];
  
  parse_pca_info(pca_info_file, scene_blocks);
  
  print "Scene Blocks:"
  print scene_blocks

  
  #Begin multiprocessing
  job_list=[];
  start_time = time.time();

  bvpl_octree_batch.init_process("bvplLoadGlobalPCA125Process");
  bvpl_octree_batch.set_input_string(0,pca_dir);
  bvpl_octree_batch.run_process();
  (id, type) = bvpl_octree_batch.commit_output(0);
  global_pca = dbvalue(id, type);
  
  #Enqueue jobs
  i = 0;
  for s_idx in range (0, len(scene_blocks)):
      nblocks = scene_blocks[s_idx];
      for block_i in range (0, nblocks[1]):
          for block_j in range (0, nblocks[2]):
              for block_k in range (0, nblocks[3]):
                  current_job = pca_project_job(global_pca, s_idx, block_i, block_j, block_k);
                  job_list.append(current_job);
                  i= i+1;          
                              
  execute_pca_jobs(job_list, num_cores);

    