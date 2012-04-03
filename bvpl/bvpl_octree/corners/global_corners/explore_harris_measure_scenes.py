#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14, 2011

@author:Isabel Restrepo

Threshold corners coefficients. Each block is processed in a separate thread.
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
import numpy as np
import matplotlib.pyplot as plt

#time.sleep(30);

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string
    
def plot_histogram(full_path_file):
    f = open(full_path_file, 'r');

    lines=[];
    lines = f.readlines();

    x=[];
    line0=lines[0]; 
    this_line = line0.split(", ");
    for j in this_line:
        x.append(float(j));
            

    y=[];
    line1 = lines[1];
    this_line = line1.split(", ");
    for j in this_line:
        y.append(float(j));
  
 
    plt.figure();
    plt.bar(x,y, (x[len(x)-1] - x[0])/500);
    #plt.xlim([x[0],x[len(x)-1]]); 
    figure_file = full_path_file.split('.')[0]
    figure_file = figure_file + '.pdf';
    plt.savefig(figure_file, transparent=True);
    f.close();

class display_corners_job():
    def __init__(self, path_scene_in, path_scene_out):
        self.path_scene_in = path_scene_in;
        self.path_scene_out = path_scene_out;
       
class corners_job():
    def __init__(self, global_taylor, global_corners, scene_id):
        self.global_taylor = global_taylor;
        self.global_corners = global_corners;
        self.scene_id = scene_id;
        
def execute_corners_jobs(jobs, num_procs=4):
    work_queue=multiprocessing.Queue();
    result_queue=multiprocessing.Queue();
    for job in jobs:
        work_queue.put(job)
    
    for i in range(num_procs):
        worker= corners_worker(work_queue,result_queue)
        worker.start();
        print("worker with name ",worker.name," started!")
        
        
class corners_worker(multiprocessing.Process):
 
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
            
            bvpl_octree_batch.init_process("bvplCornerStatisticsProcess");
            bvpl_octree_batch.set_input_from_db(0,job.global_taylor);
            bvpl_octree_batch.set_input_from_db(1,job.global_corners);
            bvpl_octree_batch.set_input_int(2, job.scene_id);
            bvpl_octree_batch.run_process();
            
            bvpl_octree_batch.clear();
 
            print ("Runing time for worker:", self.name)
            print(time.time() - start_time);
    
        
class display_corners_worker(multiprocessing.Process):
 
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
            
            print("Creating a Scene");
            bvpl_octree_batch.init_process("boxmCreateSceneProcess");
            bvpl_octree_batch.set_input_string(0, job.path_scene_in);
            bvpl_octree_batch.run_process();
            (id, type) = bvpl_octree_batch.commit_output(0);
            scene= dbvalue(id, type);
             
            
            print("Save Scene");
            bvpl_octree_batch.init_process("boxmSaveSceneRawProcess");
            bvpl_octree_batch.set_input_from_db(0,scene);
            bvpl_octree_batch.set_input_string(1, job.path_scene_out);
            bvpl_octree_batch.set_input_unsigned(2,0);
            bvpl_octree_batch.set_input_unsigned(3,1);
            bvpl_octree_batch.run_process(); 
            
            plot_histogram(job.path_scene_out + "_hist_plot.txt");           
            
            bvpl_octree_batch.clear();
 
            print ("Runing time for worker:", self.name)
            print(time.time() - start_time);
            
                  
        
def parse_corners_info(corners_info_file, aux_dirs):
    
    print 'Parsing: ' + corners_info_file
    
    #parse xml file
    corners_tree = ElementTree();
    corners_tree.parse(corners_info_file);
    
 
    
    #find scene paths
    scenes_elm = corners_tree.getroot().findall('scene');
    
    if scenes_elm is None:
      print "Invalid corners info file: No scenes element"
      sys.exit(-1);
    
    print ("Number of scenes: " + str(len(scenes_elm)));
    
    for s in range(0, len(scenes_elm)):
        
        dir = scenes_elm[s].get("aux_dir")
        
        if dir is None:
            print "Invalid corners info file: Error parsing scenes"
            sys.exit(-1);
        
        print dir;
        aux_dirs.append(dir);
        
        
#*******************The Main Algorithm ************************#
if __name__=="__main__":
  bvpl_octree_batch.register_processes();
  bvpl_octree_batch.register_datatypes();


  #Parse inputs
  parser = optparse.OptionParser(description='corners Statistics Pass 0');

  parser.add_option('--taylor_dir', action="store", dest="taylor_dir");
  parser.add_option('--corners_dir', action="store", dest="corners_dir");
  parser.add_option('--num_cores', action="store", dest="num_cores", type="int", default=4);
  
  options, args = parser.parse_args()

  taylor_dir = options.taylor_dir;
  corners_dir = options.corners_dir;
  num_cores = options.num_cores;

  #ideally inputs should be parsed from the corners_global_info.xml file
  corners_info_file = corners_dir + "/global_corners_info.xml";

  if not os.path.isdir(taylor_dir +"/"):
    print "Invalid taylor_dir:"
    print taylor_dir
    sys.exit(-1);
    
  if not os.path.isdir(corners_dir +"/"):
    print "Invalid corners_dir:"
    print corners_dir
    sys.exit(-1);
    
  
  #a list to keep the dimension (#of blocks) of each scene
  aux_dirs =[];  
  parse_corners_info(corners_info_file, aux_dirs);
  
  print "Auxiliary Directories:"
  print aux_dirs;
  
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
#  for dir in aux_dirs:
#      path_scene_in = dir + "/harris_scene.xml";
#      drishti_dir = dir + "/drishti";
#      if not os.path.isdir(drishti_dir +"/"):
#        os.mkdir(drishti_dir +"/");
#      path_scene_out = drishti_dir + "/harris_scene";
#      current_job = display_corners_job(path_scene_in, path_scene_out);
#      job_list.append(current_job);
                              
# execute_display_corners_jobs(job_list, num_cores);
  for s_idx in range(0,len(aux_dirs)):
    job_list.append(corners_job(global_taylor, global_corners, s_idx));

  execute_corners_jobs(job_list, num_cores);
  
  #print results;
  print ("Pass 0 done")

  print ("Total running time: ");
  print(time.time() - start_time);
  