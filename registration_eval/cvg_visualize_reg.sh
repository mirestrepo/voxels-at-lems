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
percentile=90
./reg3d_cvg_scenes.py --root_dir $root_dir --site 7 --flight 4 --gt_flight 2 --vis_ia true --descriptor "FPFH" --n_iter 500 --cropped $cropped --basename_in $basename_in --percentile $percentile

