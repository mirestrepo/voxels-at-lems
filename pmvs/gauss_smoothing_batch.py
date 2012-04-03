#!/usr/bin/python

import bvpl_octree_batch;
import multiprocessing
import Queue 
import time
import os;
import optparse;
from xml.etree.ElementTree import ElementTree
import sys

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

class gauss_job():
    def __init__(self,scene, kernel , block_i, block_j, block_k, output_path, cell_length):
        self.scene = scene;
        self.kernel = kernel;
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
        worker= gauss_worker(work_queue,result_queue)
        worker.start();
        print("worker with name ",worker.name," started!")
        
        
    # collect the results off the queue
    #important: having a result queue makes the execute_jobs wait for all jobs in the queue before exiting
    results = []
    while len(results) < len(jobs):
        result = result_queue.get()
        results.append(result)
 
    return results
        
        
class gauss_worker(multiprocessing.Process):
 
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
          
            
            bvpl_octree_batch.set_stdout('logs/log_' + str(os.getpid())+ ".txt");
  
              
            print("Running Kernel");
            bvpl_octree_batch.init_process("bvplBlockKernelOperatorProcess");
            bvpl_octree_batch.set_input_from_db(0,job.scene);
            bvpl_octree_batch.set_input_from_db(1,job.kernel);
            bvpl_octree_batch.set_input_int(2, job.block_i);
            bvpl_octree_batch.set_input_int(3, job.block_j)
            bvpl_octree_batch.set_input_int(4, job.block_k)
            bvpl_octree_batch.set_input_string(5,"algebraic");
            bvpl_octree_batch.set_input_string(6, job.output_path);
            bvpl_octree_batch.set_input_double(7, job.cell_length);
            bvpl_octree_batch.run_process();
                                
            print ("Runing time for worker:", self.name)
            print(time.time() - start_time);
            
            #free memory
            bvpl_octree_batch.reset_stdout();
            bvpl_octree_batch.clear();
            
            #output exit code in this case
            #important: having a result queue makes the execute_jobs wait for all jobs in the queue before exiting
            self.result_queue.put(0);
            
            
            

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
                
#function to parse and xml file containing the model directory and the xml_file_name (without the path)            
def parse_scenes_info(scenes_info_file, model_dirs, output_dirs, lengths, scene_blocks):
    
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
        cell_length = scenes_elm[s].get("cell_length");
        output_dir = scenes_elm[s].get("output_dir");
        
        if path is None:
            print "Invalid info file: Error parsing scene path"
            sys.exit(-1);
            
        if output_dir is None:
            print "Invalid info file: Error parsing output_dir"
            sys.exit(-1);
            
        if cell_length is None:
            print "Invalid info file: Error parsing cell_length"
            sys.exit(-1);
        
        model_dirs.append(path); 
        output_dirs.append(output_dir);  
        lengths.append(float(cell_length));
        blocks = []; 
        blocks.append(s);       
        parse_scene(path, blocks);
        scene_blocks.append(blocks);

#*********************The Main Algorithm ****************************#

if __name__=="__main__":
  bvpl_octree_batch.register_processes();
  bvpl_octree_batch.register_datatypes();

  class dbvalue:
    def __init__(self, index, type):
      self.id = index    # unsigned integer
      self.type = type   # string


  #Parse inputs
  parser = optparse.OptionParser(description='Compute Expected Color Scene');

  parser.add_option('--scenes_info', action="store", dest="scenes_info", type="string", default="");
  parser.add_option('--num_cores', action="store", dest="num_cores", type="int", default=4);
  parser.add_option('--sigma', action="store", dest="sigma", type="float", default=1.0);


  options, args = parser.parse_args()

  scenes_info = options.scenes_info;
  num_cores = options.num_cores;
  sigma  = options.sigma;
  
  model_dirs = [];
  output_dirs = [];
  lengths=[];
  scene_blocks =[];

  parse_scenes_info(scenes_info, model_dirs, output_dirs, lengths, scene_blocks);
  
  #Begin multiprocessing
  job_list=[];
  start_time = time.time();

  print("Creating Gauss kernel");
  bvpl_octree_batch.init_process("bvpl_create_gauss3d_kernel_process");
  bvpl_octree_batch.set_input_float(0,sigma);
  bvpl_octree_batch.set_input_float(1,sigma);
  bvpl_octree_batch.set_input_float(2,sigma);
  bvpl_octree_batch.set_input_float(3,1.0); #axis of rotation - irrelevant for isotropic gaussian
  bvpl_octree_batch.set_input_float(4,0.0);
  bvpl_octree_batch.set_input_float(5,0.0);
  bvpl_octree_batch.set_input_float(6,0.0); #rotation about axis of rotation ;)
  bvpl_octree_batch.run_process();
  (kernel_id,kernel_type)= bvpl_octree_batch.commit_output(0);
  kernel = dbvalue(kernel_id,kernel_type);


  #Enqueue jobs
  if(len(model_dirs)==len(output_dirs)==len(lengths)==len(scene_blocks) ):
      
    for scene_id in range (14, len(scene_blocks)):
        
        if not os.path.isdir(output_dirs[scene_id] +"/"):
            os.mkdir(output_dirs[scene_id] +"/");
            
        if not os.path.isdir(output_dirs[scene_id] +"/drishti/"):
            os.mkdir(output_dirs[scene_id] +"/drishti/");
        
        print("Creating a Scene");
        bvpl_octree_batch.init_process("boxmCreateSceneProcess");
        bvpl_octree_batch.set_input_string(0,  model_dirs[scene_id]);
        bvpl_octree_batch.run_process();
        (id, type) = bvpl_octree_batch.commit_output(0);
        scene= dbvalue(id, type);
         
        nblocks = scene_blocks[scene_id];
        print nblocks;
        for block_i in range (0, nblocks[1]):
            for block_j in range (0, nblocks[2]):
                for block_k in range (0, nblocks[3]):
                    current_job = gauss_job(scene, kernel , block_i, block_j, block_k, output_dirs[scene_id], lengths[scene_id]);
                    job_list.append(current_job);
                    
                              
        results = execute_jobs(job_list, num_cores);
        print results;
        
        print("Creating a Scene");
        bvpl_octree_batch.init_process("boxmCreateSceneProcess");
        bvpl_octree_batch.set_input_string(0,  output_dirs[scene_id] +"/float_response_scene.xml");
        bvpl_octree_batch.run_process();
        (id, type) = bvpl_octree_batch.commit_output(0);
        scene= dbvalue(id, type);
        
        print("Save Scene");
        bvpl_octree_batch.init_process("boxmSaveSceneRawProcess");
        bvpl_octree_batch.set_input_from_db(0,scene);
        bvpl_octree_batch.set_input_string(1, output_dirs[scene_id] + "/drishti/gauss_scene");
        bvpl_octree_batch.set_input_unsigned(2,0);
        bvpl_octree_batch.set_input_unsigned(3,1);
        bvpl_octree_batch.run_process();



  print ("Total running time: ");
  print(time.time() - start_time);
    

  



  
  
