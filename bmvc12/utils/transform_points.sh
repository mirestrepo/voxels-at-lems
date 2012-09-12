
#3 6 7 8 10 11 12 16 18 21 22 23 25 26 27
for i in 8 11; do

category=residential;
dir_in="Z:/video/helicopter_providence/ground_truth_3_11/ground_truth_original/site${i}/${category}";
dir_out="Z:/video/helicopter_providence/ground_truth_3_12/ground_truth_original/site${i}/${category}";
mkdir -p $dir_out;	

"C:/vxl/build/contrib/brl/bbas/bwm/exe/Release/bwm_3d_site_transform_points.exe" -corrs "Z:/video/helicopter_providence/3d_site_transformation_3_11_to_3_12/site${i}/site${i}_correspondances.txt" -in_point_dir $dir_in -out_point_dir $dir_out	

done