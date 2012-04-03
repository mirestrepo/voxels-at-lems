import dbrec3d_batch
import multiprocessing
import Queue 
import time
import optparse
import sys
import os
from xml.etree.ElementTree import ElementTree

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

class save_scene_job():
    def __init__(self,bof_dir,scene_id):
        self.bof_dir=bof_dir;
        self.scene_id= scene_id;
        
        
def execute_jobs(jobs, num_procs=5):
    work_queue=multiprocessing.Queue();
    result_queue=multiprocessing.Queue();
    for job in jobs:
        work_queue.put(job)
    
    for i in range(num_procs):
        worker= save_scene_worker(work_queue,result_queue)
        worker.start();
        print("worker with name ",worker.name," started!")
        
        
class save_scene_worker(multiprocessing.Process):
 
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
            
            print("Save Scene");
            dbrec3d_batch.init_process("bofSaveCategorySceneRawProcess");
            dbrec3d_batch.set_input_string(0,job.bof_dir);
            dbrec3d_batch.set_input_int(1, job.scene_id);
            dbrec3d_batch.run_process();
            
            print ("Runing time for worker:", self.name)
            print(time.time() - start_time);

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

###### The Main Algorithm ##############
if __name__=="__main__":

  dbrec3d_batch.register_processes();
  dbrec3d_batch.register_datatypes();

  #Parse inputs
  parser = optparse.OptionParser(description='bof Statistics Pass 0');

  parser.add_option('--bof_dir', action="store", dest="bof_dir");
  parser.add_option('--num_cores', action="store", dest="num_cores", type="int", default=4);

  options, args = parser.parse_args()

  bof_dir = options.bof_dir;
  num_cores = options.num_cores;


  if not os.path.isdir(bof_dir +"/"):
    print "Invalid bof Dir"
    sys.exit(-1);


 #parse the number of scenes
  bof_info_file = bof_dir + "/bof_info.xml";
  nscenes = parse_bof_info(bof_info_file);
  print "Number of Scenes:"
  print nscenes
  
  #Begin multiprocessing
  t1=time.time();
  work_queue=multiprocessing.Queue();
  num_cores=8;
  job_list=[];


  #Enqueue jobs
  for scene_id in range(0, nscenes):
      current_job = save_scene_job(bof_dir, scene_id);
      job_list.append(current_job);
              
  execute_jobs(job_list, num_cores);
