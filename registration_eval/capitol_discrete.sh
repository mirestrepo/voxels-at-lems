#!/bin/bash
"""
Created on October 17, 2012

@author:Isabel Restrepo

Discretezation Experiments for the Capitol scene
"""


#***********Discretization experiments

#I. Process original scene

#1. train the scene 15 refine chuncks 2 iterations
# ./train_scenes.sh "capitol_dan" "png" 15 2

#2. Compute normas and descriptors
# ./compute_geometry.sh "capitol_dan"

#II. Process lidar

##**1. Query some info from LIDAR -- in particular we are intersted in gathering the offset
# lasinfo  -i /data/lidar_providence/capitol/19_02984634.las #liblas
# lasinfo  -i /data/lidar_providence/capitol/19_02984634.las > /data/lidar_providence/capitol/19_02984634_info.txt  #liblas
# CalcLasRange /data/lidar_providence/capitol/19_02984634.las   #LidarViewer UCDavis
# CalcLasRange /data/lidar_providence/capitol/19_02984634.las  > /data/lidar_providence/capitol/19_02984634_range.txt  #LidarViewer UCDavis
# python ./compute_lidar_offset.py -i /data/lidar_providence/capitol/19_02984634.las

##**2. Process .las file -- demean and split to make it more manageble on MeshLab ...
# las2las  -i /data/lidar_providence/capitol/19_02984634.las -o /data/lidar_providence/capitol/19_02984634_offset.las --offset "-299250.005 -4634249.995 0.0" --split-mb 70

##**3. Convert to XYZ - now it can be viewed in MeshLab
# las2txt -i /data/lidar_providence/capitol/19_02984634_offset-1.las -o /data/lidar_providence/capitol/19_02984634_offset-1.xyz --delimiter " " --parse xyz --valid_only --keep-returns 1
# las2txt -i /data/lidar_providence/capitol/19_02984634_offset-2.las -o /data/lidar_providence/capitol/19_02984634_offset-2.xyz --delimiter " " --parse xyz --valid_only --keep-returns 1

##**4. Use MeshLab to crop ROI and export to ply

##**5. Use MeshLab align tool to pick correspondances
#The align project gices the transfomation matrix. However, I need the corresponances to plot my fiducial errors.
#Meshlab outputs the picked points in the console - I manually put them in the corrs.txt file i bwm format's

##**7. Save Correspondances as bwm_correspondences

##**8. Find transformation and transfom a point cloud using correspondances
# /Projects/vxl/bin/Release/contrib/brl/bbas/bwm/exe/bwm_3d_site_transform_points -corrs /data/lidar_providence/capitol/capitol-dan-corrs.txt -input_path /Users/isa/Experiments/reg3d_eval/capitol_dan/original/gauss_233_normals_pvn_99.ply -output_path /Users/isa/Experiments/reg3d_eval/capitol_dan/original/gauss_233_normals_pvn_99_XYZ_geo.ply -transform_path /data/lidar_providence/capitol/capitol-dan_Hs -pts0_path /data/lidar_providence/capitol/capitol-dan-pts0.ply -pts1_path /data/lidar_providence/capitol/capitol-dan-pts1.ply

#III. Process trials

#1. Generate trials

# Apply a random similarity transfomation to a set of cameras

# for trial in 0 1 2 3 4 5 6 7 8 9; do
#   dir_in="/Users/isa/Experiments/reg3d_eval/capitol_dan/original"
#   dir_out="/Users/isa/Experiments/reg3d_eval/capitol_dan/trial_$trial"
#   cd /Projects/vpcl/bin_make/Release/bin
#   ./transform_cameras_rand -in_dir $dir_in -out_dir $dir_out -dt 1
#   cd $dir_out
#   ln -s ../original/imgs ./imgs
# done

#2. Train the scene 15 refine chuncks 2 iterations
# for trial in 0; do ./train_scenes.sh "capitol_dan" "trial" $trial "png" 15 1; done
# for trial in 1 2 3 4 5 6 7 8 9; do ./train_scenes.sh "capitol_dan" "trial" $trial "png" 15 2; done

#3. Compute normals and descriptors
# for trial in 0; do ./compute_geometry.sh "capitol_dan" "trial" $trial; done
for trial in 1 2 3 4 5 6 7 8 9; do ./compute_geometry.sh "capitol_dan" "trial" $trial; done

#4. Register
# for iter in 20 50 75 100 200 500; do

#   n_iter_ia=$iter;
#   n_iter_icp=$iter;
#   root_dir="/Users/isa/Experiments/reg3d_eval/capitol_dan"
#   t_basename="trial"


#   echo $iter

#   for t in 0 1 2 3 4 5 6 7 8 9; do
#     ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_ia true --descriptor "FPFH" --n_iter $n_iter_ia &
#   done
#   wait

#   for t in 0 1 2 3 4 5 6 7 8 9; do
#     ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_icp true --descriptor "FPFH" --n_iter $n_iter_icp &
#   done
#   wait

#   for t in 0 1 2 3 4 5 6 7 8 9; do
#     ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_ia true --descriptor "SHOT" --n_iter $n_iter_ia &
#   done
#   wait

#   for t in 0 1 2 3 4 5 6 7 8 9; do
#     ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_icp true --descriptor "SHOT" --n_iter $n_iter_icp &
#   done
#   wait

# done

#5. Report results




