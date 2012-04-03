#!/bin/bash
"""
Created on Mon Feb 14, 2011

@author:Isabel Restrepo

A script that encapsulates all steps needed to computer pca reconstruction error as a function of number of components used
"""

if [ $1 = "-r" ] ; then
  export PYTHONPATH=/Projects/vxl/bin/release/lib
else
  if [ $1 = "-d" ] ; then
      export PYTHONPATH=/Projects/vxl/bin/Debug/lib
  else
      echo "Need a flag, either -d or -r";
  fi 
fi

echo "PYTHONPATH=" $PYTHONPATH


model_dir="/Users/isa/Experiments/helicopter_providence/boxm_scenes/site22";
model_name="boxm_scene";

nblocks_x=3;
nblocks_y=4;
nblocks_z=2;

test_fraction=1.0;
num_cores=8;


#**************************************************
pca_dir="/Users/isa/Experiments/PCA/site22/5";
train_fraction=0.05;

#Compute reconstruction at each voxel in the scene
for ((dim = 125; dim < 126; dim = dim + 5))
do
  python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/release/reconstruction_error/compute_pca_error_scene.py --model_dir $model_dir --pca_dir $pca_dir --num_cores $num_cores --nblocks_x $nblocks_x --nblocks_y $nblocks_y --nblocks_z $nblocks_z --dimension $dim

  #Add error of fraction of voxels
  python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/release/reconstruction_error/add_pca_error.py --model_dir $model_dir --pca_dir $pca_dir --num_cores $num_cores --nblocks_x $nblocks_x --nblocks_y $nblocks_y --nblocks_z $nblocks_z --fraction $test_fraction --dimension $dim
done

#**************************************************
pca_dir="/Users/isa/Experiments/PCA/site22/10";
train_fraction=0.1;

#python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/release/reconstruction_error/extract_pca_kernels.py --model_dir $model_dir --pca_dir $pca_dir --train_fraction $train_fraction

#Compute reconstruction at each voxel in the scene
for ((dim = 125; dim < 126; dim = dim + 5))
do
  python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/release/reconstruction_error/compute_pca_error_scene.py --model_dir $model_dir --pca_dir $pca_dir --num_cores $num_cores --nblocks_x $nblocks_x --nblocks_y $nblocks_y --nblocks_z $nblocks_z --dimension $dim

  #Add error of fraction of voxels
  python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/release/reconstruction_error/add_pca_error.py --model_dir $model_dir --pca_dir $pca_dir --num_cores $num_cores --nblocks_x $nblocks_x --nblocks_y $nblocks_y --nblocks_z $nblocks_z --fraction $test_fraction --dimension $dim
done


#**************************************************
pca_dir="/Users/isa/Experiments/PCA/site22/20";
train_fraction=0.2;

#Compute PCA basis
#python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/release/reconstruction_error/extract_pca_kernels.py --model_dir $model_dir --pca_dir $pca_dir --train_fraction $train_fraction

#Compute reconstruction at each voxel in the scene
for ((dim = 125; dim < 126; dim = dim + 5))
do
  python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/release/reconstruction_error/compute_pca_error_scene.py --model_dir $model_dir --pca_dir $pca_dir --num_cores $num_cores --nblocks_x $nblocks_x --nblocks_y $nblocks_y --nblocks_z $nblocks_z --dimension $dim

  #Add error of fraction of voxels
  python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/release/reconstruction_error/add_pca_error.py --model_dir $model_dir --pca_dir $pca_dir --num_cores $num_cores --nblocks_x $nblocks_x --nblocks_y $nblocks_y --nblocks_z $nblocks_z --fraction $test_fraction --dimension $dim
done


#**************************************************
pca_dir="/Users/isa/Experiments/PCA/site22/50";
train_fraction=0.5;

#Compute PCA basis
#python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/release/reconstruction_error/extract_pca_kernels.py --model_dir $model_dir --pca_dir $pca_dir --train_fraction $train_fraction


#Compute reconstruction at each voxel in the scene
for ((dim = 125; dim < 126; dim = dim + 5))
do
  python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/release/reconstruction_error/compute_pca_error_scene.py --model_dir $model_dir --pca_dir $pca_dir --num_cores $num_cores --nblocks_x $nblocks_x --nblocks_y $nblocks_y --nblocks_z $nblocks_z --dimension $dim

  #Add error of fraction of voxels
  python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/release/reconstruction_error/add_pca_error.py --model_dir $model_dir --pca_dir $pca_dir --num_cores $num_cores --nblocks_x $nblocks_x --nblocks_y $nblocks_y --nblocks_z $nblocks_z --fraction $test_fraction --dimension $dim
done

#**************************************************
pca_dir="/Users/isa/Experiments/PCA/site22/80";
train_fraction=0.8;

#Compute PCA basis
#python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/release/reconstruction_error/extract_pca_kernels.py --model_dir $model_dir --pca_dir $pca_dir --train_fraction $train_fraction

#Compute reconstruction at each voxel in the scene
for ((dim = 125; dim < 126; dim = dim + 5))
do
  python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/release/reconstruction_error/compute_pca_error_scene.py --model_dir $model_dir --pca_dir $pca_dir --num_cores $num_cores --nblocks_x $nblocks_x --nblocks_y $nblocks_y --nblocks_z $nblocks_z --dimension $dim

  #Add error of fraction of voxels
  python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/release/reconstruction_error/add_pca_error.py --model_dir $model_dir --pca_dir $pca_dir --num_cores $num_cores --nblocks_x $nblocks_x --nblocks_y $nblocks_y --nblocks_z $nblocks_z --fraction $test_fraction --dimension $dim
done


#**************************************************
pca_dir="/Users/isa/Experiments/PCA/site22/100";
train_fraction=1.0;

#Compute PCA basis
#python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/release/reconstruction_error/extract_pca_kernels.py --model_dir $model_dir --pca_dir $pca_dir --train_fraction $train_fraction

#Compute reconstruction at each voxel in the scene
for ((dim = 125; dim < 126; dim = dim + 5))
do
  python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/release/reconstruction_error/compute_pca_error_scene.py --model_dir $model_dir --pca_dir $pca_dir --num_cores $num_cores --nblocks_x $nblocks_x --nblocks_y $nblocks_y --nblocks_z $nblocks_z --dimension $dim

  #Add error of fraction of voxels
  python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/release/reconstruction_error/add_pca_error.py --model_dir $model_dir --pca_dir $pca_dir --num_cores $num_cores --nblocks_x $nblocks_x --nblocks_y $nblocks_y --nblocks_z $nblocks_z --fraction $test_fraction --dimension $dim
done
