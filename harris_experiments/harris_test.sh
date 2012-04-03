#!/bin/bash
"""
Created on Mon Feb 14, 2011

@author:Isabel Restrepo

A script that encapsulates all steps needed to learn and classify based on corner features
"""

START=$(date +%s)

if [ $1 = "-r" ] ; then
  LEMS_PYTHONPATH=/Projects/lemsvxl/bin/Release/lib
  VXL_PYTHONPATH=/Projects/vxl/bin/Release/lib
else
  if [ $1 = "-d" ] ; then
       LEMS_PYTHONPATH=/Projects/lemsvxl/bin/Debug/lib
       VXL_PYTHONPATH=/Projects/vxl/bin/Debug/lib
  else
      echo "Need a flag, either -d or -r";
  fi 
fi

#################################################################################################################################
#steps to run - set to true to run - note that the work flow can't be run at once because the user needs to complete the xml file
#################################################################################################################################
project_taylor=false;
compute_corner_measure=true

#################################################################################################################################
#main directories - all other dirs are relative to this
main_dir="/Users/isa/Experiments/BOF/helicopter_providence";
#################################################################################################################################



################################################################################
#2b. Run Taylor kernels and 10-d basis scenes
################################################################################
taylor_dir=$main_dir"/taylor/global_taylor";
corners_dir=$main_dir"/corners/k_1_t_2/global_corners";

if $compute_corner_measure; then

   export PYTHONPATH=$VXL_PYTHONPATH;
   echo "PYTHONPATH=" $PYTHONPATH
  
   num_cores=4;
   #python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/corners/global_corners/compute_harris_measure.py --taylor_dir $taylor_dir --corners_dir $corners_dir --num_cores $num_cores
   num_cores=4;
   #python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/corners/global_corners/explore_harris_measure_scenes.py --taylor_dir $taylor_dir --corners_dir $corners_dir --num_cores $num_cores
   
   num_cores=6;
   python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/corners/global_corners/threshold_corners.py --taylor_dir $taylor_dir --corners_dir $corners_dir --num_cores $num_cores
fi

END=$(date +%s)
DIFF=$(( $END - $START ))
echo "Shell script took $DIFF seconds"
