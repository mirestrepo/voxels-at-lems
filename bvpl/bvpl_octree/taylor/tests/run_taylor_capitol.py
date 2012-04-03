import os;
from multiprocessing import Queue
from taylor_kernel_threads import taylor_kernel_job,execute_jobs
import time
import bvpl_octree_batch

bvpl_octree_batch.register_processes();
bvpl_octree_batch.register_datatypes();

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string


#model_dir ="/Users/isa/Experiments/CapitolBOXM_1_1_1";
#output_dir = "/Users/isa/Experiments/Taylor/CapitolBOXM_1_1_1";
#kernel_path = "/Projects/vxl/src/contrib/brl/bseg/bvpl/doc/taylor2_5_5_5";


model_dir ="/Users/isa/Experiments/CapitolBOXMSmall";
output_dir = "/Users/isa/Experiments/Taylor/CapitolBOXMSmall";
kernel_path = "/Projects/vxl/src/contrib/brl/bseg/bvpl/doc/taylor2_5_5_5";

if not os.path.isdir( output_dir + "/"):
    os.mkdir( output_dir + "/");

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

blocks_x = 1; blocks_y = 1; blocks_z=1;

print("Creating a Scene");
bvpl_octree_batch.init_process("boxmCreateSceneProcess");
bvpl_octree_batch.set_input_string(0,  model_dir +"/mean_color_scene.xml");
bvpl_octree_batch.run_process();
(scene_id, scene_type) = bvpl_octree_batch.commit_output(0);
scene= dbvalue(scene_id, scene_type);

#Begin multiprocessing
t1=time.time();
work_queue=Queue();
num_cores=8;
job_list=[];


if __name__=="__main__":
  #Enqueue jobs
  for curr_kernel in range(0, len(kernel_list)):
  #for curr_kernel in range(0, 1):
      #curr_kernel = 1;
      for i in range(0, blocks_x):
          for j in range(0, blocks_y):
              for k in range(0, blocks_z):
                  curr_kernel_path = kernel_path + "/" + kernel_list[curr_kernel]+ ".txt";
                  output_path = output_dir + "/" + kernel_list[curr_kernel];
                  if not os.path.isdir( output_path + "/"):
                      os.mkdir( output_path + "/");
                  current_job = taylor_kernel_job(scene, curr_kernel_path, i, j, k, output_path);
                  job_list.append(current_job);
              
  execute_jobs(job_list, num_cores);

  