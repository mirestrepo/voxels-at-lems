# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13, 2011

@author:Isabel Restrepo

Computes sample data mean and scatter. 
"""
import os;
import dbrec3d_batch
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
    
     
class pca_stats_job():
    def __init__(self, categories, global_pca, scene_id, file_out):
        self.categories = categories;
        self.global_pca = global_pca;
        self.scene_id = scene_id;     
        self.file_out = file_out;
        
   
def execute_pca_jobs(jobs, num_procs=4):
    work_queue=multiprocessing.Queue();
    result_queue=multiprocessing.Queue();
    for job in jobs:
        work_queue.put(job)
    
    for i in range(num_procs):
        worker= pca_stats_worker(work_queue,result_queue)
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
              
        
class pca_stats_worker(multiprocessing.Process):
 
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

            dbrec3d_batch.init_process("bof_sample_statistics_process");
            dbrec3d_batch.set_input_from_db(0,job.categories);
            dbrec3d_batch.set_input_from_db(1,job.global_pca);
            dbrec3d_batch.set_input_unsigned(2, job.scene_id);
            dbrec3d_batch.set_input_string(3, job.file_out);
            dbrec3d_batch.run_process();
            
            dbrec3d_batch.clear();
            dbrec3d_batch.reset_stdout();

 
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
  dbrec3d_batch.register_processes();
  dbrec3d_batch.register_datatypes();

   #Parse inputs
  parser = optparse.OptionParser(description='Compute PCA sample statistics');

  parser.add_option('--bof_dir', action="store", dest="bof_dir");
  parser.add_option('--pca_dir', action="store", dest="pca_dir");
  parser.add_option('--num_cores', action="store", dest="num_cores", type="int", default=4);

  options, args = parser.parse_args()

  bof_dir = options.bof_dir;
  pca_dir = options.pca_dir;
  num_cores = options.num_cores;

  if not os.path.isdir(bof_dir +"/"):
    print "Invalid BOF Dir"
    sys.exit(-1);

  #ideally inputs should be parsed from the pca_global_info.xml file
  pca_info_file = pca_dir + "/pca_global_info.xml";
  temp_results_dir = pca_dir + "/temp";

  if not os.path.isdir(pca_dir +"/"):
    print "Invalid PCA Dir"
    sys.exit(-1);
    
  if not os.path.isdir(temp_results_dir +"/"):
    os.mkdir(temp_results_dir +"/");

  nscenes=parse_pca_info(pca_info_file);
  print ("Number of scenes: " + str(nscenes));
  

  #load category info 
  dbrec3d_batch.init_process("bofLoadCategoryInfoProces");
  dbrec3d_batch.set_input_string(0, bof_dir);
  dbrec3d_batch.set_input_string(1, "bof_info_train.xml")
  dbrec3d_batch.set_input_string(2, "bof_category_train_info.xml")
  dbrec3d_batch.run_process();
  (id, type) = dbrec3d_batch.commit_output(0);
  categories= dbvalue(id, type);
  
  
  dbrec3d_batch.init_process("bvplLoadGlobalPCA125Process");
  dbrec3d_batch.set_input_string(0,pca_dir);
  dbrec3d_batch.run_process();
  (id, type) = dbrec3d_batch.commit_output(0);
  global_pca = dbvalue(id, type);
  
  
  #Begin multiprocessing
  job_list=[];
  start_time = time.time();
  
  #Enqueue jobs
  i=0;
  for s_idx in range (0,nscenes):
      file_out = temp_results_dir + "/stats_pass_0_" + str(i) + ".txt";
      current_job = pca_stats_job(categories, global_pca, s_idx, file_out);
      job_list.append(current_job);
      i= i+1;
      
  print ("job_list" + str(len(job_list)));
  execute_pca_jobs(job_list, num_cores);
 
                             
                  
    