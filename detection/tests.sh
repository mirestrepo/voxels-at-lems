#!/bin/bash
"""
Created on Mon Sept 19, 2011

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
make_cluster_id_scenes=false;
compute_typical_bbox=false;

#make_cluster_id_scenes=true;
compute_typical_bbox=true;

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
bof_dir=$main_dir"/bof";
k_means_dir=$bof_dir"/k_means_"$num_means


#init bof xml file
if $make_cluster_id_scenes; then
   num_cores=8;
   python /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_codebook/k_means/cluster_id_scenes.py --bof_dir $bof_dir --k_means_dir $k_means_dir --num_cores $num_cores 
   python /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_codebook/k_means/save_cluster_id_scene_raw.py --bof_dir $bof_dir --num_cores $num_cores
fi

if $compute_typical_bbox; then
   python ./typical_bbox.py --bof_dir $bof_dir
fi
   

END=$(date +%s)
DIFF=$(( $END - $START ))
echo "Shell script took $DIFF seconds"
