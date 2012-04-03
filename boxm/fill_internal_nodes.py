import boxm_batch;
import os;
import optparse;


boxm_batch.register_processes();
boxm_batch.register_datatypes();

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string


print("Filling internal nodes");

#Parse inputs
parser = optparse.OptionParser(description='Fill Internal Nodes');

parser.add_option('--model_dir', action="store", dest="model_dir", type="string", default="");
parser.add_option('--model_name', action="store", dest="model_name", type="string",default="");


options, args = parser.parse_args()

model_dir = options.model_dir;
model_name = options.model_name;

if len(model_dir) == 0:
  print "Missing Model Dir"
  sys.exit(-1);

if len(model_name) == 0:
  print "Missing Model Name"
  sys.exit(-1);


print("Creating a Scene");
boxm_batch.init_process("boxmCreateSceneProcess");
boxm_batch.set_input_string(0,  model_dir +"/" + str(model_name) + ".xml");
boxm_batch.run_process();
(scene_id, scene_type) = boxm_batch.commit_output(0);
scene = dbvalue(scene_id, scene_type);

print("*************************************");


print("Filling internal nodes");
boxm_batch.init_process("boxm_fill_internal_cells_process");
boxm_batch.set_input_from_db(0, scene);
boxm_batch.run_process();
(scene_id, scene_type) = boxm_batch.commit_output(0);
filled_scene = dbvalue(scene_id, scene_type);

