#!/bin/bash

#This file contains a series of steps for manual georegistration of a point-cloud from the PVM to LIDAR

####********DOWNTOWN************

##**1. Query some info from LIDAR -- in particular we are intersted in gathering the offset
# lasinfo  -i /data/lidar_providence/downtown.las #liblas
# lasinfo  -i /data/lidar_providence/downtown.las > /data/lidar_providence/downtown_info.txt  #liblas
# CalcLasRange /data/lidar_providence/downtown.las   #LidarViewer UCDavis
# CalcLasRange /data/lidar_providence/downtown.las  > /data/lidar_providence/downtown_range.txt  #LidarViewer UCDavis
# python ./compute_lidar_offset.py -i /data/lidar_providence/downtown.las

##**2. Process .las file -- demean and split to make it more manageble on MeshLab ...
# las2las  -i /data/lidar_providence/downtown.las -o /data/lidar_providence/downtown_offset.las --offset "-299250.005 -4632749.995 0.0" --split-mb 70

##**3. Convert to XYZ - now it can be viewed in MeshLab
# las2txt -i /data/lidar_providence/downtown_offset-1.las -o /data/lidar_providence/downtown_offset-1.xyz --delimiter " " --parse xyz --valid_only --keep-returns 1
# las2txt -i /data/lidar_providence/downtown_offset-2.las -o /data/lidar_providence/downtown_offset-2.xyz --delimiter " " --parse xyz --valid_only --keep-returns 1

##**4. Use MeshLab to crop ROI and export to ply

##**5. Convert ply to pcd
# python ../vpcl/vpcl_ply2pcd.py -i /data/lidar_providence/downtown_offset-1-financial.ply -o /data/lidar_providence/downtown_offset-1-financial.pcd -t "PointXYZ"

##**6. Display LIDAR and PVM using PCL viewer. At this point we can pick points. I manually changed the viewer code to print the values to screen.
# /Projects/pcl_dev/pcl/trunk/Release/bin/pcl_viewer.app/Contents/MacOS/pcl_viewer /data/lidar_providence/downtown_offset-1-financial.pcd --fc 0 255 0

# /Projects/pcl_dev/pcl/trunk/Release/bin/pcl_viewer.app/Contents/MacOS/pcl_viewer /Users/isa/Experiments/reg3d_eval/downtown_dan/original/gauss_233_normals_pvn_99_XYZ.pcd --fc 0 0 255

##**7. Save Correspondances as bwm_correspondences

##**8. Find transformation and transfom a point cloud using correspondances
# /Projects/vxl/bin/Release/contrib/brl/bbas/bwm/exe/bwm_3d_site_transform_points -corrs /data/lidar_providence/downtown_offset-1-financial-dan-corrs.txt -input_path /Users/isa/Experiments/reg3d_eval/downtown_dan/original/gauss_233_normals_pvn_99.ply -output_path /Users/isa/Experiments/reg3d_eval/downtown_dan/original/gauss_233_normals_pvn_99_XYZ_geo.ply -pts0_path /data/lidar_providence/downtown_offset-1-financial-dan-pts0.ply -pts1_path /data/lidar_providence/downtown_offset-1-financial-dan-pts1.ply


####********CAPITOL************

##**1. Query some info from LIDAR -- in particular we are intersted in gathering the offset
# lasinfo  -i /data/lidar_providence/capitol/19_02984634.las #liblas
# lasinfo  -i /data/lidar_providence/capitol/19_02984634.las > /data/lidar_providence/capitol/19_02984634_info.txt  #liblas
# CalcLasRange /data/lidar_providence/capitol/19_02984634.las   #LidarViewer UCDavis
# CalcLasRange /data/lidar_providence/capitol/19_02984634.las  > /data/lidar_providence/capitol/19_02984634_range.txt  #LidarViewer UCDavis
# python ./compute_lidar_offset.py -i /data/lidar_providence/capitol/19_02984634.las

##**2. Process .las file -- demean and split to make it more manageble on MeshLab ...
# las2las  -i /data/lidar_providence/capitol/19_02984634.las -o /data/lidar_providence/capitol/19_02984634_offset.las --offset "-299250.005 -4634249.995 0.0" --split-mb 70

##**3. Convert to XYZ - now it can be viewed in MeshLab
# las2txt -i /data/lidar_providence/capitol/19_02984634_offset-1.las -o /data/lidar_providence/capitol/19_02984634_offset-1.xyz --delimiter " " --parse xyz --valid_only --keep-returns 1
# las2txt -i /data/lidar_providence/capitol/19_02984634_offset-2.las -o /data/lidar_providence/capitol/19_02984634_offset-2.xyz --delimiter " " --parse xyz --valid_only --keep-returns 1

##**4. Use MeshLab to crop ROI and export to ply

##**5. Use MeshLab align tool to pick correspondances
#The align project gices the transfomation matrix. However, I need the corresponances to plot my fiducial errors.
#Meshlab outputs the picked points in the console - I manually put them in the corrs.txt file i bwm format's

##**7. Save Correspondances as bwm_correspondences

##**8. Find transformation and transfom a point cloud using correspondances
# /Projects/vxl/bin/Release/contrib/brl/bbas/bwm/exe/bwm_3d_site_transform_points -corrs /data/lidar_providence/capitol/capitol-dan-corrs.txt -input_path /Users/isa/Experiments/reg3d_eval/capitol_dan/original/gauss_233_normals_pvn_99.ply -output_path /Users/isa/Experiments/reg3d_eval/capitol_dan/original/gauss_233_normals_pvn_99_XYZ_geo.ply -pts0_path /data/lidar_providence/capitol/capitol-dan-pts0.ply -pts1_path /data/lidar_providence/capitol/capitol-dan-pts1.ply


####********SciLi************

##**1. Query some info from LIDAR -- in particular we are intersted in gathering the offset
# lasinfo  -i /data/lidar_providence/east_side/19_03004632.las #liblas
# lasinfo  -i /data/lidar_providence/east_side/19_03004632.las > /data/lidar_providence/east_side/19_03004632_info.txt  #liblas
# CalcLasRange /data/lidar_providence/east_side/19_03004632.las   #LidarViewer UCDavis
# CalcLasRange /data/lidar_providence/east_side/19_03004632.las  > /data/lidar_providence/east_side/19_03004632_range.txt  #LidarViewer UCDavis
# python ./compute_lidar_offset.py -i /data/lidar_providence/east_side/19_03004632.las

##**2. Process .las file -- demean and split to make it more manageble on MeshLab ...
# las2las  -i /data/lidar_providence/east_side/19_03004632.las -o /data/lidar_providence/east_side/19_03004632_offset.las --offset "-300750.005 -4632749.995 0.0" --split-mb 70

##**3. Convert to XYZ - now it can be viewed in MeshLab
# las2txt -i /data/lidar_providence/east_side/19_03004632_offset-1.las -o /data/lidar_providence/east_side/19_03004632_offset-1.xyz --delimiter " " --parse xyz --valid_only --keep-returns 1
# las2txt -i /data/lidar_providence/east_side/19_03004632_offset-2.las -o /data/lidar_providence/east_side/19_03004632_offset-2.xyz --delimiter " " --parse xyz --valid_only --keep-returns 1

##**4. Use MeshLab to crop ROI and export to ply

##**5. Use MeshLab align tool to pick correspondances
#The align project gices the transfomation matrix. However, I need the corresponances to plot my fiducial errors.
#Meshlab outputs the picked points in the console - I manually put them in the corrs.txt file i bwm format's

##**7. Save Correspondances as bwm_correspondences

##**8. Find transformation and transfom a point cloud using correspondances
/Projects/vxl/bin/Release/contrib/brl/bbas/bwm/exe/bwm_3d_site_transform_points -corrs /data/lidar_providence/east_side/scili_3_12-corrs.txt -input_path /Users/isa/Experiments/reg3d_eval/scili_3_12/original/gauss_233_normals_pvn_99.ply -output_path /Users/isa/Experiments/reg3d_eval/scili_3_12/original/gauss_233_normals_pvn_99_XYZ_geo.ply -pts0_path /data/lidar_providence/east_side/scili_3_12-pts0.ply -pts1_path /data/lidar_providence/east_side/scili_3_12-pts1.ply
