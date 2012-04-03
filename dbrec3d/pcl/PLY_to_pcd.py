#!/bin/python

#  scene_to_pcl.py
#  voxels-at-lems
#
#  Created by Isabel Restrepo on 11/2/11.
#  Copyright (c) 2011 Brown University. All rights reserved.


import dbrec3d_batch;
import os;
import optparse;

dbrec3d_batch.register_processes();
dbrec3d_batch.register_datatypes();

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

ply_fname = "/Users/isa/Experiments/helicopter_providence/tests_normals/max_level_6/flipped_normals.ply"
pcd_fname = "/Users/isa/Experiments/helicopter_providence/tests_normals/max_level_6/flipped_normals.pcd"
dbrec3d_batch.init_process("pcl_read_and_filter_ply_normals_process");

dbrec3d_batch.set_input_string(0, ply_fname);
dbrec3d_batch.set_input_string(1, pcd_fname);
dbrec3d_batch.set_input_float(2, 0.0701328); #this value corresponds to 5%
dbrec3d_batch.run_process();

