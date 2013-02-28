#***********************************
#      IJCV experiments
#***********************************



#----------------------------------
#      Reconstruction
#----------------------------------

cd /Projects/gssd_code/dual/build/recon

site_path=/Users/isa/Experiments/super3d_journal/winners/ssd

site=downtown
./ssd_dual -oL 9 -w 1 1 10 2 -mcn 0.0153 -d $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_1_1_10_2_25.ply

# site=scili
# ./ssd_dual -oL 9 -w 1 1 10 2 -mcn 0.0546 -d $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_1_1_10_2_25.ply &

# site=bh
# ./ssd_dual -oL 9 -w 1 1 10 2 -mcn 0.0583 -d $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_1_1_10_2_25.ply &

wait