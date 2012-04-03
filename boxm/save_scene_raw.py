import boxm_batch;
boxm_batch.register_processes();
boxm_batch.register_datatypes();

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string


model_dir="/Users/isa/Experiments/DowntownBOXM_12_12_4";

print("Creating a Scene");
boxm_batch.init_process("boxmCreateSceneProcess");
boxm_batch.set_input_string(0,  model_dir +"/mean_color_scene.xml");
boxm_batch.run_process();
(scene_id, scene_type) = boxm_batch.commit_output(0);
scene= dbvalue(scene_id, scene_type);

print("Save Scene");
boxm_batch.init_process("boxmSaveSceneRawProcess");
boxm_batch.set_input_from_db(0,scene);
boxm_batch.set_input_string(1, model_dir + "/raw_mean_scene");
boxm_batch.set_input_unsigned(2,0);
boxm_batch.set_input_unsigned(3,1);
boxm_batch.run_process();