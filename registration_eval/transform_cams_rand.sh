#!/bin/bash

# Apply a random similarity transfomation to a set of cameras

#dir_in="/data/reg3d_eval/downtown_dan/original"
#dir_out="/data/reg3d_eval/downtown_dan/trial_2"
#cd /Projects/vpcl/bin_make/Release/bin
#./transform_cameras_rand -in_dir $dir_in -out_dir $dir_out -dt 1000
#
#cd $dir_out
#ln -s ../original/imgs ./imgs

for trial in 0 1 2; do
  dir_in="/data/reg3d_eval/downtown_dan/original"
  dir_out="/data/reg3d_eval/downtown_dan/pert_01_$trial"
  cd $dir_out
  ln -s ../original/imgs ./imgs
  cp ../original/scene_info.xml ./scene_info.xml
done