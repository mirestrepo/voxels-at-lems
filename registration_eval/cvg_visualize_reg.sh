#!/bin/bash
"""
Created on Dec 6, 2012

@author:Isabel Restrepo

Visualizaton for registration of cvg data (variation in illumination)
"""

# Visualize few results
root_dir="/Users/isa/Experiments/reg3d_eval/cvg_eo_data"
cropped=true;
basename_in="gauss_233_normals_pvn_cropped"
percentile=95
./reg3d_cvg_scenes.py --root_dir $root_dir --site 2 --flight 5 --gt_flight 4 --vis_icp true --descriptor "FPFH" --n_iter 500 --cropped $cropped --basename_in $basename_in --percentile $percentile

