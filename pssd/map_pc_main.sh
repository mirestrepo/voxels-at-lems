#***********************************
#      IJCV experiments
#***********************************

#----------------------------------
#      Reconstruction
#----------------------------------

cd /Projects/gssd_code/dual/build/recon

# site=downtown
# site_path=/Users/isa/Experiments/super3d_journal/$site
# ./ssd_dual -oL 9 -w 1 2 10 4 -mcn 0.0127 -d $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_20_45_c_sum_exp_nmag.ply $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_20_45_c_sum_exp_nmag_1_2_10_4_20.ply &
# ./ssd_dual -oL 9 -w 1 1 10 2 -mcn 0.0127 -d $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_20_45_c_sum_exp_nmag.ply $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_20_45_c_sum_exp_nmag_1_1_10_2_20.ply &
# ./ssd_dual -oL 9 -w 1 2 10 4 -mcn 0.0136 -d $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_30_60_c_sum_exp_nmag.ply $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_30_60_c_sum_exp_nmag_1_2_10_4_20.ply &
# ./ssd_dual -oL 9 -w 1 1 10 2 -mcn 0.0136 -d $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_30_60_c_sum_exp_nmag.ply $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_30_60_c_sum_exp_nmag_1_1_10_2_20.ply &
# # wait

# #mcn 25%
# ./ssd_dual -oL 9 -w 1 2 10 4 -mcn 0.0144 -d $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_20_45_c_sum_exp_nmag.ply $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_20_45_c_sum_exp_nmag_1_2_10_4_25.ply &
# ./ssd_dual -oL 9 -w 1 1 10 2 -mcn 0.0144 -d $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_20_45_c_sum_exp_nmag.ply $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_20_45_c_sum_exp_nmag_1_1_10_2_25.ply &
# ./ssd_dual -oL 9 -w 1 1 10 2 -mcn 0.0153 -d $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_30_60_c_sum_exp_nmag.ply $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_30_60_c_sum_exp_nmag_1_1_10_2_25.ply &
# ./ssd_dual -oL 9 -w 1 2 10 4 -mcn 0.0153 -d $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_30_60_c_sum_exp_nmag.ply $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_30_60_c_sum_exp_nmag_1_2_10_4_25.ply &
# wait

# mcn 50%

# ./ssd_dual -oL 9 -w 1 2 10 4 -mcn 0.0226 -d $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_20_45_c_sum_exp_nmag.ply $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_20_45_c_sum_exp_nmag_1_2_10_4_50.ply &
# ./ssd_dual -oL 9 -w 1 1 10 2 -mcn 0.0226 -d $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_20_45_c_sum_exp_nmag.ply $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_20_45_c_sum_exp_nmag_1_1_10_2_50.ply &
# ./ssd_dual -oL 9 -w 1 2 10 4 -mcn 0.0234 -d $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_30_60_c_sum_exp_nmag.ply $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_30_60_c_sum_exp_nmag_1_2_10_4_50.ply &
# ./ssd_dual -oL 9 -w 1 1 10 2 -mcn 0.0234 -d $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_30_60_c_sum_exp_nmag.ply $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_30_60_c_sum_exp_nmag_1_1_10_2_50.ply &
# wait

# ./ssd_dual -oL 9 -w 1 1 20 1 -mcn 0.0153 -d $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_30_60_c_sum_exp_nmag.ply $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_30_60_c_sum_exp_nmag_1_1_20_1_25.ply &
# ./ssd_dual -oL 9 -w 1 1 40 1 -mcn 0.0153 -d $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_30_60_c_sum_exp_nmag.ply $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_30_60_c_sum_exp_nmag_1_1_40_1_25.ply &
# ./ssd_dual -oL 9 -w 1 1 20 1 -mcn 0.0152 -d $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_60_120_c_sum_exp_nmag.ply $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_60_120_c_sum_exp_nmag_1_1_20_1_25.ply &
# ./ssd_dual -oL 9 -w 1 1 40 1 -mcn 0.0152 -d $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_60_120_c_sum_exp_nmag.ply $site_path/s_map_pc/c_sum_exp_nmag/downtown_s_map_pc_60_120_c_sum_exp_nmag_1_1_40_1_25.ply &



# wait

cd /Projects/gssd_code/dual/build/recon

site_path=/Users/isa/Experiments/super3d_journal/winners/gssd

site=downtown
./ssd_dual -oL 9 -w 1 1 10 2 -mcn 0.0153 -d $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_1_1_10_2_25.ply

# site=scili
# ./ssd_dual -oL 9 -w 1 1 10 2 -mcn 0.0546 -d $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_1_1_10_2_25.ply &

# site=bh
# ./ssd_dual -oL 9 -w 1 1 10 2 -mcn 0.0583 -d $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_1_1_10_2_25.ply &

wait