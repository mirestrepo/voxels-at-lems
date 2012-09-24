from vpcl_adaptor import *
ply_file = "/Users/isa/Experiments/reg3d_eval/downtown_dan/original/gauss_233_normals_pvn_99.ply"
pcd_file = "/Users/isa/Experiments/reg3d_eval/downtown_dan/original/gauss_233_normals_pvn_99_XYZ.pcd"
ply2pcd(ply_file, pcd_file, "PointXYZ", 1)