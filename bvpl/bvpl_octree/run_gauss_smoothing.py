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



class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

class gauss_smoothing_job():
    def __init__(self,scene, sigma , block_i, block_j, block_k, output_path, cell_length):
        self.scene = scene;
        self.sigma = sigma;
        self.block_i = block_i;
        self.block_j = block_j;
        self.block_k = block_k;
        self.output_path = output_path;
        self.cell_length = cell_length;
        
        
def execute_jobs(jobs, num_procs=5):
    work_queue=multiprocessing.Queue();
    result_queue=multiprocessing.Queue();
    for job in jobs:
        work_queue.put(job)
    
    for i in range(num_procs):
        worker= gauss_kernel_worker(work_queue,result_queue)
        worker.start();
        print("worker with name ",worker.name," started!")
        
    # collect the results off the queue
    #important: having a result queue makes the execute_jobs wait for all jobs in the queue before exiting
    results = []
    while len(results) < len(jobs):
        result = result_queue.get()
        results.append(result)
 
    return results
        
class gauss_kernel_worker(multiprocessing.Process):
 
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
            
            print("Creating Gauss kernel");
            bvpl_octree_batch.init_process("bvpl_create_gauss3d_kernel_process");
            bvpl_octree_batch.set_input_float(0,job.sigma);
            bvpl_octree_batch.set_input_float(1,job.sigma);
            bvpl_octree_batch.set_input_float(2,job.sigma);
            bvpl_octree_batch.set_input_float(3,1.0);
            bvpl_octree_batch.set_input_float(4,0.0);
            bvpl_octree_batch.set_input_float(5,0.0);
            bvpl_octree_batch.set_input_float(6,0.0);
            bvpl_octree_batch.run_process();
            (kernel_id,kernel_type)= bvpl_octree_batch.commit_output(0);
            kernel = dbvalue(kernel_id,kernel_type);


            print("Running Kernel");
            bvpl_octree_batch.init_process("bvplBlockKernelOperatorProcess");
            bvpl_octree_batch.set_input_from_db(0,job.scene);
            bvpl_octree_batch.set_input_from_db(1,kernel);
            bvpl_octree_batch.set_input_int(2, job.block_i);
            bvpl_octree_batch.set_input_int(3, job.block_j)
            bvpl_octree_batch.set_input_int(4, job.block_k)
            bvpl_octree_batch.set_input_string(5,"algebraic");
            bvpl_octree_batch.set_input_string(6, job.output_path);
            bvpl_octree_batch.set_input_double(7, job.cell_length);
            bvpl_octree_batch.run_process();
            
            print ("Runing time for worker:", self.name)
            print(time.time() - start_time);
      
            #output exit code in this case
            #important: having a result queue makes the execute_jobs wait for all jobs in the queue before exiting
            self.result_queue.put(0);

if __name__=="__main__":

  bvpl_octree_batch.register_processes();
  bvpl_octree_batch.register_datatypes();

  parser = optparse.OptionParser(description='Run Taylor Kernels');

  parser.add_option('--model_dir', action="store", dest="model_dir");
  parser.add_option('--num_cores', action="store", dest="num_cores", type="int", default=4);
  parser.add_option('--nblocks_x', action="store", dest="nblocks_x", type="int");
  parser.add_option('--nblocks_y', action="store", dest="nblocks_y", type="int");
  parser.add_option('--nblocks_z', action="store", dest="nblocks_z", type="int");


  options, args = parser.parse_args();

  model_dir = options.model_dir;
  nblocks_x = options.nblocks_x;
  nblocks_y = options.nblocks_y;
  nblocks_z = options.nblocks_z;
  num_cores = options.num_cores;

  if not os.path.isdir(model_dir +"/"):
      print "Invalid Model Dir"
      sys.exit(-1);


  print("Creating a Scene");
  bvpl_octree_batch.init_process("boxmCreateSceneProcess");
  bvpl_octree_batch.set_input_string(0,  model_dir +"/site12_pmvs.xml");
  bvpl_octree_batch.run_process();
  (scene_id, scene_type) = bvpl_octree_batch.commit_output(0);
  scene= dbvalue(scene_id, scene_type);

  #Begin multiprocessing
  t1=time.time();
  job_list=[];


  blocks_x = [i for i in range(0,nblocks_x)];
  blocks_y = [i for i in range(0,nblocks_y)];
  blocks_z = [i for i in range(0,nblocks_z)];
  
  random.shuffle(blocks_x);
  random.shuffle(blocks_y);
  random.shuffle(blocks_y);

  #Enqueue jobs
  for i in range(0, len(blocks_x)):
      for j in range(0, len(blocks_y)):
          for k in range(0, len(blocks_z)):
              block_i = blocks_x[i]; block_j = blocks_y[j]; block_k = blocks_z[k];
              current_job = gauss_smoothing_job(scene, 3.0, block_i, block_j, block_k, model_dir, 1.0);
              job_list.append(current_job);
  
  # wait for all the jobs            
  results = execute_jobs(job_list, num_cores);
  
  print("Creating a Scene");
  bvpl_octree_batch.init_process("boxmCreateSceneProcess");
  bvpl_octree_batch.set_input_string(0,  model_dir +"/float_response_scene.xml");
  bvpl_octree_batch.run_process();
  (scene_id, scene_type) = bvpl_octree_batch.commit_output(0);
  scene= dbvalue(scene_id, scene_type);
  
  print("Save Scene");
  bvpl_octree_batch.init_process("boxmSaveSceneRawProcess");
  bvpl_octree_batch.set_input_from_db(0,scene);
  bvpl_octree_batch.set_input_string(1,model_dir + "/drishti/gauss_scene");
  bvpl_octree_batch.set_input_unsigned(2,0);
  bvpl_octree_batch.set_input_unsigned(3,1);
  bvpl_octree_batch.run_process();
  