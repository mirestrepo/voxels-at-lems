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
parser = optparse.OptionParser(description='Compute PCA Error Scene');
parser.add_option('--model_dir', action="store", dest="model_dir");
options, args = parser.parse_args();

model_dir = options.model_dir;

#model_dir = "/Users/isa/Experiments/boxm_cit_only_filtered";

output_dir = model_dir + "/gauss_grad_alpha";

if not os.path.isdir( output_dir + "/"):
    os.mkdir( output_dir + "/");

print("Creating a Scene");
bvpl_octree_batch.init_process("boxmCreateSceneProcess");
bvpl_octree_batch.set_input_string(0,  model_dir +"/alpha_scene.xml");
bvpl_octree_batch.run_process();
(scene_id, scene_type) = bvpl_octree_batch.commit_output(0);
scene= dbvalue(scene_id, scene_type);

print("Compute Gradients");
bvpl_octree_batch.init_process("bvplComputeGaussGradients");
bvpl_octree_batch.set_input_from_db(0, scene);
bvpl_octree_batch.set_input_string(1,  output_dir);
bvpl_octree_batch.run_process();
(scene_id, scene_type) = bvpl_octree_batch.commit_output(0);
grad_scene= dbvalue(scene_id, scene_type);