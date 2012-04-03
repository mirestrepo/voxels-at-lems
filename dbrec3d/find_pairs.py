# Script to find pairs of primitives in a scene. 

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
dbrec3d_batch.set_input_string(0, output_path + "/hierarchy.xml");
dbrec3d_batch.set_input_string(1, output_path + "/contexts.xml");
dbrec3d_batch.run_process();

dbrec3d_batch.print_db();

#Parameters to group edge "0" and "1"
mean_x = 2.0; mean_y = 0; mean_z = 2.0;
var = 3;
xmin=-5; ymin=-1; zmin=-7;
xmax=0; ymax=1; zmax=0;

print("Composing pairs");
id_0 = 0; id_1=1;
print(str(id_0));
print(str(id_1));
dbrec3d_batch.init_process("dbrec3dFindPairsProcess");
dbrec3d_batch.set_input_int(0, id_0);
dbrec3d_batch.set_input_int(1, id_1);
dbrec3d_batch.set_input_double(2,mean_x); 
dbrec3d_batch.set_input_double(3,mean_y);
dbrec3d_batch.set_input_double(4,mean_z);
dbrec3d_batch.set_input_double(5,var);
dbrec3d_batch.set_input_double(6,var);
dbrec3d_batch.set_input_double(7,var);
dbrec3d_batch.set_input_int(8,xmin);
dbrec3d_batch.set_input_int(9,ymin);
dbrec3d_batch.set_input_int(10,zmin);
dbrec3d_batch.set_input_int(11,xmax);
dbrec3d_batch.set_input_int(12,ymax);
dbrec3d_batch.set_input_int(13,zmax);
dbrec3d_batch.set_input_string(14, pair_scene_dir);
dbrec3d_batch.run_process();
(id,type)= dbrec3d_batch.commit_output(0);
composite_context_id = dbvalue(id,type);

print("Save VRML");
dbrec3d_batch.init_process("dbrec3dSaveVrmlProcess");
dbrec3d_batch.set_input_from_db(0,composite_context_id);
dbrec3d_batch.set_input_string(1,pair_scene_dir + "/edges_01.wrl");
dbrec3d_batch.set_input_double(2, -0.13);
dbrec3d_batch.set_input_double(3, -0.08);
dbrec3d_batch.set_input_double(4, 0);
dbrec3d_batch.set_input_double(5, -0.08);
dbrec3d_batch.set_input_double(6, -0.03);
dbrec3d_batch.set_input_double(7, 0.05);
dbrec3d_batch.run_process();

 
print("Save Parts and Contexts");
dbrec3d_batch.init_process("dbrec3dXmlWriteProcess");
dbrec3d_batch.set_input_string(0, pair_scene_dir + "/hierarchy.xml");
dbrec3d_batch.set_input_string(1, pair_scene_dir + "/contexts.xml");
dbrec3d_batch.run_process();



  





#Save Raw

  



  





#Save Raw