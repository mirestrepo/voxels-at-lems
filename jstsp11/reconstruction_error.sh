#!/bin/bash
"""
Created on Mon Feb 14, 2011

@author:Isabel Restrepo

A script that encapsulates all steps needed to computer pca reconstruction error as a function of number of components used
"""

START=$(date +%s)

if [ $1 = "-r" ] ; then
  LEMS_PYTHONPATH=/Projects/lemsvxl/bin_xcode4/Release/lib
  VXL_PYTHONPATH=/Projects/vxl/bin_xcode4/Release/lib
else
  if [ $1 = "-d" ] ; then
       LEMS_PYTHONPATH=/Projects/lemsvxl/bin_xcode4/Debug/lib
       VXL_PYTHONPATH=/Projects/vxl/bin_xcode4/Debug/lib
  else
      echo "Need a flag, either -d or -r";
  fi 
fi


main_dir="/Users/isa/Experiments/BOF/helicopter_providence/pca";
pca_dir=$main_dir"/global_pca";
num_cores=16;
pca_error=false;

if $pca_error; then 
    export PYTHONPATH=$VXL_PYTHONPATH;
    echo "PYTHONPATH=" $PYTHONPATH;
    T=$(date +%s);
    python2.7 /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/pca_global/pca_proj_error.py --pca_dir $pca_dir --num_cores $num_cores
    python2.7 /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/pca_global/pca_add_proj_error.py --pca_dir $pca_dir --num_cores $num_cores
    
    DIFF=$(( $(date +%s) - $T ))
    time_file=$pca_dir/"pca_project_run_time.txt";
    echo "pca_project.py took $DIFF seconds" > $time_file; 
    
fi

main_dir="/Users/isa/Experiments/BOF/helicopter_providence/taylor";
taylor_dir=$main_dir"/global_taylor";
num_cores=16;
taylor_error=true;

if $taylor_error; then 
    export PYTHONPATH=$VXL_PYTHONPATH;
    echo "PYTHONPATH=" $PYTHONPATH;
    T=$(date +%s);
    python2.7 /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/taylor/taylor_global/taylor_proj_error.py --taylor_dir $taylor_dir --num_cores $num_cores
    
    DIFF=$(( $(date +%s) - $T ))
    time_file=$pca_dir/"pca_project_run_time.txt";
    echo "pca_project.py took $DIFF seconds" > $time_file; 
    
fi