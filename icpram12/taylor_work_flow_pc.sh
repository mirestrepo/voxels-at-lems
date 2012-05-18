#!/bin/bash
"""
Created on Mon Feb 14, 2011

@author:Isabel Restrepo

A script that encapsulates all steps needed to learn and classify based on taylor features
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
#main directories - all other dirs are relative to this
main_dir="/Volumes/Users/brandon/Desktop/helicopter2_providence/taylor";
#main_dir="/Users/isa/Experiments/BOF/providence_sites/taylor";
#################################################################################################################################

  




################################################################################
#3b. Learn Taylor codebook
################################################################################
export PYTHONPATH=$LEMS_PYTHONPATH;
echo "PYTHONPATH=" $PYTHONPATH


for num_means in 2 4 8 10 20 50 100 
do
    bof_dir=$main_dir"/bof";
    class_histograms_dir=$bof_dir"/class_histograms_"$num_means
    classification_dir=$bof_dir"/classification_"$num_means
    ncategories=5;
    python /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_categories/plot_category_histograms.py --bof_dir $bof_dir --class_histograms_dir $class_histograms_dir
    python /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/classify/display_classification_results.py --classification_dir $classification_dir --ncategories $ncategories

done

END=$(date +%s)
DIFF=$(( $END - $START ))
echo "Shell script took $DIFF seconds"
