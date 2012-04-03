# Computes the gaussian gradients on a boxm_alpha_scene

import bvpl_octree_batch;
import os;
import optparse;


bvpl_octree_batch.register_processes();
bvpl_octree_batch.register_datatypes();

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

print("Computing Gaussian Gradients on Alpha");

#Parse inputs
parser = optparse.OptionParser(description='Save gradients to binary and text');
parser.add_option('--model_dir', action="store", dest="model_dir");
options, args = parser.parse_args();

model_dir = options.model_dir;

#model_dir = "/Users/isa/Experiments/boxm_cit_only_filtered";
grad_dir = model_dir + "/gauss_grad_alpha";


print("Creating a Scene");
bvpl_octree_batch.init_process("boxmCreateSceneProcess");
bvpl_octree_batch.set_input_string(0,  model_dir +"/alpha_scene.xml");
bvpl_octree_batch.run_process();
(scene_id, scene_type) = bvpl_octree_batch.commit_output(0);
alpha_scene= dbvalue(scene_id, scene_type);

print("Creating a Scene");
bvpl_octree_batch.init_process("boxmCreateSceneProcess");
bvpl_octree_batch.set_input_string(0,  grad_dir +"/float_gradient_scene.xml");
bvpl_octree_batch.run_process();
(scene_id, scene_type) = bvpl_octree_batch.commit_output(0);
grad_scene= dbvalue(scene_id, scene_type);

print("Compute Gradients");
bvpl_octree_batch.init_process("bvplGradSceneToBinProcess");
bvpl_octree_batch.set_input_from_db(0, alpha_scene);
bvpl_octree_batch.set_input_from_db(1, grad_scene);
bvpl_octree_batch.set_input_string(2,  grad_dir + "/scene_gradients.txt");
bvpl_octree_batch.run_process();
