#!/bin/bash
"""
Created on October 20, 2012

@author:Isabel Restrepo

Experiments for cvg data (variation in illumination)
"""

#*******************************************************
#I. Set up the scene files and model directories

#1. Read bundler output and output imgs/ cams_krt/ and model/
# for flight in 2; do
#     for site in 2 3 4 7; do
#         ./set_up_cvg_scenes.sh $flight $site
#     done
# done

# for flight in 4; do
#     for site in 1 2 3 4 5 7; do
#         ./set_up_cvg_scenes.sh $flight $site &
#     done
# done

# wait

# for flight in 5; do
#     for site in 1 2 3 4 5 7; do
#         ./set_up_cvg_scenes.sh $flight $site &
#     done
# done
# wait


#2. Use matlab to plot the points and cameras

#3. Manually assemble a scene.xml

#*******************************************************
#II Train scenes

# for flight in 2; do
#     for site in 1 2 3 4 7; do
#         ./train_cvg_scenes.sh $flight $site 17 2
#     done
# done

# for flight in 4; do
#     for site in 2; do
#         ./train_cvg_scenes.sh $flight $site 17 2
#     done
# done

# for flight in 5; do
#     for site in 5; do
#         ./train_cvg_scenes.sh $flight $site 17 2
#     done
# done
#*******************************************************
#II Compute Normals and extract geometry

# for flight in 2; do
#     for site in 2; do
#         ./cvg_compute_geometry.sh $flight $site
#     done
# done

# for flight in 4; do
#     for site in 2; do
#         ./cvg_compute_geometry.sh $flight $site
#     done
# done

for flight in 5; do
    for site in 5; do
        ./cvg_compute_geometry.sh $flight $site
    done
done

#*******************************************************
#II Register
# for iter in 500; do

#   n_iter_ia=$iter;
#   n_iter_icp=$iter;
#   root_dir="/Users/isa/Experiments/reg3d_eval/cvg_eo_data"
#   cropped=true;
#   basename_in="gauss_233_normals_pvn_cropped"
#   echo "Running iteration: "
#   echo $iter
#   percentile=90

#   for site in 1 2 3 4 7; do
#     ./reg3d_cvg_scenes.py --root_dir $root_dir --site $site --flight 5 --gt_flight 4 --reg_ia true --descriptor "SHOT" --n_iter $n_iter_ia --cropped $cropped --basename_in $basename_in --percentile $percentile &
#     ./reg3d_cvg_scenes.py --root_dir $root_dir --site $site --flight 5 --gt_flight 2 --reg_ia true --descriptor "SHOT" --n_iter $n_iter_ia --cropped $cropped --basename_in $basename_in --percentile $percentile &
#     ./reg3d_cvg_scenes.py --root_dir $root_dir --site $site --flight 4 --gt_flight 2 --reg_ia true --descriptor "SHOT" --n_iter $n_iter_ia --cropped $cropped --basename_in $basename_in --percentile $percentile &
#     ./reg3d_cvg_scenes.py --root_dir $root_dir --site $site --flight 5 --gt_flight 4 --reg_ia true --descriptor "FPFH" --n_iter $n_iter_ia --cropped $cropped --basename_in $basename_in --percentile $percentile &
#     ./reg3d_cvg_scenes.py --root_dir $root_dir --site $site --flight 5 --gt_flight 2 --reg_ia true --descriptor "FPFH" --n_iter $n_iter_ia --cropped $cropped --basename_in $basename_in --percentile $percentile &
#     ./reg3d_cvg_scenes.py --root_dir $root_dir --site $site --flight 4 --gt_flight 2 --reg_ia true --descriptor "FPFH" --n_iter $n_iter_ia --cropped $cropped --basename_in $basename_in --percentile $percentile &
#     wait
#   done

#   for site in 1 2 3 4 7; do
#     ./reg3d_cvg_scenes.py --root_dir $root_dir --site $site --flight 5 --gt_flight 4 --reg_icp true --descriptor "SHOT" --n_iter $n_iter_ia --cropped $cropped --basename_in $basename_in --percentile $percentile &
#     ./reg3d_cvg_scenes.py --root_dir $root_dir --site $site --flight 5 --gt_flight 2 --reg_icp true --descriptor "SHOT" --n_iter $n_iter_ia --cropped $cropped --basename_in $basename_in --percentile $percentile &
#     ./reg3d_cvg_scenes.py --root_dir $root_dir --site $site --flight 4 --gt_flight 2 --reg_icp true --descriptor "SHOT" --n_iter $n_iter_ia --cropped $cropped --basename_in $basename_in --percentile $percentile &
#     ./reg3d_cvg_scenes.py --root_dir $root_dir --site $site --flight 5 --gt_flight 4 --reg_icp true --descriptor "FPFH" --n_iter $n_iter_ia --cropped $cropped --basename_in $basename_in --percentile $percentile &
#     ./reg3d_cvg_scenes.py --root_dir $root_dir --site $site --flight 5 --gt_flight 2 --reg_icp true --descriptor "FPFH" --n_iter $n_iter_ia --cropped $cropped --basename_in $basename_in --percentile $percentile &
#     ./reg3d_cvg_scenes.py --root_dir $root_dir --site $site --flight 4 --gt_flight 2 --reg_icp true --descriptor "FPFH" --n_iter $n_iter_ia --cropped $cropped --basename_in $basename_in --percentile $percentile &
#     wait
#   done

# done


#ICP

# for iter in 500 700 1000; do

#   n_iter_ia=$iter;
#   n_iter_icp=$iter;
#   root_dir="/Users/isa/Experiments/reg3d_eval/cvg_eo_data"


# #   echo $iter

#   # for site in 1; do
#   #   # ./reg3d_cvg_scenes.py --root_dir $root_dir --site $site --flight 5 --gt_flight 4 --reg_icp true --descriptor "FPFH" --n_iter $n_iter_ia &
#   #   # ./reg3d_cvg_scenes.py --root_dir $root_dir --site $site --flight 5 --gt_flight 2 --reg_icp true --descriptor "FPFH" --n_iter $n_iter_ia &
#   #   # ./reg3d_cvg_scenes.py --root_dir $root_dir --site $site --flight 4 --gt_flight 2 --reg_icp true --descriptor "FPFH" --n_iter $n_iter_ia &
#   # done
#   # wait


# done

#*******************************************************
#5. Visualize few results
# root_dir="/Users/isa/Experiments/reg3d_eval/cvg_eo_data"
# ./reg3d_cvg_scenes.py --root_dir $root_dir --site 1 --flight 5 --gt_flight 4 --vis_ia true --descriptor "FPFH" --n_iter 500

