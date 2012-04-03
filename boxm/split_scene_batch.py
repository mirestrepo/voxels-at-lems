#!/usr/bin/python

import boxm_batch;
import multiprocessing
import Queue 
import time
import os;
import optparse;
from xml.etree.ElementTree import ElementTree

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

class boxm_job():
    def __init__(self,model_dir,model_name, grey_offset):
        self.model_dir=model_dir;
        self.model_name = model_name;
        self.grey_offset = grey_offset;
        
        
def execute_jobs(jobs, num_procs=5):
    work_queue=multiprocessing.Queue();
    result_queue=multiprocessing.Queue();
    for job in jobs:
        work_queue.put(job)
    
    for i in range(num_procs):
        worker= boxm_worker(work_queue,result_queue)
        worker.start();
        print("worker with name ",worker.name," started!")
        
        
    # collect the results off the queue
    #important: having a result queue makes the execute_jobs wait for all jobs in the queue before exiting
    results = []
    while len(results) < len(jobs):
        result = result_queue.get()
        results.append(result)
 
    return results
        
        
class boxm_worker(multiprocessing.Process):
 
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
            
            model_dir=job.model_dir;
            model_name =job.model_name;
            grey_offset = job.grey_offset;
            
            print("Model dir:")
            print model_dir
            print("Model Name:")
            print model_name
            
            
            print("Creating a Scene");
            boxm_batch.init_process("boxmCreateSceneProcess");
            boxm_batch.set_input_string(0,  model_dir + "/" + model_name + ".xml");
            boxm_batch.run_process();
            (scene_id, scene_type) = boxm_batch.commit_output(0);
            scene= dbvalue(scene_id, scene_type);
            
           
            print("Splitting the scene");
            boxm_batch.init_process("boxmSplitSceneProcess");
            boxm_batch.set_input_from_db(0, scene);
            boxm_batch.run_process();
            (scene_id, scene_type) = boxm_batch.commit_output(0);
            apm_scene = dbvalue(scene_id, scene_type);
            (scene_id, scene_type) = boxm_batch.commit_output(1);
            alpha_scene = dbvalue(scene_id, scene_type);
            
            print("Save Scene");
            boxm_batch.init_process("boxmSaveScene    RawProcess");
            boxm_batch.set_input_from_db(0,alpha_scene);
            boxm_batch.set_input_string(1,model_dir + "/drishti/alpha_scene");
            boxm_batch.set_input_unsigned(2,0);
            boxm_batch.set_input_unsigned(3,1);
            boxm_batch.run_process();
            
            #free memory
            boxm_batch.clear();
         
            print ("Runing time for worker:", self.name)
            print(time.time() - start_time);
            
            #output exit code in this case
            #important: having a result queue makes the execute_jobs wait for all jobs in the queue before exiting
            self.result_queue.put(0);
            
#function to parse and xml file containing the model directory and the xml_file_name (without the path)            
def parse_scenes_info(scenes_info_file, model_dirs, model_names):
    
    print 'Parsing: ' + scenes_info_file
    
    #parse xml file
    bof_tree = ElementTree();
    bof_tree.parse(scenes_info_file);
    
    scenes_elm = bof_tree.getroot().findall('scene');
    
    if scenes_elm is None:
      print "Invalid bof info file: No scenes element"
      sys.exit(-1);
         
 
    #find scene paths
    for s in range(0, len(scenes_elm)):
        path = scenes_elm[s].get("path");
        name = scenes_elm[s].get("name");
        
        if path is None:
            print "Error parsing scene path"
            sys.exit(-1);
            
        if name is None:
            print "Error parsing scene name"
            sys.exit(-1);
        
        model_dirs.append(path); 
        model_names.append(name);  

#*********************The Main Algorithm ****************************#

if __name__=="__main__":
  boxm_batch.register_processes();
  boxm_batch.register_datatypes();

  class dbvalue:
    def __init__(self, index, type):
      self.id = index    # unsigned integer
      self.type = type   # string


  #Parse inputs
  parser = optparse.OptionParser(description='Compute Expected Color Scene');

  parser.add_option('--scenes_info', action="store", dest="scenes_info", type="string", default="");
  parser.add_option('--num_cores', action="store", dest="num_cores", type="int", default=4);
  parser.add_option('--grey_offset', action="store", dest="grey_offset", type="float", default=0);


  options, args = parser.parse_args()

  scenes_info = options.scenes_info;
  num_cores = options.num_cores;
  grey_offset  = options.grey_offset;
  
  model_dirs = [];
  model_names = [];
  parse_scenes_info(scenes_info, model_dirs, model_names);
  
  #Begin multiprocessing
  job_list=[];
  start_time = time.time();


  #Enqueue jobs
  for si in range (0, len(model_dirs)):
      if not os.path.isdir(model_dirs[si] +"/drishti/"):
        os.mkdir(model_dirs[si] +"/drishti/");
      current_job = boxm_job(model_dirs[si], model_names[si],grey_offset);
      job_list.append(current_job);
                              
  results = execute_jobs(job_list, num_cores);
  print results;
  print ("Pass 0 done")

  print ("Total running time: ");
  print(time.time() - start_time);
    

  



  
  
