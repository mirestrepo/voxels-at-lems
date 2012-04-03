# Script to merge the mixture of gaussians inside a grid into single gaussians. The result is a grid with univariate gaussians
# Author : Isabel Restrepo
# 3-26-2009

import bvxm_batch
import os
bvxm_batch.register_processes();
bvxm_batch.register_datatypes();

#Delay for debugging
import time
time.sleep(30);


world_dir = "/Users/isa/Experiments/CapitolSiteHigh_sfm/capitol_rotated"
results_dir ="/Users/isa/Experiments/CapitolSiteHigh_sfm/capitol_rotated";


print("------------------------------------------")
print("Merging Mixtures");
bvxm_batch.init_process("bvxmMergeMogProcess");
bvxm_batch.set_input_string(0,world_dir + "/gauss_f3.vox");
bvxm_batch.set_input_string(1,results_dir + "/KL_gaussf1.vox");
bvxm_batch.run_process();

print("------------------------------------------")
print("Most probable mode");
bvxm_batch.init_process("bvxmMogToMpmProcess");
bvxm_batch.set_input_string(0,world_dir + "/gauss_f3.vox");
bvxm_batch.set_input_string(1,results_dir + "/MPM_gaussf1.vox");
bvxm_batch.run_process();