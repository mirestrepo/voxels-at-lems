#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14, 2011

@author:Isabel Restrepo

A script to run (fast) k-means independently for each block of all registered scenes
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
    def __init__(self, bof_path, starting_means_path, scene_id, block_i, block_j, block_k, max_it, file_out):
        self.bof_path = bof_path;
        self.starting_means_path = starting_means_path;
        self.scene_id = scene_id;
        self.block_i = block_i;
        self.block_j = block_j;
        self.block_k = block_k;
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
            dbrec3d_batch.init_process("bofKMeansTrainProcess");
            dbrec3d_batch.set_input_string(0, job.bof_path);
            dbrec3d_batch.set_input_string(1, job.starting_means_path);
            dbrec3d_batch.set_input_int(2, job.scene_id);
            dbrec3d_batch.set_input_int(3, job.block_i);
            dbrec3d_batch.set_input_int(4, job.block_j);
            dbrec3d_batch.set_input_int(5, job.block_k);
            dbrec3d_batch.set_input_unsigned(6, job.max_it);
            dbrec3d_batch.set_input_string(7, job.file_out);
            dbrec3d_batch.run_process();
            
            dbrec3d_batch.clear();
            dbrec3d_batch.reset_stdout();
 
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



def parse_bof_info(bof_info_file, scene_blocks):
    
    print 'Parsing: ' + bof_info_file
    
    #parse xml file
    bof_tree = ElementTree();
    bof_tree.parse(bof_info_file);
    
    #find scene paths
    scenes_elm = bof_tree.getroot().findall('scene');
    
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
  dbrec3d_batch.register_processes();
  dbrec3d_batch.register_datatypes();


  #Parse inputs
  parser = optparse.OptionParser(description='bof Statistics Pass 0');

  parser.add_option('--bof_dir', action="store", dest="bof_dir");
  parser.add_option('--k_means_dir', action="store", dest="k_means_dir");
  parser.add_option('--num_cores', action="store", dest="num_cores", type="int", default=4);
  parser.add_option('--max_it', action="store", dest="max_it", type="int", default=100);

  
  options, args = parser.parse_args()

  bof_dir = options.bof_dir;
  k_means_dir = options.k_means_dir;
  num_cores = options.num_cores;
  max_it = options.max_it;

  if not os.path.isdir(bof_dir +"/"):
    print "Invalid bof Dir"
    sys.exit(-1);
    
  if not os.path.isdir(k_means_dir +"/"):
    print "Invalid k-means Dir"
    sys.exit(-1)
  
  cm_dir = k_means_dir + "/CM"
  
  if not os.path.isdir(cm_dir +"/"):
    os.mkdir(cm_dir +"/")
  
   #a list to keep the dimension (#of blocks) of each scene
  bof_info_file = bof_dir + "/bof_info.xml";
  scene_blocks =[];
  parse_bof_info(bof_info_file, scene_blocks);
  print "Scene Blocks:"
  print scene_blocks


  
  #Begin multiprocessing
  job_list=[];
  start_time = time.time();
  saveout = sys.stdout   # save initial state of stdout

  #initial satrting point means
  sp_file = k_means_dir + "/sp_means.txt"

  #Enqueue jobs
  i=0;
  for scene_id in range (0, len(scene_blocks)):
        nblocks = scene_blocks[scene_id];
        for block_i in range (0, nblocks[1]):
            for block_j in range (0, nblocks[2]):
                for block_k in range (0, nblocks[3]):
                    cm_file = cm_dir + "/CM_" + str(scene_id) + "_" + str(block_i) + "_" + str(block_j) + "_" + str(block_k) + ".txt";
                    current_job = bof_job(bof_dir, sp_file , scene_id, block_i, block_j, block_k, max_it, cm_file);
                    job_list.append(current_job);
                    i=i+1
                                
  execute_bof_jobs(job_list, num_cores);
  
  sys.stdout = saveout

  print ("Pass 0 done")

  print ("Total running time: ");
  print(time.time() - start_time);
  
  sys.exit(i);
    