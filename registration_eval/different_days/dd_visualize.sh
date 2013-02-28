#!/bin/bash
"""
Created on Dec 6, 2012

@author:Isabel Restrepo

Various visualizations
"""
#----------------------------------------
# Visualize registration few results
#----------------------------------------

root_dir="/Users/isa/Experiments/reg3d_eval"
iter=500;
sample_distance=1;
nsamples=6;
basename_in="gauss_233_normals_pvn_cropped"
percentile=99
descriptor="SHOT"
# descriptor="FPFH"
echo $compute_scale
#-------IA--------------
./dd_reg3d_main.py --root_dir $root_dir --site="downtown" --src_str "2011" --tgt_str "2006"  --descriptor $descriptor --n_iter $iter  --basename_in $basename_in --percentile $percentile --vis_icp --cropped --nsamples $nsamples --sample_distance $sample_distance



# ./dd_reg3d_main.py --root_dir $root_dir --site="BH" --src_str "CVG" --tgt_str "2006"  --descriptor $descriptor --n_iter $iter  --basename_in $basename_in --percentile $percentile --vis_ia --cropped --nsamples $nsamples --sample_distance $sample_distance --compute_scale --bound_scale --bound_percentile 20