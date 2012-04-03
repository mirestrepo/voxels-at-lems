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

grad_scene_path = "/Users/isa/Experiments/boxm_scili_full/steerable_filters_alpha/steerable_gauss_3d_scene.xml"
valid_scene_path = "/Users/isa/Experiments/boxm_scili_full/steerable_filters_alpha/valid_scene.xml"
pcd_file = "/Users/isa/Experiments/pcl/tests/boxm_scili_full.pcd"

#/Users/isa/Experiments/boxm_cit_only_filtered/steerable_filters_alpha
#
#grad_scene_path = "/Users/isa/Experiments/helicopter_providence/boxm_scenes/site12/steerable_filters_alpha/steerable_gauss_3d_scene.xml"
#valid_scene_path=  "/Users/isa/Experiments/helicopter_providence/boxm_scenes/site12/steerable_filters_alpha/valid_scene.xml"
#pcd_file = "/Users/isa/Experiments/pcl/tests/site_12.pcd"

#load  gradient scene
print("Creating a Scene");
dbrec3d_batch.init_process("boxmCreateSceneProcess");
dbrec3d_batch.set_input_string(0,  grad_scene_path);
dbrec3d_batch.run_process();
(scene_id, scene_type) = dbrec3d_batch.commit_output(0);
grad_scene= dbvalue(scene_id, scene_type);

#load valid scene
dbrec3d_batch.init_process("boxmCreateSceneProcess");
dbrec3d_batch.set_input_string(0,  valid_scene_path);
dbrec3d_batch.run_process();
(scene_id, scene_type) = dbrec3d_batch.commit_output(0);
valid_scene= dbvalue(scene_id, scene_type);

dbrec3d_batch.init_process("pcl_convert_scene_to_pc_process");
dbrec3d_batch.set_input_from_db(0, grad_scene);
dbrec3d_batch.set_input_from_db(1, valid_scene);
dbrec3d_batch.set_input_string(2,  pcd_file);
dbrec3d_batch.run_process();

