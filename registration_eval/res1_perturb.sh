#!/bin/bash
"""
Created on December 17, 2012

@author:Isabel Restrepo

Camera PerturbationExperiments for Residential1 = East Side

"""

#***********Discretization experiments

#1. Generate trials

# Apply a random similarity transfomation to a set of cameras

# root_dir="/Users/isa/Experiments/reg3d_eval/res_east_side"
# python reg3d_main_pert.py --root_dir $root_dir --perturb true


# for trial in 0 1 2 3 4 5 6 7 8 9; do
#   dir_out="/Users/isa/Experiments/reg3d_eval/res_east_side/pert_005_$trial"
#   cd $dir_out
#   ln -s ../original/imgs ./imgs
#   cp ../original/scene_info.xml ./scene_info.xml


#   dir_out="/Users/isa/Experiments/reg3d_eval/res_east_side/pert_01_$trial"
#   cd $dir_out
#   ln -s ../original/imgs ./imgs
#   cp ../original/scene_info.xml ./scene_info.xml


#   dir_out="/Users/isa/Experiments/reg3d_eval/res_east_side/pert_015_$trial"
#   cd $dir_out
#   ln -s ../original/imgs ./imgs
#   cp ../original/scene_info.xml ./scene_info.xml
# done


#2. Train the scene
# for trial in 0 1 2 3 4 5 6 7 8 9; do ./train_scenes.sh "res_east_side" "pert_005" $trial "png" 27 1; done
# for trial in 0 1 2 3 4 5 6 7 8 9; do ./train_scenes.sh "res_east_side" "pert_01" $trial "png" 27 1; done
# for trial in 0 1 2 3 4 5 6 7 8 9; do ./train_scenes.sh "res_east_side" "pert_015" $trial "png" 27 1; done


#3. Compute normals and descriptors
for trial in 0 1 2 3 4 5 6 7 8 9; do ./compute_geometry.sh "res_east_side" "pert_005" $trial; done
# for trial in 0 1 2 3 4 5 6 7 8 9; do ./compute_geometry.sh "res_east_side" "pert_01" $trial; done
# for trial in 0 1 2 3 4 5 6 7 8 9; do ./compute_geometry.sh "res_east_side" "pert_015" $trial; done

#4. Register
# for iter in 20 50 75 100 200 500; do

#   n_iter_ia=$iter;
#   n_iter_icp=$iter;
#   root_dir="/Users/isa/Experiments/reg3d_eval/res_east_side"
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

#5. Visualize few results
# root_dir="/Users/isa/Experiments/reg3d_eval/res_east_side"
# t_basename="trial"
# ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial 5 --vis_ia true --descriptor "FPFH" --n_iter 500
# ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial 5 --vis_ia true --descriptor "SHOT" --n_iter 500
# ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial 5 --vis_icp true --descriptor "FPFH" --n_iter 500
# ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial 5 --vis_icp true --descriptor "SHOT" --n_iter 500

#6. Report results




