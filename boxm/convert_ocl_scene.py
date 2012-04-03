import boxm_batch,os;
boxm_batch.register_processes();
boxm_batch.register_datatypes();


class dbvalue:
 def __init__(self, index, type):
   self.id = index # unsigned integer
   self.type = type # string


model_dir ="/Users/isa/Experiments/CapitolBOXM_6_4_4";
output_path = "/Users/isa/Experiments/tests/ocl_scene";
if not os.path.isdir( output_path + "/"):
  os.mkdir( output_path + "/");

max_mb = -1;


print("Creating a Scene");
boxm_batch.init_process("boxmCreateSceneProcess");
boxm_batch.set_input_string(0, model_dir + "/capitol_scene.xml");
boxm_batch.run_process();
(scene_id, scene_type) = boxm_batch.commit_output(0);
scene = dbvalue(scene_id, scene_type);

print("Convert Scene");
boxm_batch.init_process("boxmOclConvertBoxmToOclProcess");
boxm_batch.set_input_from_db(0, scene);
boxm_batch.set_input_string(1, output_path);
boxm_batch.set_input_int(2, -1);
boxm_batch.set_input_bool(3, 0);
boxm_batch.run_process();


# print("Refine Scene");
# boxm_batch.init_process("boxmOclRefineProcess");
# boxm_batch.set_input_string(0, "F:/APl/try4ocl/scene.xml");
# boxm_batch.set_input_float(1, prob_thresh);
# boxm_batch.run_process();

