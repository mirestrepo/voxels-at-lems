#!/bin/bash

#reference_aligment.sh 30 manual registrations of lidar to lidar
#to get a lower bound for the error


#1. Pick Correspondances using MeshLab Align tool
#2. Save correspondances as a bwm correspondance file format
#3. Find transformation and transfom a point cloud using correspondances

for ((i=4; i<5; i++ )) do
/Projects/vxl/bin/Release/contrib/brl/bbas/bwm/exe/bwm_3d_site_transform_points -corrs /data/lidar_providence/manual_error/corrs${i}.txt -transform_path /data/lidar_providence/manual_error/Hs${i}
done
