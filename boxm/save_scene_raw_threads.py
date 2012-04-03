import boxm_batch
import multiprocessing
import Queue 
import time

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

class save_scene_job():
    def __init__(self,input_scene_path,output_scene_path):
        self.input_scene_path=input_scene_path;
        self.output_scene_path = output_scene_path;
        
        
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
            
            print("Creating a Scene");
            boxm_batch.init_process("boxmCreateSceneProcess");
            boxm_batch.set_input_string(0, job.input_scene_path);
            boxm_batch.run_process();
            (scene_id, scene_type) = boxm_batch.commit_output(0);
            scene= dbvalue(scene_id, scene_type);

            print("Save Scene");
            boxm_batch.init_process("boxmSaveOccupancyRawProcess");
            boxm_batch.set_input_from_db(0,scene);
            boxm_batch.set_input_string(1, job.output_scene_path);
            boxm_batch.set_input_unsigned(2,0);
            boxm_batch.set_input_unsigned(3,1);
            boxm_batch.run_process();
            
            print ("Runing time for worker:", self.name)
            print(time.time() - start_time);


###### The Main Algorithm ##############

boxm_batch.register_processes();
boxm_batch.register_datatypes();

model_path = "/Users/isa/Experiments/Taylor/CapitolBOXMSmall";


kernel_list=[];

kernel_list.append("I0");
kernel_list.append("Ix");
kernel_list.append("Iy");
kernel_list.append("Iz");
kernel_list.append("Ixx");
kernel_list.append("Iyy");
kernel_list.append("Izz");
kernel_list.append("Ixy");
kernel_list.append("Ixz");
kernel_list.append("Iyz");

#Begin multiprocessing
t1=time.time();
work_queue=multiprocessing.Queue();
num_cores=8;
job_list=[];


if __name__=="__main__":
  #Enqueue jobs
  for i in range(0, len(kernel_list)):
  
      scene_in_path = model_path + "/" + kernel_list[i] + "/float_response_scene.xml";
      scene_out_path = model_path + "/" + kernel_list[i]+ "/float_response_scene";
      
      current_job = save_scene_job(scene_in_path, scene_out_path);
      job_list.append(current_job);
              
  execute_jobs(job_list, num_cores);
