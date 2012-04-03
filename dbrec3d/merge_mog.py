import dbrec3d_batch;
dbrec3d_batch.register_processes();
dbrec3d_batch.register_datatypes();

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string


model_dir ="/Users/isa/Experiments/CapitolBOXM";


print("Creating a Scene");
dbrec3d_batch.init_process("boxmCreateSceneProcess");
dbrec3d_batch.set_input_string(0,  model_dir +"/apm_scene.xml");
dbrec3d_batch.run_process();
(scene_id, scene_type) = dbrec3d_batch.commit_output(0);
mog_scene = dbvalue(scene_id, scene_type);

print("*************************************");

print("Save Scene");
dbrec3d_batch.init_process("boxmSaveOccupancyRawProcess");
dbrec3d_batch.set_input_from_db(0,mog_scene);
dbrec3d_batch.set_input_string(1,model_dir + "/gauss_scene");
dbrec3d_batch.set_input_unsigned(2,0);
dbrec3d_batch.set_input_unsigned(3,0);
dbrec3d_batch.run_process();

#print("Merging the scene");
#dbrec3d_batch.init_process("boxmMergeMixturesProcess");
#dbrec3d_batch.set_input_from_db(0, mog_scene);
#dbrec3d_batch.run_process();
#(scene_id, scene_type) = dbrec3d_batch.commit_output(0);
#gauss_scene = dbvalue(scene_id, scene_type);


#print("Convert to regular grid");
#dbrec3d_batch.init_process("boxmSceneToBvxmGridProcess");
#dbrec3d_batch.set_input_from_db(0,mog_scene);
#dbrec3d_batch.set_input_string(1, model_dir + "/apm_scene.vox");
#dbrec3d_batch.set_input_unsigned(2, 0);
#dbrec3d_batch.set_input_bool(3, 1);
#dbrec3d_batch.run_process();
#(grid_id, grid_type) = dbrec3d_batch.commit_output(0);
#grid = dbvalue(grid_id, grid_type);
#
#print("Save Grid");
#dbrec3d_batch.init_process("bvxmSaveGridRawProcess");
#dbrec3d_batch.set_input_from_db(0,grid);
#dbrec3d_batch.set_input_string(1,pair_scene_dir + "/apm_scene.raw");
#dbrec3d_batch.run_process();
