#!/bin/bash

if [ $1 = "-r" ] ; then
  export PYTHONPATH=/Projects/vxl/bin_xcode4/Release/lib
else
  if [ $1 = "-d" ] ; then
      export PYTHONPATH=/Projects/vxl/bin_xcode4/Debug/lib
  else
      echo "Need a flag, either -d or -r";
  fi 
fi

echo "PYTHONPATH=" $PYTHONPATH

#model_dir="/Users/isa/Experiments/boxm_cit_only_filtered";
#model_name="boxm_scene"

#model_dir="/Users/isa/Experiments/helicopter_providence/boxm_scenes/site12";

#model_dir="/Volumes/vision/video/isabel/super3d/scili_experiment/normal_scene/boxm_cit_only"
#model_dir="/Users/isa/Experiments/boxm_scili_full"

#python /Projects/voxels-at-lems/scripts/boxm/compute_expected_color_scene.py --model_dir $model_dir --model_name $model_name --grey_offset 1.0
#python2.7 /Projects/voxels-at-lems/scripts/boxm/split_scene.py --model_dir $model_dir

#python2.7 /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/steerable_gauss_filters/init_response_scene.py
#python /Projects/voxels-at-lems/scripts/boxm/fill_internal_nodes.py
#python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/compute_gauss_gradient_alpha.py --model_dir $model_dir
#python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/gauss_gradient_to_binary.py
#python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/pca_error.py
#python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/extract_pca_kernels.py
#python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/run_taylor_capitol.py
#python /Projects/voxels-at-lems/scripts/boxm/update_downtown.py
#python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/save_scene_threads.py
#python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/compute_taylor_error_scene.py
#python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/add_taylor_error.py
#python /Projects/voxels-at-lems/scripts/bmvc11/render_top_expected_image.py
#python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/release/training_error/normalized_training_error.py
#python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/load_pca_info.py

model_dir="/Users/isa/Experiments/tests/from_ply";
nblocks_x=4;
nblocks_y=4;
nblocks_z=2;
num_cores=8;
python2.7 /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/run_gauss_smoothing.py --model_dir $model_dir --nblocks_x $nblocks_x --nblocks_y $nblocks_y --nblocks_z $nblocks_z --num_cores $num_cores


#********************** Super 3D *******************************#
#model_dir="/Users/isa/Experiments/super3d/scili_experiments_bicubic/sr2_scene_images/boxm_cit_only"
#python2.7 /Projects/voxels-at-lems/scripts/boxm/split_scene.py --model_dir $model_dir
#python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/compute_gauss_gradient_alpha.py --model_dir $model_dir
#python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/gauss_gradient_to_binary.py --model_dir $model_dir
#python /Projects/voxels-at-lems/scripts/super3d/filter_vis_images.py
#python2.7 /Projects/voxels-at-lems/scripts/super3d/compute_mean_var.py
#python2.7 /Projects/voxels-at-lems/scripts/super3d/compute_ssd.py
#python /Projects/voxels-at-lems/scripts/super3d/plot_ssd.py


#********************** BOXM UTILS: Splitting/Expected Appearance/Normals/Filling *******************************#
#model_dir="/Users/isa/Experiments/helicopter_providence/boxm_scenes/site1";
#model_name="mean_color_all_nodes_max_level_4"
#model_out_name="mean_color_all_nodes_max_level_3"
#model_dir="/Users/isa/Experiments/tests/from_ply";
#ply_file="/Users/isa/Experiments/tests/from_ply/site12_pmvs.ply"

#python2.7 /Projects/voxels-at-lems/scripts/boxm/compute_expected_color_scene.py --model_dir $model_dir --model_name $model_name --grey_offset 1.0
#python2.7 /Projects/voxels-at-lems/scripts/boxm/split_scene.py --model_dir $model_dir
#python2.7 /Projects/voxels-at-lems/scripts/boxm/fill_internal_nodes.py --model_dir $model_dir --model_name $model_name
#python2.7 /Projects/voxels-at-lems/scripts/boxm/remove_level0.py --model_dir $model_dir --model_name $model_name --model_out_name $model_out_name

#python2.7 /Projects/voxels-at-lems/scripts/boxm/create_scene_from_ply.py --model_dir $model_dir --ply_file $ply_file


################################################################################
# Run Taylor kernels 
################################################################################
#taylor_dir="/Users/isa/Experiments/helicopter_providence/tests_normals/max_level_6";
#dimension=3; #x,y,z

#init_global_taylor=false;
#project_taylor=true;

#if $init_global_taylor; then
  #  python2.7 /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/taylor/taylor_global/init_global_taylor.py --taylor_dir $taylor_dir --dimension $dimension
#fi


#if  $project_taylor; then

  #  num_cores=8;
  #python2.7 /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/taylor/taylor_global/compute_taylor_coefficients.py --taylor_dir $taylor_dir --num_cores $num_cores --dimension $dimension
#fi