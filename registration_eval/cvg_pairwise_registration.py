import reg3d_transformations as reg3d_T
from numpy import linalg as LA
import transformations as tf



cvg_root = "/Users/isa/Experiments/reg3d_eval/cvg_eo_data"

# #******************** Site 1 ********************

# #Load f2-lidar
# f2_lidar_file = cvg_root + "/flight2_sites/site_1/Hs_geo.txt"
# f2_geo = reg3d_T.geo_transformation(f2_lidar_file)


# #Load f4-f2
# f4_f2_file = cvg_root + "/flight4_sites/site_1/f4-f2_Hs.txt"
# f4_f2 = reg3d_T.gt_transformation(f4_f2_file)

# #Load f5-f2
# f5_f2_file = cvg_root + "/flight5_sites/site_1/f5-f2_Hs.txt"
# f5_f2 = reg3d_T.gt_transformation(f5_f2_file)

# #Compute missing ones

# #f5-f4
# f5_f4_Hs = LA.inv(f4_f2.Hs).dot(f5_f2.Hs)
# f5_f4 = reg3d_T.gt_transformation(f5_f4_Hs)
# f5_f4.save_to_file(cvg_root + "/flight5_sites/site_1/f5-f4_Hs")
# #f2-lidar
# f4_Hs_geo = f2_geo.Hs_geo.dot(f4_f2.Hs)
# f4_geo = reg3d_T.gt_transformation(f4_Hs_geo)
# f4_geo.save_to_file(cvg_root + "/flight4_sites/site_1/Hs_geo")

# # import pdb; pdb.set_trace()

# #******************** Site 2 ********************

# #Load f2-lidar
# f2_lidar_file = cvg_root + "/flight2_sites/site_2/Hs_geo.txt"
# f2_geo = reg3d_T.geo_transformation(f2_lidar_file)


# #Load f4-f2
# f4_f2_file = cvg_root + "/flight4_sites/site_2/f4-f2_Hs.txt"
# f4_f2 = reg3d_T.gt_transformation(f4_f2_file)

# #Load f5-f2
# f5_f4_file = cvg_root + "/flight5_sites/site_2/f5-f4_Hs.txt"
# f5_f4 = reg3d_T.gt_transformation(f5_f4_file)

#Compute missing ones

#f5-f2
# f5_f2_Hs = f4_f2.Hs.dot(f5_f4.Hs)
# f5_f2 = reg3d_T.gt_transformation(f5_f2_Hs)
# f5_f2.save_to_file(cvg_root + "/flight5_sites/site_2/f5-f2_Hs")
# #f2-lidar
# f4_Hs_geo = f2_geo.Hs_geo.dot(f4_f2.Hs)
# f4_geo = reg3d_T.gt_transformation(f4_Hs_geo)
# f4_geo.save_to_file(cvg_root + "/flight4_sites/site_2/Hs_geo")

# # import pdb; pdb.set_trace()

#******************** Site 3 ********************

# # Load f2-lidar
# f2_lidar_file = cvg_root + "/flight2_sites/site_3/Hs_geo.txt"
# f2_geo = reg3d_T.geo_transformation(f2_lidar_file)


# #Load f4-f2
# f4_f2_file = cvg_root + "/flight4_sites/site_3/f4-f2_Hs.txt"
# f4_f2 = reg3d_T.gt_transformation(f4_f2_file)

# #Load f5-f2
# f5_f4_file = cvg_root + "/flight5_sites/site_3/f5-f4_Hs.txt"
# f5_f4 = reg3d_T.gt_transformation(f5_f4_file)

# Compute missing ones

# f5-f2
# f5_f2_Hs = f4_f2.Hs.dot(f5_f4.Hs)
# f5_f2 = reg3d_T.gt_transformation(f5_f2_Hs)
# f5_f2.save_to_file(cvg_root + "/flight5_sites/site_3/f5-f2_Hs")
# # f2-lidar
# f4_Hs_geo = f2_geo.Hs_geo.dot(f4_f2.Hs)
# f4_geo = reg3d_T.gt_transformation(f4_Hs_geo)
# f4_geo.save_to_file(cvg_root + "/flight4_sites/site_3/Hs_geo")

# import pdb; pdb.set_trace()

#******************** Site 4 ********************

# # Load f2-lidar
# f2_lidar_file = cvg_root + "/flight2_sites/site_4/Hs_geo.txt"
# f2_geo = reg3d_T.geo_transformation(f2_lidar_file)


# #Load f4-f2
# f4_f2_file = cvg_root + "/flight4_sites/site_4/f4-f2_Hs.txt"
# f4_f2 = reg3d_T.gt_transformation(f4_f2_file)

# #Load f5-f2
# f5_f4_file = cvg_root + "/flight5_sites/site_4/f5-f4_Hs.txt"
# f5_f4 = reg3d_T.gt_transformation(f5_f4_file)

# #Compute missing ones

# # f5-f2
# f5_f2_Hs = f4_f2.Hs.dot(f5_f4.Hs)
# f5_f2 = reg3d_T.gt_transformation(f5_f2_Hs)
# f5_f2.save_to_file(cvg_root + "/flight5_sites/site_4/f5-f2_Hs")
# # f2-lidar
# f4_Hs_geo = f2_geo.Hs_geo.dot(f4_f2.Hs)
# f4_geo = reg3d_T.gt_transformation(f4_Hs_geo)
# f4_geo.save_to_file(cvg_root + "/flight4_sites/site_4/Hs_geo")

# # import pdb; pdb.set_trace()

#******************** Site 7 ********************

# Load f2-lidar
f5_lidar_file = cvg_root + "/flight5_sites/site_7/Hs_geo.txt"
f5_geo = reg3d_T.geo_transformation(f5_lidar_file)


#Load f4-f2
f4_f2_file = cvg_root + "/flight4_sites/site_7/f4-f2_Hs.txt"
f4_f2 = reg3d_T.gt_transformation(f4_f2_file)

#Load f5-f4
f5_f4_file = cvg_root + "/flight5_sites/site_7/f5-f4_Hs.txt"
f5_f4 = reg3d_T.gt_transformation(f5_f4_file)

#Compute missing ones

# f5-f2
f5_f2_Hs = f4_f2.Hs.dot(f5_f4.Hs)
f5_f2 = reg3d_T.gt_transformation(f5_f2_Hs)
f5_f2.save_to_file(cvg_root + "/flight5_sites/site_7/f5-f2_Hs")
# f2-lidar
f2_Hs_geo = f5_geo.Hs_geo.dot(LA.inv(f5_f2_Hs))
f2_geo = reg3d_T.gt_transformation(f2_Hs_geo)
f2_geo.save_to_file(cvg_root + "/flight2_sites/site_7/Hs_geo")
# f4-lidar
f4_Hs_geo = f5_geo.Hs_geo.dot(LA.inv(f5_f4.Hs))
f4_geo = reg3d_T.gt_transformation(f4_Hs_geo)
f4_geo.save_to_file(cvg_root + "/flight4_sites/site_7/Hs_geo")


# # import pdb; pdb.set_trace()