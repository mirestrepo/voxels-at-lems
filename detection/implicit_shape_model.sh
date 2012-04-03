#!/bin/bash
"""
Created on Mon Sept 27, 2011

@author:Isabel Restrepo

Detection tests
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
learn_category_codebook=false;

learn_category_codebook=true;

#################################################################################################################################
#main directories - all other dirs are relative to this
#main_dir="/Users/isa/Experiments/BOF/test_downtown/taylor";
main_dir="/Users/isa/Experiments/BOF/helicopter_providence/taylor";
#################################################################################################################################




################################################################################
#3b. Learn Taylor codebook
################################################################################
export PYTHONPATH=$LEMS_PYTHONPATH;
echo "PYTHONPATH=" $PYTHONPATH

num_means=20;
bof_dir=$main_dir"/bof_category_specific";
k_means_dir=$bof_dir"/k_means_"$num_means
fraction=0.01;
J=10;  #number of subsamples
max_it=500; #max number of iteration for k-means

if $learn_category_codebook; then
   num_cores=8;
   /opt/local/Library/Frameworks/Python.framework/Versions/2.6/bin/python /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_category_codebook/learn_category_codebook.py --bof_dir $bof_dir --k_means_dir $k_means_dir --num_cores $num_cores --num_means $num_means --fraction $fraction --J $J --max_it $max_it
fi

   

END=$(date +%s)
DIFF=$(( $END - $START ))
echo "Shell script took $DIFF seconds"
