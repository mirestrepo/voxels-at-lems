#!/bin/python

#  convert_id_to_rgbcloud.py
#  voxels-at-lems
#
#  Created by Maria Isabel Restrepo on 11/15/11.
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


#Run k-means
pcl_dir = "/Users/isa/Experiments/pcl/tests"
id_pcd_file = pcl_dir + "/means_50_scili/class_id.pcd"
rgb_pcd_file = pcl_dir + "/means_50_scili/class_id_rgb.pcd"
nmeans = 50;

dbrec3d_batch.init_process("pcl_convert_id_to_rgb_process");
dbrec3d_batch.set_input_string(0, id_pcd_file);
dbrec3d_batch.set_input_string(1, rgb_pcd_file);
dbrec3d_batch.set_input_unsigned(2, nmeans);
dbrec3d_batch.run_process();