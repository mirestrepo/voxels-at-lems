# Temporary tests. 

#In this test
#1. Create Scene
#2. Create kernel 
#3. Apply kernel to the scene
#4. Display results as raw


import bvpl_octree_batch;
import os;
bvpl_octree_batch.register_processes();
bvpl_octree_batch.register_datatypes();

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

print("Running run_gauss_x.py");

model_dir = "/Users/isa/Experiments/CapitolBOXMSmall";
output_dirs = ["/Users/isa/Experiments/tests/gauss_x/x","/Users/isa/Experiments/tests/gauss_x/y","/Users/isa/Experiments/tests/gauss_x/z"];


sigma1 = 1;
sigma2 = 1;
sigma3 = 1;

axes_x=[-1.0,0.0,0.0];
axes_y=[0.0,-1.0,0.0];
axes_z=[0.0,0.0,1.0];

angle =  0.0;

print("Creating a Scene");
bvpl_octree_batch.init_process("boxmCreateSceneProcess");
bvpl_octree_batch.set_input_string(0,  model_dir +"/gaussf1_scene.xml");
bvpl_octree_batch.run_process();
(scene_id, scene_type) = bvpl_octree_batch.commit_output(0);
scene= dbvalue(scene_id, scene_type);

for i in range(0,1) :

  output_dir = output_dirs[i];
  
  if not os.path.isdir( output_dir + "/"):
    os.mkdir( output_dir + "/");
  
  axis_x = axes_x[i];
  axis_y = axes_y[i];
  axis_z = axes_z[i];
  
  if not os.path.isdir( output_dir + "/"):
    os.mkdir( output_dir + "/");

  print("Creating 3D edge kernel");
  bvpl_octree_batch.init_process("bvplCreateGauss3dXKernelProcess");
  bvpl_octree_batch.set_input_float(0,sigma1);
  bvpl_octree_batch.set_input_float(1,sigma2);
  bvpl_octree_batch.set_input_float(2,sigma3);
  bvpl_octree_batch.set_input_float(3,axis_x);
  bvpl_octree_batch.set_input_float(4,axis_y);
  bvpl_octree_batch.set_input_float(5,axis_z);
  bvpl_octree_batch.set_input_float(6,angle);
  bvpl_octree_batch.run_process();
  (kernel_id,kernel_type)= bvpl_octree_batch.commit_output(0);
  kernel = dbvalue(kernel_id,kernel_type);

  print("Running Operator");
  bvpl_octree_batch.init_process("bvplSceneKernelOperatorProcess");
  bvpl_octree_batch.set_input_from_db(0,scene);
  bvpl_octree_batch.set_input_from_db(1,kernel);
  bvpl_octree_batch.set_input_string(2,"bsta_gauss_f1");
  bvpl_octree_batch.set_input_string(3,"positive_gauss_convolution");
  bvpl_octree_batch.set_input_string(4, output_dir);
  bvpl_octree_batch.run_process();
  (out_scene_id,out_scene_type)= bvpl_octree_batch.commit_output(0);
  result_scene = dbvalue(out_scene_id,out_scene_type);

  resolution = 0;
  enforce_level = 1;

  print("Convert to regular grid");
  bvpl_octree_batch.init_process("boxmSceneToBvxmGridProcess");
  bvpl_octree_batch.set_input_from_db(0,result_scene);
  bvpl_octree_batch.set_input_string(1, output_dir + "/response.vox");
  bvpl_octree_batch.set_input_unsigned(2, resolution);
  bvpl_octree_batch.set_input_bool(3, enforce_level);
  bvpl_octree_batch.run_process();
  (grid_id, grid_type) = bvpl_octree_batch.commit_output(0);
  grid = dbvalue(grid_id, grid_type);

  print("Save Grid");
  bvpl_octree_batch.init_process("bvxmSaveGridRawProcess");
  bvpl_octree_batch.set_input_from_db(0,grid);
  bvpl_octree_batch.set_input_string(1,output_dir + "/response.raw");
  bvpl_octree_batch.run_process();