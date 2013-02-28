
#!/bin/bash
"""
Created on October 17, 2012

@author:Isabel Restrepo

Experiments for the Capitol scene
"""


#***********Discretization experiments

#I. Process original scene

#1. Used the scene from BMVC12 experiments

#II. Process lidar - refer to scili_3_12_lidar.sh

#III. Process trials

#1. Generate trials

# Apply a random similarity transfomation to a set of cameras

# base_dir="/Users/isa/Experiments/reg3d_eval/scili_3_12"
# cd /Projects/vpcl/bin_make/Release/bin
# ./transform_cameras_rand -base_dir $base_dir -dt 1 -nt 10

# for trial in 0 1 2 3 4 5 6 7 8 9; do
#   dir_out="/Users/isa/Experiments/reg3d_eval/scili_3_12/trial_$trial"
#   cd $dir_out
#   ln -s ../original/imgs ./imgs
# done

#2. Train the scene 15 refine chuncks 2 iterations
# for trial in 0 1 2 3 4 5 6 7 8 9; do ./train_scenes.sh "scili_3_12" "trial" $trial "png" 25 1; done

#3. Compute normals and descriptors
# for trial in 0 1 2 3 4 5 6 7 8 9; do ./compute_geometry.sh "scili_3_12" "trial" $trial; done

# 4. Register
for iter in 20 50 75 100 200 500; do

  n_iter_ia=$iter;
  n_iter_icp=$iter;
  root_dir="/Users/isa/Experiments/reg3d_eval/scili_3_12"
  t_basename="trial"


  echo $iter

  for t in 0 1 2 3 4 5 6 7 8 9; do
    ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_ia true --descriptor "FPFH" --n_iter $n_iter_ia &
  done
  wait

  for t in 0 1 2 3 4 5 6 7 8 9; do
    ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_icp true --descriptor "FPFH" --n_iter $n_iter_icp &
  done
  wait

  for t in 0 1 2 3 4 5 6 7 8 9; do
    ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_ia true --descriptor "SHOT" --n_iter $n_iter_ia &
  done
  wait

  for t in 0 1 2 3 4 5 6 7 8 9; do
    ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_icp true --descriptor "SHOT" --n_iter $n_iter_icp &
  done
  wait

done

#5. Visualize few results
# root_dir="/Users/isa/Experiments/reg3d_eval/scili_3_12"
# t_basename="trial"
# ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial 5 --vis_ia true --descriptor "FPFH" --n_iter 500
# ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial 2 --vis_ia true --descriptor "SHOT" --n_iter 500
# ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial 2 --vis_icp true --descriptor "FPFH" --n_iter 500
# ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial 2 --vis_icp true --descriptor "SHOT" --n_iter 500


