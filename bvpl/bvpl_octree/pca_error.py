# Computes the gaussian gradients on a boxm_alpha_scene

import bvpl_octree_batch;
import os;
bvpl_octree_batch.register_processes();
bvpl_octree_batch.register_datatypes();

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

print("Compute PCA reconstruction error");

# path containing pca matrices and info file
pca_dir = "/Users/isa/Experiments/PCA/CapitolBOXM_1_1_1";


print("Extract PC");
bvpl_octree_batch.init_process("bvplComputeTestErrorProcess");
bvpl_octree_batch.set_input_string(0, pca_dir);
bvpl_octree_batch.run_process();
  