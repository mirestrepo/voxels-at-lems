#!/bin/sh

#  normalize_object_lcf.py
#  voxels-at-lems
#
#  Created by Maria Restrepo on 11/22/11.
#  Copyright (c) 2011 Brown University. All rights reserved.
#  Calls processes to normalize the local coordinate system on a point cloud


import dbrec3d_batch;
import os;
import optparse;

dbrec3d_batch.register_processes();
dbrec3d_batch.register_datatypes();

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string


pcl_dir = "/Users/isa/Experiments/pcl/tests"
#input_pcd_file = pcl_dir + "/boxm_scili.pcd"
#output_pcd_file = pcl_dir + "/boxm_scili_normalized_lcf.pcd"
input_pcd_file = pcl_dir + "/site12_objects/object_1.pcd"
output_pcd_file = pcl_dir + "/site12_objects/object_1_normalized_lcf.pcd"

dbrec3d_batch.init_process("pcl_trasform_xy_align_process");
dbrec3d_batch.set_input_string(0, input_pcd_file);
dbrec3d_batch.set_input_string(1, output_pcd_file);
dbrec3d_batch.run_process();