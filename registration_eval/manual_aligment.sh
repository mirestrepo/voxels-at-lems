#!/bin/bash

#manual_aligment.sh contains a series of steps for manual registration
#of two point-clouds (PVM to PVM)

#*********** CVG DATA ****************************

#*************************************************
#*********** Site 1 ******************************
#*************************************************


#*********** Flight 4 -> Flight 2 ****************

#1. Pick Correspondances using MeshLab Align tool
#2. Save correspondances as a bwm correspondance file format
#3. Find transformation and transfom a point cloud using correspondances
# /Projects/vxl/bin/Release/contrib/brl/bbas/bwm/exe/bwm_3d_site_transform_points -corrs /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_1/f4-f2-corrs.txt -input_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_1/gauss_233_normals_pvn_99.ply -output_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_1/gauss_233_normals_pvn_99_f2_reg.ply -transform_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_1/f4-f2_Hs -pts0_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_1/f4-f2-pts0.ply -pts1_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_1/f4-f2-pts1.ply

#*********** Flight 4 -> Flight 2 ****************

#1. Pick Correspondances using MeshLab Align tool
#2. Save correspondances as a bwm correspondance file format
#3. Find transformation and transfom a point cloud using correspondances
# /Projects/vxl/bin/Release/contrib/brl/bbas/bwm/exe/bwm_3d_site_transform_points -corrs /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_1/f5-f2-corrs.txt -input_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_1/gauss_233_normals_pvn_99.ply -output_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_1/gauss_233_normals_pvn_99_f2_reg.ply -transform_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_1/f5-f2_Hs -pts0_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_1/f5-f2-pts0.ply -pts1_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_1/f5-f2-pts1.ply

#*********** Flight 2 -> LIDAR ****************

#1. Pick Correspondances using MeshLab Align tool
#2. Save correspondances as a bwm correspondance file format
#3. Find transformation and transfom a point cloud using correspondances
# /Projects/vxl/bin/Release/contrib/brl/bbas/bwm/exe/bwm_3d_site_transform_points -corrs /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight2_sites/site_1/f2-lidar-corrs.txt -input_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight2_sites/site_1/gauss_233_normals_pvn_99.ply -output_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight2_sites/site_1/gauss_233_normals_pvn_99_geo_reg.ply -transform_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight2_sites/site_1/Hs_geo -pts0_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight2_sites/site_1/f2-lidar-pts0.ply -pts1_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight2_sites/site_1/f2-lidar-pts1.ply

#*************************************************
#*********** Site 2 ******************************
#*************************************************

#*********** Flight 4 -> Flight 2 ****************

# 1. Pick Correspondances using MeshLab Align tool
# 2. Save correspondances as a bwm correspondance file format
# 3. Find transformation and transfom a point cloud using correspondances
# /Projects/vxl/bin/Release/contrib/brl/bbas/bwm/exe/bwm_3d_site_transform_points -corrs /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_2/f4-f2-corrs.txt -input_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_2/gauss_233_normals_pvn_99.ply -output_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_2/gauss_233_normals_pvn_99_f2_reg.ply -transform_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_2/f4-f2_Hs -pts0_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_2/f4-f2-pts0.ply -pts1_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_2/f4-f2-pts1.ply

#*********** Flight 5 -> Flight 4 ****************

#1. Pick Correspondances using MeshLab Align tool
#2. Save correspondances as a bwm correspondance file format
#3. Find transformation and transfom a point cloud using correspondances
# /Projects/vxl/bin/Release/contrib/brl/bbas/bwm/exe/bwm_3d_site_transform_points -corrs /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_2/f5-f4-corrs.txt -input_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_2/gauss_233_normals_pvn_99.ply -output_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_2/gauss_233_normals_pvn_99_f4_reg.ply -transform_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_2/f5-f4_Hs -pts0_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_2/f5-f4-pts0.ply -pts1_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_2/f5-f4-pts1.ply

#*********** Flight 2 -> LIDAR ****************

#1. Pick Correspondances using MeshLab Align tool
#2. Save correspondances as a bwm correspondance file format
#3. Find transformation and transfom a point cloud using correspondances
# /Projects/vxl/bin/Release/contrib/brl/bbas/bwm/exe/bwm_3d_site_transform_points -corrs /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight2_sites/site_2/f2-lidar-corrs.txt -input_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight2_sites/site_2/gauss_233_normals_pvn_99.ply -output_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight2_sites/site_2/gauss_233_normals_pvn_99_geo_reg.ply -transform_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight2_sites/site_2/Hs_geo -pts0_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight2_sites/site_2/f2-lidar-pts0.ply -pts1_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight2_sites/site_2/f2-lidar-pts1.ply

#*************************************************
#*********** Site 3 ******************************
#*************************************************


#*********** Flight 4 -> Flight 2 ****************

#1. Pick Correspondances using MeshLab Align tool
#2. Save correspondances as a bwm correspondance file format
#3. Find transformation and transfom a point cloud using correspondances
# /Projects/vxl/bin/Release/contrib/brl/bbas/bwm/exe/bwm_3d_site_transform_points -corrs /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_3/f4-f2-corrs.txt -input_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_3/gauss_233_normals_pvn_99.ply -output_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_3/gauss_233_normals_pvn_99_f2_reg.ply -transform_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_3/f4-f2_Hs -pts0_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_3/f4-f2-pts0.ply -pts1_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_3/f4-f2-pts1.ply

#*********** Flight 5 -> Flight 4 ****************

#1. Pick Correspondances using MeshLab Align tool
#2. Save correspondances as a bwm correspondance file format
#3. Find transformation and transfom a point cloud using correspondances
# /Projects/vxl/bin/Release/contrib/brl/bbas/bwm/exe/bwm_3d_site_transform_points -corrs /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_3/f5-f4-corrs.txt -input_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_3/gauss_233_normals_pvn_99.ply -output_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_3/gauss_233_normals_pvn_99_f4_reg.ply -transform_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_3/f5-f4_Hs -pts0_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_3/f5-f4-pts0.ply -pts1_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_3/f5-f4-pts1.ply

#*********** Flight 2 -> LIDAR ****************

#1. Pick Correspondances using MeshLab Align tool
#2. Save correspondances as a bwm correspondance file format
#3. Find transformation and transfom a point cloud using correspondances
/Projects/vxl/bin/Release/contrib/brl/bbas/bwm/exe/bwm_3d_site_transform_points -corrs /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight2_sites/site_3/f2-lidar-corrs.txt -input_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight2_sites/site_3/gauss_233_normals_pvn_99.ply -output_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight2_sites/site_3/gauss_233_normals_pvn_99_geo_reg.ply -transform_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight2_sites/site_3/Hs_geo -pts0_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight2_sites/site_3/f2-lidar-pts0.ply -pts1_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight2_sites/site_3/f2-lidar-pts1.ply

#*************************************************
#*********** Site 4 ******************************
#*************************************************

#*********** Flight 4 -> Flight 2 ****************

#1. Pick Correspondances using MeshLab Align tool
#2. Save correspondances as a bwm correspondance file format
#3. Find transformation and transfom a point cloud using correspondances
# /Projects/vxl/bin/Release/contrib/brl/bbas/bwm/exe/bwm_3d_site_transform_points -corrs /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_4/f4-f2-corrs.txt -input_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_4/gauss_233_normals_pvn_99.ply -output_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_4/gauss_233_normals_pvn_99_f2_reg.ply -transform_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_4/f4-f2_Hs -pts0_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_4/f4-f2-pts0.ply -pts1_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_4/f4-f2-pts1.ply

#*********** Flight 5 -> Flight 4 ****************

#1. Pick Correspondances using MeshLab Align tool
#2. Save correspondances as a bwm correspondance file format
#3. Find transformation and transfom a point cloud using correspondances
# /Projects/vxl/bin/Release/contrib/brl/bbas/bwm/exe/bwm_3d_site_transform_points -corrs /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_4/f5-f4-corrs.txt -input_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_4/gauss_233_normals_pvn_99.ply -output_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_4/gauss_233_normals_pvn_99_f4_reg.ply -transform_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_4/f5-f4_Hs -pts0_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_4/f5-f4-pts0.ply -pts1_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_4/f5-f4-pts1.ply

#*********** Flight 2 -> LIDAR ****************

#1. Pick Correspondances using MeshLab Align tool
#2. Save correspondances as a bwm correspondance file format
#3. Find transformation and transfom a point cloud using correspondances
# /Projects/vxl/bin/Release/contrib/brl/bbas/bwm/exe/bwm_3d_site_transform_points -corrs /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight2_sites/site_4/f2-lidar-corrs.txt -input_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight2_sites/site_4/gauss_233_normals_pvn_99.ply -output_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight2_sites/site_4/gauss_233_normals_pvn_99_geo_reg.ply -transform_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight2_sites/site_4/Hs_geo -pts0_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight2_sites/site_4/f2-lidar-pts0.ply -pts1_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight2_sites/site_4/f2-lidar-pts1.ply

#*************************************************
#*********** Site 7 ******************************
#*************************************************

#*********** Flight 4 -> Flight 2 ****************

#1. Pick Correspondances using MeshLab Align tool
#2. Save correspondances as a bwm correspondance file format
#3. Find transformation and transfom a point cloud using correspondances
# /Projects/vxl/bin/Release/contrib/brl/bbas/bwm/exe/bwm_3d_site_transform_points -corrs /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_7/f4-f2-corrs.txt -input_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_7/gauss_233_normals_pvn_99.ply -output_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_7/gauss_233_normals_pvn_99_f2_reg.ply -transform_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_7/f4-f2_Hs -pts0_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_7/f4-f2-pts0.ply -pts1_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight4_sites/site_7/f4-f2-pts1.ply

#*********** Flight 5 -> Flight 4 ****************

#1. Pick Correspondances using MeshLab Align tool
#2. Save correspondances as a bwm correspondance file format
# #3. Find transformation and transfom a point cloud using correspondances
# /Projects/vxl/bin/Release/contrib/brl/bbas/bwm/exe/bwm_3d_site_transform_points -corrs /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_7/f5-f4-corrs.txt -input_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_7/gauss_233_normals_pvn_99.ply -output_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_7/gauss_233_normals_pvn_99_f4_reg.ply -transform_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_7/f5-f4_Hs -pts0_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_7/f5-f4-pts0.ply -pts1_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_7/f5-f4-pts1.ply

#*********** Flight 5 -> LIDAR ****************

#1. Pick Correspondances using MeshLab Align tool
#2. Save correspondances as a bwm correspondance file format
#3. Find transformation and transfom a point cloud using correspondances
# /Projects/vxl/bin/Release/contrib/brl/bbas/bwm/exe/bwm_3d_site_transform_points -corrs /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_7/f5-lidar-corrs.txt -input_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_7/gauss_233_normals_pvn_99.ply -output_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_7/gauss_233_normals_pvn_99_geo_reg.ply -transform_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_7/Hs_geo -pts0_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_7/f5-lidar-pts0.ply -pts1_path /Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_7/f5-lidar-pts1.ply

