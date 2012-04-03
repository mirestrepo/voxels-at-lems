# Script to save a context to vml
#In this test
# -Load Scenes
# -Compose pairs
# -Save Raw


import dbrec3d_batch;
import os;

dbrec3d_batch.register_processes();
dbrec3d_batch.register_datatypes();

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string


model_dir = "/Users/isa/Experiments/CapitolBOXMSmall";

output_path = "/Users/isa/Experiments/tests/edges/";
  
pair_scene_dir = "/Users/isa/Experiments/tests/edges_pairs/0_1_pair";
if not os.path.isdir( pair_scene_dir + "/"):
  os.mkdir( pair_scene_dir + "/");
#Compose pairs

print("Loading Parts and Contexts");
dbrec3d_batch.init_process("dbrec3dXmlParseProcess");
dbrec3d_batch.set_input_string(0, pair_scene_dir + "/hierarchy.xml");
dbrec3d_batch.set_input_string(1, pair_scene_dir + "/contexts.xml");
dbrec3d_batch.run_process();

dbrec3d_batch.print_db();

print("Save VRML");
dbrec3d_batch.init_process("dbrec3dSaveVrmlProcess");
dbrec3d_batch.set_input_int(0,4);
dbrec3d_batch.set_input_string(1,pair_scene_dir + "/edges_01.wrl");
dbrec3d_batch.set_input_double(2, 0.13);
dbrec3d_batch.set_input_double(3, -0.08);
dbrec3d_batch.set_input_double(4, 0);
dbrec3d_batch.set_input_double(5, -0.08);
dbrec3d_batch.set_input_double(6, -0.03);
dbrec3d_batch.set_input_double(7, 0.05);
dbrec3d_batch.run_process();

 
print("Save Parts and Contexts");
dbrec3d_batch.init_process("dbrec3dXmlWriteProcess");
dbrec3d_batch.set_input_string(0, pair_scene_dir + "/hierarchy2.xml");
dbrec3d_batch.set_input_string(1, pair_scene_dir + "/contexts2.xml");
dbrec3d_batch.run_process();