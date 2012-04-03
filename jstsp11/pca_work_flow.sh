#!/bin/bash

#Created on Mon Dec 12, 2011
#Author:Isabel Restrepo
#USAGE: pca_work_flow.sh [-r or -d for release or debug][ integer for trial # ]
#DESCRIPTION:A script that encapsulates all steps needed to learn and classify based on pca features
#This script was written with the purpose of running different trials of the learning/classification pipeline 
#so that results can be shown as the average of the trials


START=$(date +%s)

if [ $1 = "-r" ] ; then
  LEMS_PYTHONPATH=/Projects/lemsvxl/bin_xcode4/Release/lib_temp
  VXL_PYTHONPATH=/Projects/vxl/bin_xcode4/Release/lib_temp
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
init_global_pca=true;  #init auxiliary scenes and cell_lenghts
learn_pca=true;
project_pca=true;
#***************Stop here you need to make sure the bof_info.xml is accurate************************************#
learn_codebook=true;
#***************Stop here you need to make sure the bof_categories_info.xml is accurate**************************# 
learn_categories=true;
classify=true;
clean_files=true;



#################################################################################################################################
#steps to run - set to true to run - note that the work flow can't be run at once because the user needs to complete the xml file
#################################################################################################################################
init_global_pca=false;  #init auxiliary scenes and cell_lenghts
learn_pca=false;
project_pca=false;
#***************Stop here you need to make sure the bof_info.xml is accurate************************************#
learn_codebook=false;
#***************Stop here you need to make sure the bof_categories_info.xml is accurate**************************# 
learn_categories=false;
#classify=false;
clean_files=false;


#################################################################################################################################
trial=$2; #grab the trial from the second argument
main_dir="/Users/isa/Experiments/BOF/helicopter_providence/pca_cross_validation/trial_"$trial;
#################################################################################################################################

################################################################################
#. Learn PCA kernels and obtain 10-d projection scenes
################################################################################
pca_dir=$main_dir"/global_pca";
bof_dir=$main_dir"/bof";
num_cores=8;


if  $init_global_pca; then

    export PYTHONPATH=$VXL_PYTHONPATH;
    echo "PYTHONPATH=" $PYTHONPATH

    python2.7 /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/pca_global/init_global_pca.py --pca_dir $pca_dir --num_cores $num_cores

fi


if  $learn_pca; then

		export PYTHONPATH=$LEMS_PYTHONPATH;
		echo "PYTHONPATH=" $PYTHONPATH
    T=$(date +%s);
    python2.7 /Projects/voxels-at-lems/scripts/dbrec3d/bof/pca/compute_sample_statistics.py --pca_dir $pca_dir --bof_dir $bof_dir --num_cores $num_cores
    DIFF=$(( $(date +%s) - $T ))
    time_file=$pca_dir/"compute_sample_statistics_run_time.txt";
    echo "compute_sample_statistics.py took $DIFF seconds" > $time_file 

    export PYTHONPATH=$VXL_PYTHONPATH;
    echo "PYTHONPATH=" $PYTHONPATH;
    python2.7 /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/pca_global/combine_stats_pairwise.py --pca_dir $pca_dir --num_cores $num_cores
    python2.7 /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/pca_global/set_up_pca.py --pca_dir $pca_dir
    
fi


if $project_pca; then 
    num_cores=8;
    export PYTHONPATH=$VXL_PYTHONPATH;
    echo "PYTHONPATH=" $PYTHONPATH;
    T=$(date +%s);
    python2.7 /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/pca_global/pca_project.py --pca_dir $pca_dir --num_cores $num_cores
    DIFF=$(( $(date +%s) - $T ))
    time_file=$pca_dir/"pca_project_run_time.txt";
    echo "pca_project.py took $DIFF seconds" > $time_file; 
    
fi

################################################################################
# Learn pca codebook
################################################################################
export PYTHONPATH=$LEMS_PYTHONPATH;
echo "PYTHONPATH=" $PYTHONPATH

num_means=20;
k_means_dir=$bof_dir"/k_means_"$num_means
fraction=0.001;
J=10;  #number of subsamples
max_it=500; #max number of iteration for k-means
nclasses=5;


#learn class_codebook
if  $learn_codebook; then 
  num_cores=$nclasses;
  T1=$(date +%s)
  python2.7 /Projects/voxels-at-lems/scripts/dbrec3d/bof/general/learn_category_codebook/learn_category_codebook_mt.py --bof_dir $bof_dir --k_means_dir $k_means_dir --num_cores $num_cores --num_means $num_means --fraction $fraction --J $J --max_it $max_it --nclasses $nclasses 
  DIFF=$(( $(date +%s) - $T1 ))
  echo "learn_category_codebook_mt.py took $DIFF seconds"
  


  num_cores=$nclasses;
  T=$(date +%s)
  python2.7 /Projects/voxels-at-lems/scripts/dbrec3d/bof/general/learn_category_codebook/k_means_on_category_means.py --k_means_dir $k_means_dir --num_cores $num_cores --max_it $max_it --nclasses $nclasses 
  DIFF=$(( $(date +%s) - $T ))
  echo "k_means_on_category_means.py took $DIFF seconds"
  
  
  T=$(date +%s)
  python2.7 /Projects/voxels-at-lems/scripts/dbrec3d/bof/general/learn_category_codebook/choose_min_distortion_FM.py --k_means_dir $k_means_dir
  DIFF=$(( $(date +%s) - $T ))
  echo "choose_min_distortion_FM.py took $DIFF seconds"  
  
  DIFF=$(( $(date +%s) - $T1 ))
  time_file=$k_means_dir/"run_time.txt";
  echo "learning the codebook took $DIFF seconds" > $time_file; 
  
fi



################################################################################
# Learn distribution of pca categories
################################################################################

class_histograms_dir=$bof_dir"/class_histograms_"$num_means
classification_dir=$bof_dir"/classification_"$num_means
ncategories=$nclasses;

if $learn_categories; then
  num_cores=8; 
  T=$(date +%s) 
  python2.7 /Projects/voxels-at-lems/scripts/dbrec3d/bof/general/learn_categories/learn_categories.py --bof_dir $bof_dir --k_means_dir $k_means_dir --class_histograms_dir $class_histograms_dir --num_cores $num_cores
  DIFF=$(( $(date +%s) - $T ))
  time_file=$class_histograms_dir/"run_time.txt";
  echo "learn_categories.py took $DIFF seconds" > $time_file 
  
  python2.7 /Projects/voxels-at-lems/scripts/dbrec3d/bof/pca/learn_categories/combine_quatization.py --bof_dir $bof_dir --k_means_dir $k_means_dir --class_histograms_dir $class_histograms_dir
  python /Projects/voxels-at-lems/scripts/dbrec3d/bof/pca/learn_categories/plot_category_histograms.py --bof_dir $bof_dir --class_histograms_dir $class_histograms_dir
  #python2.7 /Projects/voxels-at-lems/scripts/dbrec3d/bof/pca/learn_categories/save_category_scenes_raw.py --bof_dir $bof_dir --num_cores $num_cores
fi


################################################################################
# Classify pca 
################################################################################
    
if $classify; then
  num_cores=8;
  T=$(date +%s) 
  #python2.7 /Projects/voxels-at-lems/scripts/dbrec3d/bof/general/classify/classify.py --bof_dir $bof_dir --k_means_dir $k_means_dir --class_histograms_dir $class_histograms_dir --classification_dir $classification_dir --num_cores $num_cores --ncategories $ncategories
  DIFF=$(( $(date +%s) - $T ))
  time_file=$classification_dir/"run_time.txt";
  echo "classify.py took $DIFF seconds" > $time_file   
  python /Projects/voxels-at-lems/scripts/dbrec3d/bof/general/classify/display_classification_results.py --classification_dir $classification_dir --ncategories $nclasses
fi

################################################################################
# Clean Projection Files
################################################################################
if $clean_files; then
  rm -rf $main_dir"/aux_dirs"
  purge
fi



END=$(date +%s)
DIFF=$(( $END - $START ))
echo "Shell script took $DIFF seconds"
