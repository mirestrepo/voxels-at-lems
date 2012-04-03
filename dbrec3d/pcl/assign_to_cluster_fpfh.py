#!/bin/python

#  assign_to_cluster_fpfh.py
#  voxels-at-lems
#
#  Created by Maria Isabel Restrepo on 11/14/11.
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

#grad_scene_path = "/Users/isa/Experiments/boxm_scili_full/steerable_filters_alpha/steerable_gauss_3d_scene.xml"
#valid_scene_path = "/Users/isa/Experiments/boxm_scili_full/steerable_filters_alpha/valid_scene.xml"
#pcd_file = "/Users/isa/Experiments/pcl/tests/boxm_scili_full.pcd"

#Run k-means
pcl_dir = "/Users/isa/Experiments/pcl/tests"
xyznormal_file = pcl_dir + "/boxm_scili.pcd";
fpfh_file =pcl_dir + "/fpfh_boxm_scili.pcd"; 
means_file = pcl_dir + "/means_50_scili/lowest_sse_means.txt"
output_dir = pcl_dir + "/means_50_scili";

dbrec3d_batch.init_process("pcl_k_means_assign_process");
dbrec3d_batch.set_input_string(0, xyznormal_file);
dbrec3d_batch.set_input_string(1, fpfh_file);
dbrec3d_batch.set_input_string(2,  means_file);
dbrec3d_batch.set_input_string(3,  output_dir);

dbrec3d_batch.run_process();