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

pcd_fname = "/Users/isa/Experiments/helicopter_providence/tests_normals/max_level_6/flipped_normals.pcd"

dbrec3d_batch.init_process("pcl_split_points_and_normals_process");
dbrec3d_batch.set_input_string(0, pcd_fname);
dbrec3d_batch.run_process();

