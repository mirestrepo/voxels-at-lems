#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14, 2011

@author:Isabel Restrepo

A script to classify objects in testing scenes
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
    def __init__(self, bof_dir,p_xc, codebook , scene_id, top_p, path_out):
        self.bof_dir = bof_dir;
        self.codebook = codebook;
        self.p_xc = p_xc;
        self.scene_id = scene_id;
        self.path_out = path_out;
        self.top_p = top_p;
        
   
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

            dbrec3d_batch.init_process("bof_classify_salient_process");
            dbrec3d_batch.set_input_from_db(0, job.codebook);
            dbrec3d_batch.set_input_from_db(1, job.p_xc);
            dbrec3d_batch.set_input_int(2, job.scene_id);
            dbrec3d_batch.set_input_float(3, job.top_p);
            dbrec3d_batch.set_input_string(4, job.bof_dir);
            dbrec3d_batch.set_input_string(5, job.path_out);
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
  parser = optparse.OptionParser(description='bof Statistics Pass 0');

  parser.add_option('--bof_dir', action="store", dest="bof_dir");
  parser.add_option('--k_means_dir', action="store", dest="k_means_dir");
  parser.add_option('--num_cores', action="store", dest="num_cores", type="int", default=4);
  parser.add_option('--ncategories', action="store", dest="ncategories", type="int", default=0);
  parser.add_option('--class_histograms_dir', action="store", dest="class_histograms_dir");
  parser.add_option('--classification_dir', action="store", dest="classification_dir");
  parser.add_option('--thresh', action="store", dest="thresh", type="float", default =1)


  options, args = parser.parse_args()

  bof_dir = options.bof_dir;
  k_means_dir = options.k_means_dir;
  class_histograms_dir = options.class_histograms_dir;
  classification_dir = options.classification_dir;
  num_cores = options.num_cores;
  ncategories = options.ncategories;
  thresh = options.thresh;
  top_p=thresh/100;

  if not os.path.isdir(bof_dir +"/"):
      print "Invalid bof Dir"
      sys.exit(-1);

  if not os.path.isdir(k_means_dir +"/"):
      print "Invalid k-means Dir"
      sys.exit(-1)

  if not os.path.isdir(class_histograms_dir +"/"):
      print "Invalid class_histograms_dir"
      sys.exit(-1)

  if not os.path.isdir(classification_dir +"/"):
      os.mkdir(classification_dir + "/"); 

  #parse the number of scenes
  bof_info_file = bof_dir + "/bof_info_test.xml";
  nscenes = parse_bof_info(bof_info_file);
  print "Number of Scenes:"
  print nscenes

  #Begin multiprocessing
  job_list=[];
  start_time = time.time();

  #load codebook
  codebook_file = k_means_dir + "/lowest_sse_means.txt"
  dbrec3d_batch.init_process("bofInitCodebookProcess");
  dbrec3d_batch.set_input_string(0,codebook_file);
  dbrec3d_batch.run_process();
  (id, type) = dbrec3d_batch.commit_output(0);
  codebook= dbvalue(id, type);

  #load class/keypoints distributions
  dbrec3d_batch.init_process("bofLoadPXCProcess");
  dbrec3d_batch.set_input_from_db(0,codebook);
  dbrec3d_batch.set_input_string(1,class_histograms_dir);
  dbrec3d_batch.set_input_unsigned(2, ncategories);
  dbrec3d_batch.run_process();
  (id, type) = dbrec3d_batch.commit_output(0);
  p_xc= dbvalue(id, type);
    
  #Enqueue jobs
  for scene_id in range(0, nscenes):
      current_job = bof_job(bof_dir, p_xc, codebook , scene_id, top_p, classification_dir);
      job_list.append(current_job);
                                
  execute_bof_jobs(job_list, num_cores);