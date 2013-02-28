#!/bin/bash

#geo-register cameras, then export stats


root_dir="/Users/isa/Experiments/reg3d_eval"

# #-----------------Downtown 2006-----------------

# site=downtown_2006

# cams_in_dir=${root_dir}/${site}/original/cams_krt
# cams_out_dir=${root_dir}/${site}/original/cams_krt_geo
# stats_file=$cams_out_dir/STATS

# # mkdir $cams_out_dirx
# geoTform="/data/lidar_providence/downtown_offset-1-financial-dan-Hs.txt"

# cd /Projects/vpcl/bin_make/Release/bin
# ./compute_geo_cam_stats -geo_tform $geoTform -stats_file $stats_file -in_cam_dir $cams_in_dir -out_cam_dir $cams_out_dir

# #-----------------Capitol 2006-----------------

# site=capitol_2006

# cams_in_dir=${root_dir}/${site}/original/cams_krt
# cams_out_dir=${root_dir}/${site}/original/cams_krt_geo
# stats_file=$cams_out_dir/STATS

# # mkdir $cams_out_dir
# geoTform="/data/lidar_providence/capitol/capitol-dan_Hs.txt"

# cd /Projects/vpcl/bin_make/Release/bin
# ./compute_geo_cam_stats -geo_tform $geoTform -stats_file $stats_file -in_cam_dir $cams_in_dir -out_cam_dir $cams_out_dir

# #-----------------BH 2006-----------------

# site=BH_2006

# cams_in_dir=${root_dir}/${site}/original/cams_krt
# cams_out_dir=${root_dir}/${site}/original/cams_krt_geo
# stats_file=$cams_out_dir/STATS

# mkdir $cams_out_dir
# geoTform="/Users/isa/Experiments/reg3d_eval/BH_2006/original/Hs_geo.txt"

# cd /Projects/vpcl/bin_make/Release/bin
# ./compute_geo_cam_stats -geo_tform $geoTform -stats_file $stats_file -in_cam_dir $cams_in_dir -out_cam_dir $cams_out_dir

#-----------------Capitol 2011-----------------

# site=capitol_2011

# cams_in_dir=${root_dir}/${site}/original/cams_krt
# cams_out_dir=${root_dir}/${site}/original/cams_krt_geo
# stats_file=$cams_out_dir/STATS

# mkdir $cams_out_dir
# geoTform="/Users/isa/Experiments/reg3d_eval/capitol_2011/original/Hs_geo.txt"

# cd /Projects/vpcl/bin_make/Release/bin
# ./compute_geo_cam_stats -geo_tform $geoTform -stats_file $stats_file -in_cam_dir $cams_in_dir -out_cam_dir $cams_out_dir

#-----------------Downtown 2011-----------------

# site=downtown_2011

# cams_in_dir=${root_dir}/${site}/original/cams_krt
# cams_out_dir=${root_dir}/${site}/original/cams_krt_geo
# stats_file=$cams_out_dir/STATS

# mkdir $cams_out_dir
# geoTform="/Users/isa/Experiments/reg3d_eval/downtown_2011/original/Hs_geo.txt"

# cd /Projects/vpcl/bin_make/Release/bin
# ./compute_geo_cam_stats -geo_tform $geoTform -stats_file $stats_file -in_cam_dir $cams_in_dir -out_cam_dir $cams_out_dir

# #-----------------SciLi 3-12-----------------

# site=scili_3_12

# cams_in_dir=${root_dir}/${site}/original/cams_krt
# cams_out_dir=${root_dir}/${site}/original/cams_krt_geo
# stats_file=$cams_out_dir/STATS

# mkdir $cams_out_dir
# geoTform="/data/lidar_providence/east_side/scili_3_12_Hs.txt"

# cd /Projects/vpcl/bin_make/Release/bin
# ./compute_geo_cam_stats -geo_tform $geoTform -stats_file $stats_file -in_cam_dir $cams_in_dir -out_cam_dir $cams_out_dir



# #-----------------res_east_side - 2011-----------------

# site=res_east_side

# cams_in_dir=${root_dir}/${site}/original/cams_krt
# cams_out_dir=${root_dir}/${site}/original/cams_krt_geo
# stats_file=$cams_out_dir/STATS

# mkdir $cams_out_dir
# geoTform="/data/lidar_providence/east_side/res_east_side_Hs.txt"

# cd /Projects/vpcl/bin_make/Release/bin
# ./compute_geo_cam_stats -geo_tform $geoTform -stats_file $stats_file -in_cam_dir $cams_in_dir -out_cam_dir $cams_out_dir


#-----------------res_middletown - 2011-----------------

# site=res_middletown

# cams_in_dir=${root_dir}/${site}/original/cams_krt
# cams_out_dir=${root_dir}/${site}/original/cams_krt_geo
# stats_file=$cams_out_dir/STATS

# mkdir $cams_out_dir
# geoTform="/data/lidar_providence/middle_town_residential/residential_Hs.txt"

# cd /Projects/vpcl/bin_make/Release/bin
# ./compute_geo_cam_stats -geo_tform $geoTform -stats_file $stats_file -in_cam_dir $cams_in_dir -out_cam_dir $cams_out_dir

#-----------------BH - CVG-----------------

for site in 5; do

    for f in 5; do
        cams_in_dir=${root_dir}/cvg_eo_data/flight${f}_sites/site_${site}/cams_krt
        cams_out_dir=${root_dir}/cvg_eo_data/flight${f}_sites/site_${site}/cams_krt_geo
        stats_file=$cams_out_dir/STATS.txt

        mkdir $cams_out_dir
        geoTform=${root_dir}/cvg_eo_data/flight${f}_sites/site_${site}/Hs_geo.txt

        cd /Projects/vpcl/bin_make/Release/bin
        ./compute_geo_cam_stats -geo_tform $geoTform -stats_file $stats_file -in_cam_dir $cams_in_dir -out_cam_dir $cams_out_dir
    done
done