#!/bin/bash
"""
Created on October 17, 2012

@author:Isabel Restrepo

Discretization Experiments for the Downtown scene
"""


#***********Discretization experiments

#I. Process original scene

#1. train the scene 15 refine chuncks 2 iterations
# ./train_scenes.sh "downtown_dan" "png" 15 2

#2. Compute normas and descriptors
# ./compute_geometry.sh "downtown_dan"

#II. Process lidar - refer to ./capitol_lidar.sh

#III. Process trials

#1. Generate trials

# Apply a random similarity transfomation to a set of cameras

# base_dir="/Users/isa/Experiments/reg3d_eval/downtown_dan"
# cd /Projects/vpcl/bin_make/Release/bin
# ./transform_cameras_rand -base_dir $base_dir -dt 1 -nt 10

# for trial in 0 1 2 3 4 5 6 7 8 9; do
#   dir_out="/Users/isa/Experiments/reg3d_eval/downtown_dan/trial_$trial"
#   cd $dir_out
#   ln -s ../original/imgs ./imgs
# done

#2. Train the scenes
# for trial in 8; do ./train_scenes.sh "downtown_dan" "trial" $trial "tif" 15 2; done
# for trial in 0 1 2 3 4 5 6 7 8 9; do ./train_scenes.sh "downtown_dan" "trial" $trial "tif" 10 3; done

#3. Compute normals and descriptors
# for trial in 8; do ./compute_geometry.sh "downtown_dan" "trial" $trial; done
# for trial in 0 1 2 3 4 5 6 7 8 9; do ./compute_geometry.sh "downtown_dan" "trial" $trial; done

#4. Register
# for iter in 20 50 75 100 200 500; do

#   n_iter_ia=$iter;
#   n_iter_icp=$iter;
#   root_dir="/Users/isa/Experiments/reg3d_eval/downtown_dan"
#   t_basename="trial"


#   echo $iter

#   for t in 8; do
#     ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_ia true --descriptor "FPFH" --n_iter $n_iter_ia &
#   done
#   wait

#   for t in 8; do
#     ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_icp true --descriptor "FPFH" --n_iter $n_iter_icp &
#   done
#   wait

#   for t in 8; do
#     ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_ia true --descriptor "SHOT" --n_iter $n_iter_ia &
#   done
#   wait

#   for t in 8; do
#     ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_icp true --descriptor "SHOT" --n_iter $n_iter_icp &
#   done
#   wait

# done


for t in 8; do


  root_dir="/Users/isa/Experiments/reg3d_eval/downtown_dan"
  t_basename="trial"


  for iter in 20 50 75 100 200 500; do
    n_iter_ia=$iter;
    ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_ia true --descriptor "FPFH" --n_iter $n_iter_ia &
    ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_ia true --descriptor "SHOT" --n_iter $n_iter_ia &
  done
  wait

  for iter in 20 50 75 100 200 500; do
    n_iter_icp=$iter;
    ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_icp true --descriptor "FPFH" --n_iter $n_iter_icp &
    ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_icp true --descriptor "SHOT" --n_iter $n_iter_icp &
  done
  wait

done

#5. Visualize few results
# root_dir="/Users/isa/Experiments/reg3d_eval/downtown_dan"
# t_basename="trial"
# ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial 5 --vis_ia true --descriptor "FPFH" --n_iter 500
# ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial 5 --vis_ia true --descriptor "SHOT" --n_iter 500
# ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial 5 --vis_icp true --descriptor "FPFH" --n_iter 500
# ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial 5 --vis_icp true --descriptor "SHOT" --n_iter 500

#6. Report results




