#***********************************
#      IJCV experiments
#***********************************



#----------------------------------
#      Reconstruction
#----------------------------------

cd /Projects/PoissonRecon/Bin

site_path=/Users/isa/Experiments/super3d_journal/winners/poisson

site=downtown
# ./PoissonRecon --depth 9 --samplesPerNode 1 --confidence --verbose --in $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply --out $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_1.ply&
# ./PoissonRecon --depth 9 --samplesPerNode 3 --confidence --verbose --in $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply --out $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_3.ply&
# ./PoissonRecon --depth 9 --samplesPerNode 5 --confidence --verbose --in $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply --out $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_5.ply &
# ./PoissonRecon --depth 9 --samplesPerNode 10 --confidence --verbose --in $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply --out $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_10.ply &
# ./PoissonRecon --depth 9 --samplesPerNode 5 --verbose --in $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply --out $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_5_nc.ply &
# ./PoissonRecon --depth 9 --samplesPerNode 3 --verbose --in $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply --out $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_3_nc.ply

./PoissonRecon --depth 9 --samplesPerNode 5 --verbose --confidence --pointWeight 0 --in $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply --out $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_5_pw0.ply &
./PoissonRecon --depth 9 --samplesPerNode 5 --verbose --pointWeight 0 --in $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply --out $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_5_nc_pw0.ply &

wait
# site=scili
# ./PoissonRecon --depth 9 --samplesPerNode 3 --confidence --verbose --in $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply --out $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_3.ply
# ./PoissonRecon --depth 9 --samplesPerNode 5 --confidence --verbose --in $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply --out $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_5.ply
# ./PoissonRecon --depth 9 --samplesPerNode 3 --verbose --in $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply --out $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_3_nc.ply
# ./PoissonRecon --depth 9 --samplesPerNode 5 --verbose --in $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply --out $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_5_nc.ply

# ./PoissonRecon --depth 9 --samplesPerNode 10 --verbose --confidence --in $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply --out $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_10.ply
# ./PoissonRecon --depth 9 --samplesPerNode 10 --verbose --in $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply --out $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_10_nc.ply

# ./PoissonRecon --depth 9 --samplesPerNode 5 --verbose --confidence --pointWeight 0 --in $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply --out $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_5_pw0.ply &
# ./PoissonRecon --depth 9 --samplesPerNode 5 --verbose --pointWeight 0 --in $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply --out $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_5_nc_pw0.ply &

# wait

# site=bh
# ./PoissonRecon --depth 9 --samplesPerNode 3 --confidence --verbose --in $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply --out $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_3.ply
# ./PoissonRecon --depth 9 --samplesPerNode 5 --confidence --verbose --in $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply --out $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_5.ply
# ./PoissonRecon --depth 9 --samplesPerNode 3 --verbose --in $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply --out $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_3_nc.ply
# ./PoissonRecon --depth 9 --samplesPerNode 5 --verbose --in $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply --out $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_5_nc.ply
# ./PoissonRecon --depth 9 --samplesPerNode 10 --verbose --confidence --in $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply --out $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_10.ply
# ./PoissonRecon --depth 9 --samplesPerNode 10 --verbose --in $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply --out $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_10_nc.ply


# ./PoissonRecon --depth 9 --samplesPerNode 5 --verbose --confidence --pointWeight 0 --in $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply --out $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_5_pw0.ply&
# ./PoissonRecon --depth 9 --samplesPerNode 5 --verbose --pointWeight 0 --in $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag.ply --out $site_path/${site}_s_map_pc_30_60_c_sum_exp_nmag_5_nc_pw0.ply&

# wait