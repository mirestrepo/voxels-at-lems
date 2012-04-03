# Script to find edges in a scene. 

#In this test
#1. Create Scene
#2. Create kernel 
#3. Apply kernel to the scene
#4. Convert kernel responses to dbrec3d parts
#5. Perform non-maxima suppression
#5. Display results as raw


import dbrec3d_batch;
import os;

dbrec3d_batch.register_processes();
dbrec3d_batch.register_datatypes();

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string


model_dir = "/Users/isa/Experiments/CapitolBOXMSmall";

output_path = "/Users/isa/Experiments/tests/edges";
if not os.path.isdir( output_path + "/"):
  os.mkdir( output_path + "/");
  
convert_to_grid = 1;
save_raw = 1;
  
# Main axis of edges is perpendicular to the plane of ++++ and -----. Cannonical axis is the X-axis
min_x = -1;
max_x = 0;
min_y = -2;
max_y = 2;
min_z = 0;
max_z = 0;


#Get directions

#from generate_directions import dirs_edges;
from math import pi;
#
#angle_res = pi/2;
#azimutal_res = pi/2;
#
#directions = dirs_edges(angle_res, azimutal_res);
#
directions=[];
dir = 0.0, 0.0, 1.0, pi/2;
directions.append(dir);
dir = -1.0, 0.0, 0.0, pi/2;
directions.append(dir);
dir = 0.0, 0.0, -1.0, pi/2;
directions.append(dir);
dir = 1.0, 0.0, 0.0, pi/2;
directions.append(dir);


#Print directions to file for future reference
filename = output_path + "/dirs.txt"
FILE = open(filename, "w");
import pprint
pp= pprint.PrettyPrinter(stream=FILE);
pp.pprint(directions);


print("Creating a Scene");
dbrec3d_batch.init_process("boxmCreateSceneProcess");
dbrec3d_batch.set_input_string(0,  model_dir +"/gaussf1_scene.xml");
dbrec3d_batch.run_process();
(scene_id, scene_type) = dbrec3d_batch.commit_output(0);
gauss_scene= dbvalue(scene_id, scene_type);

for i in range(0,len(directions)) :
#for i in range(0,1) :
  dir = directions[i];
  axis_x = dir[0];
  axis_y = dir[1];
  axis_z = dir[2];
  angle = dir[3]
  
  output_dir = output_path + "/dir_" + str(i);
  if not os.path.isdir( output_dir + "/"):
    os.mkdir( output_dir + "/");

  print("Creating 3D edge kernel");
  dbrec3d_batch.init_process("bvplCreateEdge3dKernelProcess");
  dbrec3d_batch.set_input_int(0,min_x);
  dbrec3d_batch.set_input_int(1,max_x);
  dbrec3d_batch.set_input_int(2,min_y);
  dbrec3d_batch.set_input_int(3,max_y);
  dbrec3d_batch.set_input_int(4,min_z);
  dbrec3d_batch.set_input_int(5,max_z);
  dbrec3d_batch.set_input_float(6,axis_x);
  dbrec3d_batch.set_input_float(7,axis_y);
  dbrec3d_batch.set_input_float(8,axis_z);
  dbrec3d_batch.set_input_float(9,angle);
  dbrec3d_batch.run_process();
  (kernel_id,kernel_type)= dbrec3d_batch.commit_output(0);
  kernel = dbvalue(kernel_id,kernel_type);

  #print("Running Operator");
  dbrec3d_batch.init_process("bvplSceneKernelOperatorProcess");
  dbrec3d_batch.set_input_from_db(0,gauss_scene);
  dbrec3d_batch.set_input_from_db(1,kernel);
  dbrec3d_batch.set_input_string(2,"bsta_gauss_f1");
  dbrec3d_batch.set_input_string(3,"positive_gauss_convolution");
  dbrec3d_batch.set_input_string(4, output_dir);
  dbrec3d_batch.run_process();
  (out_scene_id,out_scene_type)= dbrec3d_batch.commit_output(0);
  kernel_scene = dbvalue(out_scene_id,out_scene_type);

  
#  print("Convert to regular grid");
#  dbrec3d_batch.init_process("boxmSceneToBvxmGridProcess");
#  dbrec3d_batch.set_input_from_db(0,kernel_scene);
#  dbrec3d_batch.set_input_string(1, output_dir + "/bvpl_response.vox");
#  dbrec3d_batch.set_input_unsigned(2, resolution);
#  dbrec3d_batch.set_input_bool(3, enforce_level);
#  dbrec3d_batch.run_process();
#  (grid_id, grid_type) = dbrec3d_batch.commit_output(0);
#  grid = dbvalue(grid_id, grid_type);
#  
#  print("Save Grid");
#  dbrec3d_batch.init_process("bvxmSaveGridRawProcess");
#  dbrec3d_batch.set_input_from_db(0,grid);
#  dbrec3d_batch.set_input_string(1,output_dir + "/bvpl_response.raw");
#  dbrec3d_batch.run_process();

  print("Convert to Parts")
  dbrec3d_batch.init_process("dbrec3dKernelsToPartsProcess");
  dbrec3d_batch.set_input_from_db(0, kernel_scene);
  dbrec3d_batch.set_input_from_db(1, kernel);
  dbrec3d_batch.run_process();
  (id, type) = dbrec3d_batch.commit_output(0);
  context_id = dbvalue(id, type);

  print("Non-Maxima supression")
  dbrec3d_batch.init_process("dbrec3dNonMaxSuppressionProcess");
  dbrec3d_batch.set_input_from_db(0, context_id);
  dbrec3d_batch.run_process();
  context_id = dbvalue(id, type);

  print("Get the response")
  dbrec3d_batch.init_process("dbrec3dGetResponseProcess");
  dbrec3d_batch.set_input_from_db(0, context_id);
  dbrec3d_batch.run_process();
  (scene_id, scene_type) = dbrec3d_batch.commit_output(0);
  response_scene= dbvalue(scene_id, scene_type);
  
  if save_raw:
    print("Save Scene");
    dbrec3d_batch.init_process("boxmSaveOccupancyRawProcess");
    dbrec3d_batch.set_input_from_db(0,response_scene);
    dbrec3d_batch.set_input_string(1,output_dir + "/dbrec3d_suppressed_response");
    dbrec3d_batch.set_input_unsigned(2,0);
    dbrec3d_batch.set_input_unsigned(3,1);
    dbrec3d_batch.run_process();
  
  if convert_to_grid:
    resolution = 0;
    enforce_level = 1;

    print("Convert to regular grid");
    dbrec3d_batch.init_process("boxmSceneToBvxmGridProcess");
    dbrec3d_batch.set_input_from_db(0,response_scene);
    dbrec3d_batch.set_input_string(1, output_dir + "/dbrec3d_suppressed_response.vox");
    dbrec3d_batch.set_input_unsigned(2, resolution);
    dbrec3d_batch.set_input_bool(3, enforce_level);
    dbrec3d_batch.run_process();
    (grid_id, grid_type) = dbrec3d_batch.commit_output(0);
    grid = dbvalue(grid_id, grid_type);
  
    print("Save Grid");
    dbrec3d_batch.init_process("bvxmSaveGridRawProcess");
    dbrec3d_batch.set_input_from_db(0,grid);
    dbrec3d_batch.set_input_string(1,output_dir + "/dbrec3d_suppressed_response.raw");
    dbrec3d_batch.run_process();

    print("Writing Orientation Grid");
    dbrec3d_batch.init_process("bvxmSaveRGBAGridVrmlProcess");
    dbrec3d_batch.set_input_from_db(0,grid);
    dbrec3d_batch.set_input_float(1,0.001);
    dbrec3d_batch.set_input_string(2,output_dir + "/edges.wrl");
    dbrec3d_batch.run_process();
  
  print("Save Parts and Contexts");
  dbrec3d_batch.init_process("dbrec3dXmlWriteProcess");
  dbrec3d_batch.set_input_string(0, output_path + "/hierarchy.xml");
  dbrec3d_batch.set_input_string(1, output_path + "/contexts.xml");
  dbrec3d_batch.run_process();
  
  #clean up database
  dbrec3d_batch.remove_data(kernel.id);
  dbrec3d_batch.remove_data(response_scene.id);
  #dbrec3d_batch.remove_data(grid.id);


  