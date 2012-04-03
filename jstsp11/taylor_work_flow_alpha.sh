#!/bin/bash

#Created on Mon Dec 12, 2011
#Author:Isabel Restrepo
#USAGE: taylor_work_flow.sh [-r or -d for release or debug][ integer for trial # ]
#DESCRIPTION:A script that encapsulates all steps needed to learn and classify based on taylor features
#This script was written with the purpose of running different trials of the learning/classification pipeline 
#so that results can be shown as the average of the trials


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


#################################################################################################################################
#steps to run - set to true to run - note that the work flow can't be run at once because the user needs to complete the xml file
#################################################################################################################################
split_scenes=false;
project_taylor=false;
init_bof_from_taylor_info=false;

#***************Stop here you need to make sure the bof_info.xml is accurate************************************#
learn_codebook=false;
#***************Stop here you need to make sure the bof_categories_info.xml is accurate**************************# 
learn_categories=false;
classify=false;


#################################################################################################################################
main_dir="/Users/isa/Experiments/BOF/helicopter_providence/taylor_alpha";
#################################################################################################################################


################################################################################
# Split scene
################################################################################
if $split_scenes; then

  export PYTHONPATH=$VXL_PYTHONPATH;
  echo "PYTHONPATH=" $PYTHONPATH

  # an xml file containing a list a model directories and model names
  scenes_info=$main_dir"/boxm_mog3_grey_scenes.xml" 
  num_cores=4;
  python /Projects/voxels-at-lems/scripts/boxm/split_scene_batch.py --scenes_info $scenes_info --num_cores $num_cores

fi





################################################################################
#Run Taylor kernels and 10-d basis scenes
################################################################################
taylor_dir=$main_dir"/global_taylor";
aux_scene_dir=$main_dir"/aux_scenes";
dimension=10;

if $init_global_taylor
    python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/taylor/taylor_global/init_global_taylor.py --taylor_dir $taylor_dir --dimension $dimension
fi


if  $project_taylor; then

    export PYTHONPATH=$VXL_PYTHONPATH;
    echo "PYTHONPATH=" $PYTHONPATH
  
    num_cores=3;
    T=$(date +%s)
    
    python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/taylor/taylor_global/compute_taylor_coefficients.py --taylor_dir $taylor_dir --num_cores $num_cores --dimension $dimension
    time_file=$taylor_dir/"project_run_time.txt";
    echo "compute_taylor_coefficients took $DIFF seconds" > $time_file; 
  
fi


################################################################################
# Learn Taylor codebook
################################################################################
export PYTHONPATH=$LEMS_PYTHONPATH;
echo "PYTHONPATH=" $PYTHONPATH

trial=$2; #grab the trial from the second argument
num_means=20;
bof_dir=$main_dir"/bof_cross_validation/trial_"$trial;
k_means_dir=$bof_dir"/k_means_"$num_means
fraction=0.001;
J=10;  #number of subsamples
max_it=500; #max number of iteration for k-means
nclasses=5;


#learn class_codebook
if  $learn_codebook; then 
  num_cores=$nclasses;
  T1=$(date +%s)
  python2.7 /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_category_codebook/learn_category_codebook_mt.py --bof_dir $bof_dir --k_means_dir $k_means_dir --num_cores $num_cores --num_means $num_means --fraction $fraction --J $J --max_it $max_it --nclasses $nclasses 
  DIFF=$(( $(date +%s) - $T1 ))
  echo "learn_category_codebook_mt.py took $DIFF seconds"
  
  purge

  num_cores=$nclasses;
  T=$(date +%s)
  python2.7 /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_category_codebook/k_means_on_category_means.py --k_means_dir $k_means_dir --num_cores $num_cores --max_it $max_it --nclasses $nclasses 
  DIFF=$(( $(date +%s) - $T ))
  echo "k_means_on_category_means.py took $DIFF seconds"
  
  
  T=$(date +%s)
  python2.7 /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_category_codebook/choose_min_distortion_FM.py --k_means_dir $k_means_dir
  DIFF=$(( $(date +%s) - $T ))
  echo "choose_min_distortion_FM.py took $DIFF seconds"  
  
  DIFF=$(( $(date +%s) - $T1 ))
  time_file=$k_means_dir/"run_time.txt";
  echo "learning the codebook took $DIFF seconds" > $time_file; 
  
fi

purge

################################################################################
# Learn distribution of Taylor categories
################################################################################

class_histograms_dir=$bof_dir"/class_histograms_"$num_means
classification_dir=$bof_dir"/classification_"$num_means
ncategories=$nclasses;

if $learn_categories; then
  num_cores=8; 
  T=$(date +%s) 
  python2.7 /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_categories/learn_categories.py --bof_dir $bof_dir --k_means_dir $k_means_dir --class_histograms_dir $class_histograms_dir --num_cores $num_cores
  DIFF=$(( $(date +%s) - $T ))
  time_file=$class_histograms_dir/"run_time.txt";
  echo "learn_categories.py took $DIFF seconds" > $time_file 
  purge
  
  python2.7 /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_categories/combine_quatization.py --bof_dir $bof_dir --k_means_dir $k_means_dir --class_histograms_dir $class_histograms_dir
  python /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_categories/plot_category_histograms.py --bof_dir $bof_dir --class_histograms_dir $class_histograms_dir
  #python2.7 /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_categories/save_category_scenes_raw.py --bof_dir $bof_dir --num_cores $num_cores
fi


################################################################################
# Classify Taylor 
################################################################################

purge   
     
if $classify; then
  num_cores=8;
  T=$(date +%s) 
  python2.7 /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/classify/classify.py --bof_dir $bof_dir --k_means_dir $k_means_dir --class_histograms_dir $class_histograms_dir --classification_dir $classification_dir --num_cores $num_cores --ncategories $ncategories
  DIFF=$(( $(date +%s) - $T ))
  time_file=$classification_dir/"run_time.txt";
  echo "classify.py took $DIFF seconds" > $time_file   
  python /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/classify/display_classification_results.py --classification_dir $classification_dir --ncategories $nclasses
fi

purge


END=$(date +%s)
DIFF=$(( $END - $START ))
echo "Shell script took $DIFF seconds"
