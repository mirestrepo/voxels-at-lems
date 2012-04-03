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
parser.add_option('--ply_file', action="store", dest="ply_file");

options, args = parser.parse_args();

model_dir = options.model_dir;
ply_file = options.ply_file;

boxm_batch.init_process("boxmCreateSceneProcess");
boxm_batch.set_input_string(0,  model_dir +"/site12_pmvs.xml");
boxm_batch.run_process();
(scene_id, scene_type) = boxm_batch.commit_output(0);
scene= dbvalue(scene_id, scene_type);

print("*************************************");
boxm_batch.init_process("boxm_create_scene_from_ply_process");
boxm_batch.set_input_string(0,ply_file);
boxm_batch.set_input_from_db(1,scene);
boxm_batch.set_input_float(2,1.0);
boxm_batch.run_process();
(scene_id, scene_type) = boxm_batch.commit_output(0);
scene = dbvalue(scene_id, scene_type);


print("Save Scene");
boxm_batch.init_process("boxmSaveSceneRawProcess");
boxm_batch.set_input_from_db(0,scene);
boxm_batch.set_input_string(1,model_dir + "/drishti/ply_scene");
boxm_batch.set_input_unsigned(2,0);
boxm_batch.set_input_unsigned(3,1);
boxm_batch.run_process();