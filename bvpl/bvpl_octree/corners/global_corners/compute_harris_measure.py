#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14, 2011

@author:Isabel Restrepo

Threshold taylor coefficients. Each block is processed in a separate thread.
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

class taylor_project_job():
    def __init__(self, global_taylor, global_corners, scene_id, block_i, block_j, block_k):
        self.global_taylor = global_taylor;
        self.global_corners = global_corners;
        self.scene_id = scene_id;     
        self.block_i = block_i;
        self.block_j = block_j;
        self.block_k = block_k;        
   
def execute_taylor_jobs(jobs, num_procs=4):
    work_queue=multiprocessing.Queue();
    result_queue=multiprocessing.Queue();
    for job in jobs:
        work_queue.put(job)
    
    for i in range(num_procs):
        worker= taylor_worker(work_queue,result_queue)
        worker.start();
        print("worker with name ",worker.name," started!")
        
       
        
        
class taylor_worker(multiprocessing.Process):
 
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
            
            bvpl_octree_batch.init_process("bvplComputeHarrisMeasureProcess");
            bvpl_octree_batch.set_input_from_db(0,job.global_taylor);
            bvpl_octree_batch.set_input_from_db(1,job.global_corners);
            bvpl_octree_batch.set_input_int(2, job.scene_id);
            bvpl_octree_batch.set_input_int(3, job.block_i);
            bvpl_octree_batch.set_input_int(4, job.block_j);
            bvpl_octree_batch.set_input_int(5, job.block_k);
            bvpl_octree_batch.run_process();
            
            bvpl_octree_batch.clear();
 
            print ("Runing time for worker:", self.name)
            print(time.time() - start_time);

            
                   
        
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



def parse_taylor_info(taylor_info_file, scene_blocks):
    
    print 'Parsing: ' + taylor_info_file
    
    #parse xml file
    taylor_tree = ElementTree();
    taylor_tree.parse(taylor_info_file);
    
 
    
    #find scene paths
    scenes_elm = taylor_tree.getroot().findall('scene');
    
    if scenes_elm is None:
      print "Invalid taylor info file: No scenes element"
      sys.exit(-1);
    
    print ("Number of scenes: " + str(len(scenes_elm)));
    
    for s in range(0, len(scenes_elm)):
        scene_name = scenes_elm[s].get("path")
        
        if scene_name is None:
            print "Invalid taylor info file: Error parsing scenes"
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
  parser = optparse.OptionParser(description='taylor Statistics Pass 0');

  parser.add_option('--taylor_dir', action="store", dest="taylor_dir");
  parser.add_option('--corners_dir', action="store", dest="corners_dir");
  parser.add_option('--num_cores', action="store", dest="num_cores", type="int", default=4);
  
  options, args = parser.parse_args()

  taylor_dir = options.taylor_dir;
  corners_dir = options.corners_dir;
  num_cores = options.num_cores;

  #ideally inputs should be parsed from the taylor_global_info.xml file
  taylor_info_file = taylor_dir + "/taylor_global_info.xml";

  if not os.path.isdir(taylor_dir +"/"):
    print "Invalid taylor Dir"
    sys.exit(-1);
    
  if not os.path.isdir(corners_dir +"/"):
    print "Invalid corners_dir:"
    print corners_dir
    sys.exit(-1);
    
  
  #a list to keep the dimension (#of blocks) of each scene
  scene_blocks =[];
  
  parse_taylor_info(taylor_info_file, scene_blocks);
  
  print "Scene Blocks:"
  print scene_blocks  
  
  #Begin multiprocessing
  job_list=[];
  start_time = time.time();


  #load global_taylor and global_corners
  bvpl_octree_batch.init_process("bvplLoadGlobalTaylorProcess");
  bvpl_octree_batch.set_input_string(0,taylor_dir);
  bvpl_octree_batch.run_process();
  (id, type) = bvpl_octree_batch.commit_output(0);
  global_taylor = dbvalue(id, type);
  
  bvpl_octree_batch.init_process("bvplLoadGlobalCornersProcess");
  bvpl_octree_batch.set_input_string(0,corners_dir);
  bvpl_octree_batch.run_process();
  (id, type) = bvpl_octree_batch.commit_output(0);
  global_corners = dbvalue(id, type);


  #Enqueue jobs
  for s_idx in range (0, len(scene_blocks)):
    nblocks = scene_blocks[s_idx];
    for block_i in range (0, nblocks[1]):
        for block_j in range (0, nblocks[2]):
            for block_k in range (0, nblocks[3]):
                current_job = taylor_project_job(global_taylor, global_corners, s_idx, block_i, block_j, block_k);
                job_list.append(current_job);
                              
  execute_taylor_jobs(job_list, num_cores);
  #print results;
  print ("Pass 0 done")

  print ("Total running time: ");
  print(time.time() - start_time);
  