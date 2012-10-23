#II. Process lidar

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
# /Projects/vxl/bin/Release/contrib/brl/bbas/bwm/exe/bwm_3d_site_transform_points -corrs /data/lidar_providence/capitol/capitol-dan-corrs.txt -input_path /Users/isa/Experiments/reg3d_eval/capitol_dan/original/gauss_233_normals_pvn_99.ply -output_path /Users/isa/Experiments/reg3d_eval/capitol_dan/original/gauss_233_normals_pvn_99_XYZ_geo.ply -transform_path /data/lidar_providence/capitol/capitol-dan_Hs -pts0_path /data/lidar_providence/capitol/capitol-dan-pts0.ply -pts1_path /data/lidar_providence/capitol/capitol-dan-pts1.ply
