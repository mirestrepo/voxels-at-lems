import sys
import os
sys.path.append(os.pardir)

import reg3d_transformations as reg3d_T
from numpy import linalg as LA
import transformations as tf



#******************** BH ********************

# cvg_root = "/Users/isa/Experiments/reg3d_eval/cvg_eo_data"
# dan_root = "/Users/isa/Experiments/reg3d_eval/BH_2006/original"

# Paper with Vishal
vsi_root = "/Users/isa/Dropbox/MultiModalRegPaper/ground_truth/aerial-lidar/BH_VSI"
dan_root = "/Users/isa/Dropbox/MultiModalRegPaper/ground_truth/aerial-lidar/BH_2006"


# # #Load f2-lidar
# f2_lidar_file = cvg_root + "/flight2_sites/site_1/Hs_geo.txt"
# f2_geo = reg3d_T.geo_transformation(f2_lidar_file)


# #Load f4-f2
# f4_f2_file = cvg_root + "/flight4_sites/site_1/f4-f2_Hs.txt"
# f4_f2 = reg3d_T.gt_transformation(f4_f2_file)

# #Load f4-2006
# f4_2006_file = cvg_root + "/flight4_sites/site_1/f4-2006_Hs.txt"
# f4_2006 = reg3d_T.gt_transformation(f4_2006_file)

# #Load cvg-f4-2006
# f4_2006_file = cvg_root + "/flight4_sites/site_1/f4-2006_Hs.txt"
# f4_2006 = reg3d_T.gt_transformation(f4_2006_file)

#Load vsi-2006 this is only used for vishal's paper set up
f4_dan_file = vsi_root + "/vsi-2006_Hs.txt"
f4_dan = reg3d_T.gt_transformation(f4_dan_file)
dan_lidar_file = dan_root + "/Hs_geo.txt"
dan_geo = reg3d_T.geo_transformation(dan_lidar_file)
vsi_geo_Hs = dan_geo.Hs_geo.dot(f4_dan.Hs)
vsi_geo = reg3d_T.gt_transformation(vsi_geo_Hs)
vsi_geo.save_to_file(vsi_root + "/Hs_geo.txt")


# #Compute missing ones
# #2006-lidar
# dan_geo_Hs = f2_geo.Hs_geo.dot(f4_f2.Hs.dot(LA.inv(f4_2006.Hs)))
# dan_geo = reg3d_T.gt_transformation(dan_geo_Hs)
# dan_geo.save_to_file(dan_root + "/Hs_geo")

# import pdb; pdb.set_trace()


#******************** Capitol ********************

# root_2011 = "/Users/isa/Experiments/reg3d_eval/capitol_2011/original"
# root_2006 = "/Users/isa/Experiments/reg3d_eval/capitol_2006/original"

# #Load 2011-2006
# Hfile_2011_2006 = root_2011 + "/2011-2006_Hs.txt"
# T_2011_2006 = reg3d_T.gt_transformation(Hfile_2011_2006)

# #Compute missing ones
# #2006-2011
# Hs_2006_2011 = LA.inv(T_2011_2006.Hs)
# T_2006_2011 = reg3d_T.gt_transformation(Hs_2006_2011)
# T_2006_2011.save_to_file(root_2006 + "/2006-2011_Hs")



#Load 2006-lidar
# Hfile_geo_2006 = "/data/lidar_providence/capitol/capitol-dan_Hs.txt"
# Tgeo_2006 = reg3d_T.geo_transformation(Hfile_geo_2006)
# Hs_geo_2011 = Tgeo_2006.Hs_geo.dot(T_2011_2006.Hs)
# Tgeo_2011 = reg3d_T.gt_transformation(Hs_geo_2011)
# Tgeo_2011.save_to_file(root_2011 + "/Hs_geo")

#******************** Downtown ********************
#
# root_cvg ="/Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight5_sites/site_5"
# root_2011 = "/Users/isa/Experiments/reg3d_eval/downtown_2011/original"
# root_2006 = "/Users/isa/Experiments/reg3d_eval/downtown_2006/original"

# #Load 2011-2006
# Hfile_2011_2006 = root_2011 + "/2011-2006_Hs.txt"
# T_2011_2006 = reg3d_T.gt_transformation(Hfile_2011_2006)

# Hfile_cvg_2006 = root_cvg + "/f5-2006_Hs.txt"
# T_cvg_2006 = reg3d_T.gt_transformation(Hfile_cvg_2006)


# #Load 2006-lidar
# Hfile_geo_2006 = "/data/lidar_providence/downtown_offset-1-financial-dan-Hs.txt"

# Tgeo_2006 = reg3d_T.geo_transformation(Hfile_geo_2006)
# Hs_geo_2011 = Tgeo_2006.Hs_geo.dot(T_2011_2006.Hs)
# Tgeo_2011 = reg3d_T.gt_transformation(Hs_geo_2011)
# Tgeo_2011.save_to_file(root_2011 + "/Hs_geo")

# Hs_geo_cvg = Tgeo_2006.Hs_geo.dot(T_cvg_2006.Hs)
# Tgeo_cvg = reg3d_T.gt_transformation(Hs_geo_cvg)
# Tgeo_cvg.save_to_file(root_cvg + "/Hs_geo")


# import pdb; pdb.set_trace()