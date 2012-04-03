#!/bin/sh

#  run_exe.sh
#  voxels-at-lems
#
#  Created by Maria Isabel Restrepo on 11/29/11.
#  Copyright (c) 2011 Brown University. All rights reserved.

CONFIGURATION=Release;

#DBRECD vector field visualizer
#scene="/Users/isa/Experiments/helicopter_providence/tests_normals/max_level_6/proj_taylor_scene_0.xml";
#/Projects/lemsvxl/bin_xcode4/$CONFIGURATION/contrib/dbrec_lib/dbrec3d/exe/dbrec3d_render_vector_field -scene $scene

#*********************DBREC3 Segmentation******************************#
pcd_file_xyz="/Users/isa/Experiments/helicopter_providence/tests_normals/max_level_6/flipped_normals_xyz.pcd";
pcd_file_normals="/Users/isa/Experiments/helicopter_providence/tests_normals/max_level_6/flipped_normals_normals.pcd";
pcd_file_out="/Users/isa/Experiments/helicopter_providence/tests_normals/max_level_6/pc_clusters/cluster.pcd";
/Projects/lemsvxl/bin_xcode4/$CONFIGURATION/contrib/dbrec_lib/dbrec3d/exe/dbrec3d_pcd_segmentation $pcd_file_xyz $pcd_file_normals $pcd_file_out -tolerance 100 -min 200 -max 25000 -eps_angle 0.7


#PCL visualizer
pcd_file="/Users/isa/Experiments/helicopter_providence/tests_normals/max_level_6/flipped_normals.pcd";
pcd_file1="/Users/isa/Experiments/helicopter_providence/tests_normals/max_level_6/pc_clusters/cluster0.pcd"
pcd_file2="/Users/isa/Experiments/helicopter_providence/tests_normals/max_level_6/pc_clusters/cluster0.pcd"
pcd_file3="/Users/isa/Experiments/helicopter_providence/tests_normals/max_level_6/pc_clusters/cluster1.pcd"
pcd_file4="/Users/isa/Experiments/helicopter_providence/tests_normals/max_level_6/pc_clusters/cluster2.pcd"
pcd_file5="/Users/isa/Experiments/helicopter_providence/tests_normals/max_level_6/pc_clusters/cluster3.pcd"
pcd_file6="/Users/isa/Experiments/helicopter_providence/tests_normals/max_level_6/pc_clusters/cluster4.pcd"
pcd_file7="/Users/isa/Experiments/helicopter_providence/tests_normals/max_level_6/pc_clusters/cluster5.pcd"
pcd_file8="/Users/isa/Experiments/helicopter_providence/tests_normals/max_level_6/pc_clusters/cluster6.pcd"
pcd_file9="/Users/isa/Experiments/helicopter_providence/tests_normals/max_level_6/pc_clusters/cluster7.pcd"
pcd_file10="/Users/isa/Experiments/helicopter_providence/tests_normals/max_level_6/pc_clusters/cluster8.pcd"
pcd_file11="/Users/isa/Experiments/helicopter_providence/tests_normals/max_level_6/pc_clusters/cluster9.pcd"
#/Projects/pcl/src/build/visualization/tools/pcd_viewer $pcd_file $pcd_file1 $pcd_file2 $pcd_file3 

#$pcd_file4 $pcd_file5 $pcd_file6 $pcd_file7 $pcd_file8 $pcd_file9  $pcd_file10 $pcd_file11 

#/Projects/pcl/src/build/visualization/tools/pcd_viewer -ax 100 -normals 1 -normals_scale 10  $pcd_file 

#Cluster extraction
pcd_file_in="/Users/isa/Experiments/helicopter_providence/tests_normals/max_level_6/flipped_normals.pcd";
pcd_file_out="/Users/isa/Experiments/helicopter_providence/tests_normals/max_level_6/pc_clusters/cluster.pcd";

#/Projects/pcl/src/build/tools/cluster_extraction $pcd_file_in $pcd_file_out -tolerance 20 -min 100 -max 500
