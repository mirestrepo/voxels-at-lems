#!/bin/bash

# for iter in 20 500; do

#   n_iter_ia=$iter;
#   n_iter_icp=$iter;
#   root_dir="/Users/isa/Experiments/reg3d_eval/downtown_dan"
#   t_basename="pert_015"
#   # root_dir="/Users/isa/Experiments/reg3d_eval/capitol_dan"


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
#     ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_icp true --descriptor "FPFH" --rej_normals true --n_iter $n_iter_icp &
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
#   for t in 0 1 2 3 4 5 6 7 8 9; do
#     ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_icp true --descriptor "SHOT" --rej_normals true --n_iter $n_iter_icp &
#   done
#   wait

# done

for iter in 500; do

  n_iter_ia=$iter;
  n_iter_icp=$iter;
  root_dir="/Users/isa/Experiments/reg3d_eval/downtown_dan"
  t_basename="pert_005"
  # root_dir="/Users/isa/Experiments/reg3d_eval/capitol_dan"


  echo $iter

  for t in 3 4 5 6 7 8 9; do
    ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_ia true --descriptor "FPFH" --n_iter $n_iter_ia &
  done
  wait

  for t in 3 4 5 6 7 8 9; do
    ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_icp true --descriptor "FPFH" --n_iter $n_iter_icp &
  done
  wait
  for t in 3 4 5 6 7 8 9; do
    ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_icp true --descriptor "FPFH" --rej_normals true --n_iter $n_iter_icp &
  done
  wait

  for t in 3 4 5 6 7 8 9; do
    ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_ia true --descriptor "SHOT" --n_iter $n_iter_ia &
  done
  wait

  for t in 3 4 5 6 7 8 9; do
    ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_icp true --descriptor "SHOT" --n_iter $n_iter_icp &
  done
  wait
  for t in 3 4 5 6 7 8 9; do
    ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_icp true --descriptor "SHOT" --rej_normals true --n_iter $n_iter_icp &
  done
  wait

done

# for iter in 500; do

#   n_iter_ia=$iter;
#   n_iter_icp=$iter;
#   root_dir="/Users/isa/Experiments/reg3d_eval/downtown_dan"
#   t_basename="pert_01"
#   # root_dir="/Users/isa/Experiments/reg3d_eval/capitol_dan"


#   echo $iter

#   for t in 3 4 5 6 7 8 9; do
#     ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_ia true --descriptor "FPFH" --n_iter $n_iter_ia &
#   done
#   wait

#   for t in 3 4 5 6 7 8 9; do
#     ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_icp true --descriptor "FPFH" --n_iter $n_iter_icp &
#   done
#   wait
#   for t in 3 4 5 6 7 8 9; do
#     ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_icp true --descriptor "FPFH" --rej_normals true --n_iter $n_iter_icp &
#   done
#   wait

#   for t in 3 4 5 6 7 8 9; do
#     ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_ia true --descriptor "SHOT" --n_iter $n_iter_ia &
#   done
#   wait

#   for t in 3 4 5 6 7 8 9; do
#     ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_icp true --descriptor "SHOT" --n_iter $n_iter_icp &
#   done
#   wait
#   for t in 3 4 5 6 7 8 9; do
#     ./reg3d_main.py --root_dir $root_dir --t_basename $t_basename --trial $t --reg_icp true --descriptor "SHOT" --rej_normals true --n_iter $n_iter_icp &
#   done
#   wait

# done


# python ./compute_transformation_error.py --log "/Users/isa/Experiments/reg3d_eval/downtown_dan/plot_RT.log"

# for t in 0 1 2 3 4 5 6 7 8 9; do
#   python ../vpcl/vpcl_ply2pcd.py -i /Users/isa/Experiments/reg3d_eval/downtown_dan/trial_${t}/gauss_233_points_pvn_99_XYZ_geo.ply -o /Users/isa/Experiments/reg3d_eval/downtown_dan/trial_${t}/gauss_233_points_pvn_99_XYZ_geo.pcd -t "PointXYZ"
# done