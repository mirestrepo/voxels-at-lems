import boxm_batch;
import optparse;

boxm_batch.register_processes();
boxm_batch.register_datatypes();

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string


#Parse inputs
parser = optparse.OptionParser(description='Compute PCA Error Scene');
parser.add_option('--model_dir', action="store", dest="model_dir");
options, args = parser.parse_args();

model_dir = options.model_dir;

print("Creating a Scene");
boxm_batch.init_process("boxmCreateSceneProcess");
boxm_batch.set_input_string(0,  model_dir +"/boxm_scene.xml");
boxm_batch.run_process();
(scene_id, scene_type) = boxm_batch.commit_output(0);
scene= dbvalue(scene_id, scene_type);

print("*************************************");


print("Splitting the scene");
boxm_batch.init_process("boxmSplitSceneProcess");
boxm_batch.set_input_from_db(0, scene);
boxm_batch.run_process();
(scene_id, scene_type) = boxm_batch.commit_output(0);
apm_scene = dbvalue(scene_id, scene_type);
(scene_id, scene_type) = boxm_batch.commit_output(1);
alpha_scene = dbvalue(scene_id, scene_type);

print("Save Scene");
boxm_batch.init_process("boxmSaveSceneRawProcess");
boxm_batch.set_input_from_db(0,alpha_scene);
boxm_batch.set_input_string(1,model_dir + "/drishti/alpha_scene");
boxm_batch.set_input_unsigned(2,0);
boxm_batch.set_input_unsigned(3,1);
boxm_batch.run_process();