#!/bin/bash
"""
Created on October 17, 2012

@author:Isabel Restrepo

Camera principal ray perturbation experiments for the Capitol scene
"""


#***********Camera perturbation experiments

#I. Process trials

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
# for trial in 0; do ./train_scenes.sh "capitol_dan" "trial" $trial "png" 15 2; done
# for trial in 1 2 3 4 5 6 7 8 9; do ./train_scenes.sh "capitol_dan" "trial" $trial "png" 15 2; done

#3. Compute normals and descriptors
# for trial in 0; do ./compute_geometry.sh "capitol_dan" "trial" $trial; done
# for trial in 1 2 3 4 5 6 7 8 9; do ./compute_geometry.sh "capitol_dan" "trial" $trial; done

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




