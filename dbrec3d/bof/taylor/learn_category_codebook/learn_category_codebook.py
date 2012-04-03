#!/opt/local/Library/Frameworks/Python.framework/Versions/2.6/bin/python
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
from math import log, ceil
from xml.etree.ElementTree import ElementTree


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
            # print ("Runing time for worker:", self.name)
            # print(time.time() - start_time);
           
                   
        
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
#  parser = optparse.OptionParser(description='bof Statistics Pass 0');
#
#  parser.add_option('--bof_dir', action="store", dest="bof_dir");
#  parser.add_option('--k_means_dir', action="store", dest="k_means_dir");
#  parser.add_option('--num_means', action="store", dest="num_means", type="int", default =50)
#  parser.add_option('--num_cores', action="store", dest="num_cores", type="int", default=4);
#  parser.add_option('--fraction', action="store", dest="fraction", type="float", default =0.01)
#  parser.add_option('--J', action="store", dest="J", type="int", default=10);
#  parser.add_option('--max_it', action="store", dest="max_it", type="int", default=100);
#
#
#  options, args = parser.parse_args()
#
#  bof_dir = options.bof_dir;
#  k_means_dir = options.k_means_dir;
#  num_means = options.num_means;
#  num_cores = options.num_cores;
#  max_it = options.max_it;
#  fraction = options.fraction;
#  J = options.J;

  main_dir="/Users/isa/Experiments/BOF/helicopter_providence/L1_taylor";
  num_means=20;
  bof_dir=main_dir + "/bof_category_specific";
  k_means_dir=bof_dir + "/k_means_" +str(num_means)
  fraction=0.01;
  J=10;  #number of subsamples
  max_it=1000; #max number of iteration for k-means

  if not os.path.isdir(bof_dir +"/"):
      print "Invalid bof Dir"
      sys.exit(-1);

  if not os.path.isdir(k_means_dir +"/"):
      print "Invalid k-means Dir"
      os.mkdir(k_means_dir + "/" );

  #parse the number of scenes
  bof_info_file = bof_dir + "/bof_info.xml";
  nscenes = parse_bof_info(bof_info_file);
  print "Number of Scenes:"
  print nscenes

  #load category info 
  dbrec3d_batch.init_process("bofLoadCategoryInfoProces");
  dbrec3d_batch.set_input_string(0, bof_dir);
  dbrec3d_batch.run_process();
  (id, type) = dbrec3d_batch.commit_output(0);
  categories= dbvalue(id, type);

  #learn codebook for a particular class
  class_id = 0;
  class_mean_dir = k_means_dir + "/class" + str(class_id);
  if not os.path.isdir(class_mean_dir +"/"):
      os.mkdir(class_mean_dir + "/" );

    
  dbrec3d_batch.init_process("bofLearnCategoryCodebookProcess");
  dbrec3d_batch.set_input_from_db(0,categories);
  dbrec3d_batch.set_input_unsigned(1, class_id);
  dbrec3d_batch.set_input_unsigned(2, num_means);
  dbrec3d_batch.set_input_double(3, fraction);
  dbrec3d_batch.set_input_unsigned(4, J);
  dbrec3d_batch.set_input_unsigned(5, max_it);
  dbrec3d_batch.set_input_string(6, class_mean_dir);
  dbrec3d_batch.run_process();

  
#  #Begin multiprocessing
#  job_list=[];
#  start_time = time.time();
#
#  #Enqueue jobs
#  for scene_id in range (0, nscenes):
#      histogram_path = class_histograms_dir + "/scene_" + str(scene_id);
#      if not os.path.isdir(histogram_path +"/"):
#         os.mkdir(histogram_path +"/")
#         
#      current_job = bof_job(bof_dir, codebook , scene_id, histogram_path);
#      job_list.append(current_job);
#                               
#  execute_bof_jobs(job_list, num_cores);

  
    