
#********************MAP_PC

# cd /Projects/gssd_code/primal/build/recon-ssd

# site_path=/Users/isa/Experiments/super3d_journal/primal

# site=downtown
# ./ssd_recon -oL 9 -w 1 1 2 -mcn 0.0153 -d $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_1_1_2_25.ply &
# ./ssd_recon -oL 9 -w 1 2 4 -mcn 0.0153 -d $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_1_2_4_25.ply &

# site=scili
# ./ssd_recon -oL 9 -w 1 1 2 -mcn 0.0546 -d $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_1_1_2_25.ply &
# ./ssd_recon -oL 9 -w 1 2 4 -mcn 0.0546 -d $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_1_2_4_25.ply &

# site=bh
# ./ssd_recon -oL 9 -w 1 1 2 -mcn 0.0583 -d $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_1_1_2_25.ply &
# ./ssd_recon -oL 9 -w 1 2 4 -mcn 0.0583 -d $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_1_2_4_25.ply &

# wait

#********************P*VIS*NMAG

cd /Projects/gssd_code/primal/build/recon-ssd

site_path=/Users/isa/Experiments/gssd_thesis/primal

site=downtown
# ./ssd_recon -oL 9 -w 1 1 2 -mcn 0.00924 -d $site_path/${site}_pvn_90_c_p_vissum_nmag.ply $site_path/${site}_pvn_90_c_p_vissum_nmag_1_1_2_25.ply &
# ./ssd_recon -oL 9 -w 1 1 2 -mcn 0.01908-d $site_path/${site}_pvn_95_c_p_vissum_nmag.ply $site_path/${site}_pvn_95_c_p_vissum_nmag_1_1_2_25.ply &

./ssd_recon -oL 9 -w 1 1 2 -mcn 0.000458 -d $site_path/${site}_pvn_0_c_p_vissum_nmag.ply $site_path/${site}_pvn_0_c_p_vissum_nmag_1_1_2_25.ply &


# site=scili
# ./ssd_recon -oL 9 -w 1 1 2 -mcn 0.06088 -d $site_path/${site}_pvn_90_c_p_vissum_nmag.ply $site_path/${site}_pvn_90_c_p_vissum_nmag_1_1_2_25.ply &
# ./ssd_recon -oL 9 -w 1 1 2 -mcn 0.08952 -d $site_path/${site}_pvn_95_c_p_vissum_nmag.ply $site_path/${site}_pvn_95_c_p_vissum_nmag_1_1_2_25.ply &

# site=bh
# ./ssd_recon -oL 9 -w 1 1 2 -mcn 0.06632 -d $site_path/${site}_pvn_90_c_p_vissum_nmag.ply $site_path/${site}_pvn_90_c_p_vissum_nmag_1_1_2_25.ply &
# ./ssd_recon -oL 9 -w 1 1 2 -mcn 0.09754 -d $site_path/${site}_pvn_95_c_p_vissum_nmag.ply $site_path/${site}_pvn_95_c_p_vissum_nmag_1_1_2_25.ply &


# ./ssd_recon -oL 9 -w 1 1 2 -mcn 0.00725 -d $site_path/bh_pvn_30_c_p_vissum_nmag.ply $site_path/${site}_pvn_30_c_p_vissum_nmag_1_1_2_25.ply


# wait

#********************PMVS + POISSON


# cd /Projects/PoissonRecon/Bin

# site_path=/Users/isa/Experiments/gssd_thesis/pmvs_poisson

# site=downtown
# ./PoissonRecon --depth 9 --samplesPerNode 5 --verbose --pointWeight 0 --in $site_path/${site}_pmvs_output.ply --out $site_path/${site}_pmvs_output_5_nc_pw0.ply &
# ./PoissonRecon --depth 9 --samplesPerNode 5 --verbose --in $site_path/${site}_pmvs_output.ply --out $site_path/${site}_pmvs_output_5_nc.ply &

# ./PoissonRecon --depth 9 --samplesPerNode 3 --verbose --pointWeight 0 --in $site_path/${site}_pmvs_output.ply --out $site_path/${site}_pmvs_output_3_nc_pw0.ply &
# ./PoissonRecon --depth 9 --samplesPerNode 10 --verbose --in $site_path/${site}_pmvs_output.ply --out $site_path/${site}_pmvs_output_10_nc.ply &
# ./PoissonRecon --depth 9 --samplesPerNode 2 --verbose --pointWeight 0 --in $site_path/${site}_cropped_pmvs_output.ply --out $site_path/${site}_cropped_pmvs_output_2_nc_pw0.ply

