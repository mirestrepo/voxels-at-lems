#***********************************
#      IJCV experiments
#***********************************

#----------------------------------
#      Reconstruction
#----------------------------------

cd /Projects/gssd_code/dual/build/recon

site=bh
site_path=/Users/isa/Experiments/super3d_journal/$site

#map-pc mcn 25 %
# ./ssd_dual -oL 9 -w 1 1 10 2 -mcn 0.0583 -d $site_path/s_map_pc/c_sum_exp_nmag/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply $site_path/s_map_pc/c_sum_exp_nmag/${site}_s_map_pc_30_60_c_sum_exp_nmag_1_1_10_2_25.ply &
# ./ssd_dual -oL 9 -w 1 1 10 2 -mcn 0.068 -d $site_path/s_map_pc/c_sum_exp_nmag/${site}_s_map_pc_60_120_c_sum_exp_nmag.ply $site_path/s_map_pc/c_sum_exp_nmag/${site}_s_map_pc_60_120_c_sum_exp_nmag_1_1_10_2_25.ply &

./ssd_dual -oL 9 -w 1 1 20 1 -mcn 0.0583 -d $site_path/s_map_pc/c_sum_exp_nmag/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply $site_path/s_map_pc/c_sum_exp_nmag/${site}_s_map_pc_30_60_c_sum_exp_nmag_1_1_20_1_25.ply &
./ssd_dual -oL 9 -w 1 1 20 1 -mcn 0.068 -d $site_path/s_map_pc/c_sum_exp_nmag/${site}_s_map_pc_60_120_c_sum_exp_nmag.ply $site_path/s_map_pc/c_sum_exp_nmag/${site}_s_map_pc_60_120_c_sum_exp_nmag_1_1_20_1_25.ply &

./ssd_dual -oL 9 -w 1 1 40 1 -mcn 0.0583 -d $site_path/s_map_pc/c_sum_exp_nmag/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply $site_path/s_map_pc/c_sum_exp_nmag/${site}_s_map_pc_30_60_c_sum_exp_nmag_1_1_40_1_25.ply &
./ssd_dual -oL 9 -w 1 1 40 1 -mcn 0.068 -d $site_path/s_map_pc/c_sum_exp_nmag/${site}_s_map_pc_60_120_c_sum_exp_nmag.ply $site_path/s_map_pc/c_sum_exp_nmag/${site}_s_map_pc_60_120_c_sum_exp_nmag_1_1_40_1_25.ply &


#p*vis
# ./ssd_dual -oL 9 -w 1 1 10 2 -mcn 0.0540 -d $site_path/s_p_vis/c_p_vis_nmag/${site}_s_p_visum60_c_p_vissum_nmag.ply $site_path/s_p_vis/c_p_vis_nmag/${site}_s_p_visum60_c_p_vissum_nmag_1_1_10_2_25.ply &
wait