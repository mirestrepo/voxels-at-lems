#!/bin/bash
"""
Created on Mon Feb 14, 2011

@author:Isabel Restrepo

A script that encapsulates all steps needed to computer pca reconstruction error as a function of number of components used
"""

if [ $1 = "-r" ] ; then
  export PYTHONPATH=/Projects/vxl/bin/Release/lib
else
  if [ $1 = "-d" ] ; then
      export PYTHONPATH=/Projects/vxl/bin/Debug/lib
  else
      echo "Need a flag, either -d or -r";
  fi 
fi

echo "PYTHONPATH=" $PYTHONPATH

#pca_dir="/Users/isa/Experiments/BOF/learn_PCA/tests";
pca_dir="/Users/isa/Experiments/BOF/test_downtown/global_pca"
num_cores=3;

#python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/pca_global/init_global_pca.py --pca_dir $pca_dir
#python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/pca_global/compute_stats_pass0.py --pca_dir $pca_dir --num_cores $num_cores
#python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/pca_global/combine_stats_pairwise.py --pca_dir $pca_dir --num_cores $num_cores
#python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/pca_global/set_up_pca.py --pca_dir $pca_dir
python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/pca_global/pca_project.py --pca_dir $pca_dir --num_cores $num_cores
