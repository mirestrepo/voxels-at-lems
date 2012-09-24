#!/bin/bash

# Apply a random similarity transfomation to a set of cameras

for trial in 6 7 8 9; do
  dir_in="/Users/isa/Experiments/reg3d_eval/downtown_dan/original"
  dir_out="/Users/isa/Experiments/reg3d_eval/downtown_dan/trial_$trial"
  cd /Projects/vpcl/bin_make/Release/bin
  ./transform_cameras_rand -in_dir $dir_in -out_dir $dir_out -dt 1000
  cd $dir_out
  ln -s ../original/imgs ./imgs
done

# for trial in 5 6 7 8 9; do
#   dir_in="/Users/isa/Experiments/reg3d_eval/downtown_dan/original"
#   dir_out="/Users/isa/Experiments/reg3d_eval/downtown_dan/trial_$trial"
#   cd $dir_out
#   ln -s ../original/imgs ./imgs
# done

# cd $dir_out
# ln -s ../original/imgs ./imgs

# for trial in 0 1 2; do
#   dir_in="/data/reg3d_eval/downtown_dan/original"
#   dir_out="/data/reg3d_eval/downtown_dan/pert_01_$trial"
#   cd $dir_out
#   ln -s ../original/imgs ./imgs
#   cp ../original/scene_info.xml ./scene_info.xml
# done


# LidarPreprocessor –np 10 -ooc 4000 -header 0 –o /data/lidar_providence/downtown.lidar –las /data/lidar_providence/downtown.las -lasOffset -299250 -4.63275e+06
# 


# LidarPreprocessor -o ~/Desktop/LidarViewerExamples/PtArena_test1.lidar -np 4096 -ooc 2000 -header 1 -c 30 0 0 -ascii 0 1 2 6 ~/Desktop/LidarViewerExamples/PtArena.txt

