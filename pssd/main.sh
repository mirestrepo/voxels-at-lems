# cd /Projects/pssd/build/reconstruction
# ./pssd_recon -oL 10 -w 1 1 2 -tol 1.0e-7 /Users/isa/Experiments/pssd/middlebury/temple1/temple_full.ply /Users/isa/Experiments/pssd/middlebury/temple1/surface_estimation/l_10_w_1_1_2_nmag_nout.wrl
# ./pssd_recon -oL 10 -w 1 1 3 -tol 1.0e-7 /Users/isa/Experiments/pssd/middlebury/temple1/temple_full.ply /Users/isa/Experiments/pssd/middlebury/temple1/surface_estimation/l_10_w_1_1_3_nmag_nout.wrl
# ./pssd_recon -oL 10 -w 1 1 4 -tol 1.0e-7 /Users/isa/Experiments/pssd/middlebury/temple1/temple_full.ply /Users/isa/Experiments/pssd/middlebury/temple1/surface_estimation/l_10_w_1_1_4_nmag_nout.wrl

#***********************************
#      IJCV experiments
#***********************************

#----------------------------------
#      Taylor experiments
#----------------------------------

# #run taylor kernels on downtown scene
# root_dir="/data/downtown_oranges";
# # directory where boxm2 scene is stored
# model_dirname="boxm2_site_mog";
# scene_file="scene_cropped.xml"
# device_name="gpu1";

# kernel_path="/Projects/vxl/src/contrib/brl/bseg/bvpl/doc/taylor2_5_5_5";

# for (( i=2; i<3; i++ )); do
#     python ../boxm2/boxm2_compute_taylor_coefficients.py -s $root_dir -x "$model_dirname/$scene_file" -g $device_name --kernel_path $kernel_path --k_idx $i
# done

#----------------------------------
#      Reconstruction
#----------------------------------

cd /Projects/gssd_code/dual/build/recon

site=downtown
site_path=/Users/isa/Experiments/super3d_journal/$site
# ./ssd_dual -oL 9 -w 1 1 10 1 -mcn 0.0170 -d $site_path/s_p_vis/c_nmag/downtown_s_p_visum45_c_nmag.ply $site_path/s_p_vis/c_nmag/downtown_s_p_visum45_c_nmag_1_1_10_1.ply &
# ./ssd_dual -oL 9 -w 1 1 10 2 -mcn 0.0170 -d $site_path/s_p_vis/c_nmag/downtown_s_p_visum45_c_nmag.ply $site_path/s_p_vis/c_nmag/downtown_s_p_visum45_c_nmag_1_1_10_2.ply &
# ./ssd_dual -oL 9 -w 1 1 10 4 -mcn 0.0170 -d $site_path/s_p_vis/c_nmag/downtown_s_p_visum45_c_nmag.ply $site_path/s_p_vis/c_nmag/downtown_s_p_visum45_c_nmag_1_1_10_4.ply &
# ./ssd_dual -oL 9 -w 1 1 10 1 -mcn 0.0181 -d $site_path/s_p_vis/c_nmag/downtown_s_p_visum60_c_nmag.ply $site_path/s_p_vis/c_nmag/downtown_s_p_visum60_c_nmag_1_1_10_1.ply &
# ./ssd_dual -oL 9 -w 1 1 10 2 -mcn 0.0181 -d $site_path/s_p_vis/c_nmag/downtown_s_p_visum60_c_nmag.ply $site_path/s_p_vis/c_nmag/downtown_s_p_visum60_c_nmag_1_1_10_2.ply &
# ./ssd_dual -oL 9 -w 1 1 10 4 -mcn 0.0181 -d $site_path/s_p_vis/c_nmag/downtown_s_p_visum60_c_nmag.ply $site_path/s_p_vis/c_nmag/downtown_s_p_visum60_c_nmag_1_1_10_4.ply &
# ./ssd_dual -oL 9 -w 1 1 10 1 -mcn 0.0198 -d $site_path/s_p_vis/c_nmag/downtown_s_p_visum90_c_nmag.ply $site_path/s_p_vis/c_nmag/downtown_s_p_visum90_c_nmag_1_1_10_1.ply &
# ./ssd_dual -oL 9 -w 1 1 10 2 -mcn 0.0198 -d $site_path/s_p_vis/c_nmag/downtown_s_p_visum90_c_nmag.ply $site_path/s_p_vis/c_nmag/downtown_s_p_visum90_c_nmag_1_1_10_2.ply &
# ./ssd_dual -oL 9 -w 1 1 10 4 -mcn 0.0198 -d $site_path/s_p_vis/c_nmag/downtown_s_p_visum90_c_nmag.ply $site_path/s_p_vis/c_nmag/downtown_s_p_visum90_c_nmag_1_1_10_4.ply &

# wait

# ./ssd_dual -oL 9 -w 1 1 10 1 -mcn 0.0126 -d $site_path/s_p_vis/c_p_vis_nmag/downtown_s_p_visum45_c_p_vissum_nmag.ply $site_path/s_p_vis/c_p_vis_nmag/downtown_s_p_visum45_c_p_vissum_nmag_1_1_10_1.ply &
# ./ssd_dual -oL 9 -w 1 1 10 2 -mcn 0.0126 -d $site_path/s_p_vis/c_p_vis_nmag/downtown_s_p_visum45_c_p_vissum_nmag.ply $site_path/s_p_vis/c_p_vis_nmag/downtown_s_p_visum45_c_p_vissum_nmag_1_1_10_2.ply &
# ./ssd_dual -oL 9 -w 1 1 10 4 -mcn 0.0126 -d $site_path/s_p_vis/c_p_vis_nmag/downtown_s_p_visum45_c_p_vissum_nmag.ply $site_path/s_p_vis/c_p_vis_nmag/downtown_s_p_visum45_c_p_vissum_nmag_1_1_10_4.ply &
# ./ssd_dual -oL 9 -w 1 1 10 1 -mcn 0.0130 -d $site_path/s_p_vis/c_p_vis_nmag/downtown_s_p_visum60_c_p_vissum_nmag.ply $site_path/s_p_vis/c_p_vis_nmag/downtown_s_p_visum60_c_p_vissum_nmag_1_1_10_1.ply &
# ./ssd_dual -oL 9 -w 1 1 10 2 -mcn 0.0130 -d $site_path/s_p_vis/c_p_vis_nmag/downtown_s_p_visum60_c_p_vissum_nmag.ply $site_path/s_p_vis/c_p_vis_nmag/downtown_s_p_visum60_c_p_vissum_nmag_1_1_10_2.ply &
# ./ssd_dual -oL 9 -w 1 1 10 4 -mcn 0.0130 -d $site_path/s_p_vis/c_p_vis_nmag/downtown_s_p_visum60_c_p_vissum_nmag.ply $site_path/s_p_vis/c_p_vis_nmag/downtown_s_p_visum60_c_p_vissum_nmag_1_1_10_4.ply &
# ./ssd_dual -oL 9 -w 1 1 10 1 -mcn 0.0136 -d $site_path/s_p_vis/c_p_vis_nmag/downtown_s_p_visum90_c_p_vissum_nmag.ply $site_path/s_p_vis/c_p_vis_nmag/downtown_s_p_visum90_c_p_vissum_nmag_1_1_10_1.ply &
# ./ssd_dual -oL 9 -w 1 1 10 2 -mcn 0.0136 -d $site_path/s_p_vis/c_p_vis_nmag/downtown_s_p_visum90_c_p_vissum_nmag.ply $site_path/s_p_vis/c_p_vis_nmag/downtown_s_p_visum90_c_p_vissum_nmag_1_1_10_2.ply &
# ./ssd_dual -oL 9 -w 1 1 10 4 -mcn 0.0136 -d $site_path/s_p_vis/c_p_vis_nmag/downtown_s_p_visum90_c_p_vissum_nmag.ply $site_path/s_p_vis/c_p_vis_nmag/downtown_s_p_visum90_c_p_vissum_nmag_1_1_10_4.ply &
# wait

#mcn 25%
./ssd_dual -oL 9 -w 1 1 10 2 -mcn 0.0142 -d $site_path/s_p_vis/c_p_vis_nmag/downtown_s_p_visum45_c_p_vissum_nmag.ply $site_path/s_p_vis/c_p_vis_nmag/downtown_s_p_visum45_c_p_vissum_nmag_1_1_10_2_25.ply &
./ssd_dual -oL 9 -w 1 1 10 2 -mcn 0.0146 -d $site_path/s_p_vis/c_p_vis_nmag/downtown_s_p_visum60_c_p_vissum_nmag.ply $site_path/s_p_vis/c_p_vis_nmag/downtown_s_p_visum60_c_p_vissum_nmag_1_1_10_2_25.ply &

#mcn 50%
./ssd_dual -oL 9 -w 1 1 10 2 -mcn 0.0215 -d $site_path/s_p_vis/c_p_vis_nmag/downtown_s_p_visum45_c_p_vissum_nmag.ply $site_path/s_p_vis/c_p_vis_nmag/downtown_s_p_visum45_c_p_vissum_nmag_1_1_10_2_40.ply &
./ssd_dual -oL 9 -w 1 1 10 2 -mcn 0.0218 -d $site_path/s_p_vis/c_p_vis_nmag/downtown_s_p_visum60_c_p_vissum_nmag.ply $site_path/s_p_vis/c_p_vis_nmag/downtown_s_p_visum60_c_p_vissum_nmag_1_1_10_2_40.ply &
wait