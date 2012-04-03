# Computes the gaussian gradients on a boxm_alpha_scene

import bvpl_octree_batch;
import os;
bvpl_octree_batch.register_processes();
bvpl_octree_batch.register_datatypes();

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

print("Computing Steerable Gaussian Filters");

#model_dir = "/Users/isa/Experiments/helicopter_providence/boxm_scenes/site12"
#output_dir = "/Users/isa/Experiments/helicopter_providence/boxm_scenes/site12/steerable_filters_alpha";

model_dir="/Users/isa/Experiments/boxm_scili_full"
output_dir="/Users/isa/Experiments/boxm_scili_full/steerable_filters_alpha";

#model_dir = "/Users/isa/Experiments/boxm_cit_only_filtered"
#output_dir = "/Users/isa/Experiments/boxm_cit_only_filtered/steerable_filters_alpha";

if not os.path.isdir( output_dir + "/"):
    os.mkdir( output_dir + "/");

print("Creating a Scene");
bvpl_octree_batch.init_process("boxmCreateSceneProcess");
bvpl_octree_batch.set_input_string(0,  model_dir +"/alpha_scene.xml");
bvpl_octree_batch.run_process();
(scene_id, scene_type) = bvpl_octree_batch.commit_output(0);
scene= dbvalue(scene_id, scene_type);

print("Init responses scene");
bvpl_octree_batch.init_process("bvplInitSFResponseSceneProcess");
bvpl_octree_batch.set_input_from_db(0, scene);
bvpl_octree_batch.set_input_string(1,  output_dir);
bvpl_octree_batch.run_process();
(scene_id, scene_type) = bvpl_octree_batch.commit_output(0);
response_scene= dbvalue(scene_id, scene_type);
(scene_id, scene_type) = bvpl_octree_batch.commit_output(1);
valid_scene= dbvalue(scene_id, scene_type);

print("Compute responses scene");
bvpl_octree_batch.init_process("bvplComputeSFRawResponseProcess");
bvpl_octree_batch.set_input_from_db(0, response_scene);
bvpl_octree_batch.set_input_from_db(1, valid_scene);
bvpl_octree_batch.set_input_int(2, 0);
bvpl_octree_batch.set_input_int(3, 0);
bvpl_octree_batch.set_input_int(4, 0);
bvpl_octree_batch.run_process();