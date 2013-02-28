#!/bin/bash
"""
Created on Jan 10, 2013

@author:Isabel Restrepo

Register different days Experiments
"""


##*******************************************************
## Register IA
for bound_percentile in 20 10 5; do

    for sample_distance in 10 5 1; do

        for nsamples in 10 6 3; do

            iter=500;
            n_iter_ia=$iter;
            n_iter_icp=$iter;
            cropped=true;
            basename_in="gauss_233_normals_pvn_cropped"
            echo "Running iteration: "
            echo $iter
            percentile=99
            root_dir="/Users/isa/Experiments/reg3d_eval"

            #*******************************************************
            #  B.H
            #*******************************************************
            site="BH"
            # -------IA--------------
            ./dd_reg3d_main.py --root_dir $root_dir --site=$site --tgt_str "2006" --src_str "CVG" --reg_icp --descriptor "SHOT" --n_iter $n_iter_ia  --basename_in $basename_in --percentile $percentile --nsamples $nsamples --sample_distance $sample_distance --cropped --compute_scale --bound_scale --bound_percentile $bound_percentile &
            ./dd_reg3d_main.py --root_dir $root_dir --site=$site --tgt_str "2006" --src_str "CVG" --reg_icp --descriptor "FPFH" --n_iter $n_iter_ia  --basename_in $basename_in --percentile $percentile --nsamples $nsamples --sample_distance $sample_distance --cropped --compute_scale --bound_scale --bound_percentile $bound_percentile &

            #*******************************************************
            #  Capitol
            #*******************************************************
            #-------IA--------------
            site=Capitol
            ./dd_reg3d_main.py --root_dir $root_dir --site $site --src_str "2011" --tgt_str "2006" --reg_icp --descriptor "SHOT" --n_iter $n_iter_ia --basename_in $basename_in --percentile $percentile --nsamples $nsamples --sample_distance $sample_distance --cropped --compute_scale --bound_scale --bound_percentile $bound_percentile  &
            ./dd_reg3d_main.py --root_dir $root_dir --site $site --src_str "2011" --tgt_str "2006" --reg_icp --descriptor "FPFH" --n_iter $n_iter_ia --basename_in $basename_in --percentile $percentile --nsamples $nsamples --sample_distance $sample_distance --cropped --compute_scale --bound_scale --bound_percentile $bound_percentile  &
            ./dd_reg3d_main.py --root_dir $root_dir --site $site --src_str "2006" --tgt_str "2011" --reg_icp --descriptor "SHOT" --n_iter $n_iter_ia --basename_in $basename_in --percentile $percentile --nsamples $nsamples --sample_distance $sample_distance --cropped --compute_scale --bound_scale --bound_percentile $bound_percentile &
            ./dd_reg3d_main.py --root_dir $root_dir --site $site --src_str "2006" --tgt_str "2011" --reg_icp --descriptor "FPFH" --n_iter $n_iter_ia --basename_in $basename_in --percentile $percentile --nsamples $nsamples --sample_distance $sample_distance --cropped --compute_scale --bound_scale --bound_percentile $bound_percentile &

            wait
        done
    done
done



