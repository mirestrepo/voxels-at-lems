# Script to split a sample scene and convert it to bvxm_grid
# Author : Isabel Restrepo
# Jan 19, 2010


import boxm_batch;
boxm_batch.register_processes();
boxm_batch.register_datatypes();

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string


model_dir = "/Users/isa/Experiments/CapitolBOXM";


print("Creating a Scene");
boxm_batch.init_process("boxmCreateSceneProcess");
boxm_batch.set_input_string(0,  model_dir +"/alpha_scene.xml");
boxm_batch.run_process();
(scene_id, scene_type) = boxm_batch.commit_output(0);
scene = dbvalue(scene_id, scene_type);

print("*************************************");

#convert_alpha = 0;  #flag to convert alpha to probability value
#
#print("Splitting the scene");
#boxm_batch.init_process("boxmSplitSceneProcess");
#boxm_batch.set_input_from_db(0, scene);
#boxm_batch.set_input_bool(1, convert_alpha);
#boxm_batch.run_process();
#(scene_id, scene_type) = boxm_batch.commit_output(0);
#apm_scene = dbvalue(scene_id, scene_type);
#(scene_id, scene_type) = boxm_batch.commit_output(1);
#alpha_scene = dbvalue(scene_id, scene_type);

#print("Save Scene");
#boxm_batch.init_process("boxmSaveOccupancyRawProcess");
#boxm_batch.set_input_from_db(0,alpha_scene);
#boxm_batch.set_input_string(1,model_dir + "/drishti/alpha_scene");
#boxm_batch.set_input_unsigned(2,0);
#boxm_batch.set_input_unsigned(3,1);
#boxm_batch.run_process();

print("Convert to regular grid");
boxm_batch.init_process("boxmSceneToBvxmGridProcess");
boxm_batch.set_input_from_db(0,scene);
boxm_batch.set_input_string(1, model_dir + "/alpha_grid.vox");
boxm_batch.set_input_unsigned(2, 0);
boxm_batch.set_input_bool(3,1);
boxm_batch.run_process();
(grid_id, grid_type) = boxm_batch.commit_output(0);
grid = dbvalue(grid_id, grid_type);


print("Save Grid");
boxm_batch.init_process("bvxmSaveGridRawProcess");
boxm_batch.set_input_from_db(0,grid);
boxm_batch.set_input_string(1,model_dir + "/drishti/alpha_grid.raw");
boxm_batch.run_process();