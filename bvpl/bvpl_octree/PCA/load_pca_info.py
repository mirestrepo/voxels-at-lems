
import bvpl_octree_batch

  
class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

bvpl_octree_batch.register_processes();
bvpl_octree_batch.register_datatypes();

pca_dir="/Users/isa/Experiments/PCA/CapitolBOXMSmall/10";

print("Loading PCA Info");
bvpl_octree_batch.init_process("bvplLoadPCAInfoProcess");
bvpl_octree_batch.set_input_string(0, pca_dir);
bvpl_octree_batch.run_process();
(id, type) = bvpl_octree_batch.commit_output(0);
pca_info = dbvalue(id, type);