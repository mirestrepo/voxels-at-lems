#!/bin/bash
"""
Created on Dec 6, 2012

@author:Isabel Restrepo

Various visualizatons
"""
#----------------------------------------
# Visualize registration few results
#----------------------------------------

# root_dir="/Users/isa/Experiments/reg3d_eval/cvg_eo_data"
# cropped=true;
# basename_in="gauss_233_normals_pvn_cropped"
# percentile=90
# ./reg3d_cvg_scenes.py --root_dir $root_dir --site 7 --flight 4 --gt_flight 2 --vis_ia true --descriptor "FPFH" --n_iter 500 --cropped $cropped --basename_in $basename_in --percentile $percentile

#----------------------------------------
# Visualize intensity profiles
#----------------------------------------
flight=4
site=1
sceneroot=/Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight${flight}_sites/site_${site}
p3d_file=f4-f2-pts1.ply

./intensity_profile.py --sceneroot $sceneroot --points3d_file $sceneroot/$p3d_file