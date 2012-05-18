#!/bin/bash
"""
Created on Mon Feb 14, 2011

@author:Isabel Restrepo

A script to prepare scenes for BOF (bag of features) processing
"""

START=$(date +%s)

if [ $1 = "-r" ] ; then
  VXL_PYTHONPATH=/Projects/vxl/bin/Release/lib
else
  if [ $1 = "-d" ] ; then
       VXL_PYTHONPATH=/Projects/vxl/bin/Debug/lib
  else
      echo "Need a flag, either -d or -r";
  fi 
fi

################################################################################
#1.  Obtain mean scene
################################################################################

export PYTHONPATH=$VXL_PYTHONPATH;
echo "PYTHONPATH=" $PYTHONPATH

for i in 0
do
  # an xml file containing a list a model directories and model names
  scenes_info="/Users/isa/Experiments/BOF/helicopter_providence/boxm_mog3_grey_scenes"$i".xml" 
  num_cores=2;
  grey_offset=1.0;
  python /Projects/voxels-at-lems/scripts/boxm/compute_expected_color_batch.py --scenes_info $scenes_info --num_cores $num_cores --grey_offset $grey_offset

  purge
  
done
