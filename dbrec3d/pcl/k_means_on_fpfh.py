#!/bin/py

#  k_means_on_fpfh.py
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
fpfh_file =pcl_dir + "/fpfh_boxm_scili.pcd"; 
n_means = 50;
init_frac = 0.1;
init_iter = 10
max_iter = 500;
means_dir = pcl_dir + "/means_50_scili"

if not os.path.isdir(means_dir +"/"):
  os.mkdir(means_dir + "/");


dbrec3d_batch.init_process("pcl_k_means_learning_process");
dbrec3d_batch.set_input_string(0, fpfh_file);
dbrec3d_batch.set_input_unsigned(1, n_means);
dbrec3d_batch.set_input_double(2,  init_frac);
dbrec3d_batch.set_input_unsigned(3,  init_iter);
dbrec3d_batch.set_input_unsigned(4,  max_iter);
dbrec3d_batch.set_input_string(5,  means_dir);
dbrec3d_batch.run_process();

