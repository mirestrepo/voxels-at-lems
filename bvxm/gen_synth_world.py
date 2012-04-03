# Script to generate a synthetic world
# Author : Isabel Restrepo
# 03/2009

import bvxm_batch
import os
bvxm_batch.register_processes();
bvxm_batch.register_datatypes();

class dbvalue:
  def __init__(self, index, type):
    self.id = index
    self.type = type


# create world.
print("------------------------------------------")
print("Creating Voxel World");
bvxm_batch.init_process("bvxmGenSyntheticWorldProcess");
bvxm_batch.run_process();


print("Done");
