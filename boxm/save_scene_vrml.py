import boxm_batch;
boxm_batch.register_processes();
boxm_batch.register_datatypes();

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string


model_dir = "/Users/isa/Experiments/Synthetic";



print("Creating a Scene");
boxm_batch.init_process("boxmCreateSceneProcess");
boxm_batch.set_input_string(0,  model_dir +"/alpha_scene.xml");
boxm_batch.run_process();
(scene_id, scene_type) = boxm_batch.commit_output(0);
scene= dbvalue(scene_id, scene_type);

print("*************************************");


print("Save Scene to VRML");
boxm_batch.init_process("boxmSaveSceneVrmlProcess");
boxm_batch.set_input_from_db(0, scene);
boxm_batch.set_input_string(1, model_dir + "alpha_scene.wrl");
boxm_batch.run_process();


