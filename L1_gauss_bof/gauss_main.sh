#!/bin/bash
"""
Created on Mon Feb 14, 2011

@author:Isabel Restrepo

A script that encapsulates all steps needed to learn and classify based on L1 normalized gaussian features
f0, fx, fy, fz, fxx, fyy, fzz, fxy, fxz, fyz
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
compute_expected_scene=false;
init_taylor_global=false;
project_taylor=false;
init_bof_from_taylor_info=false;
#***************Stop here you need to make sure the bof_info.xml is accurate************************************#
init_k_means=false;
run_k_means=false;
init_categories_info=false;
#***************Stop here you need to make sure the bof_categories_info.xml is accurate**************************# 
learn_categories=false;
classify=false;




init_taylor_global=true;
project_taylor=true;
#init_bof_from_taylor_info=true;
#***************Stop here you need to make sure the bof_info.xml is accurate************************************#
#init_k_means=true;
#run_k_means=true;
#init_categories_info=true;
#***************Stop here you need to make sure the bof_categories_info.xml is accurate**************************# 
#learn_categories=true;
#classify=true;




#################################################################################################################################
#main directories - all other dirs are relative to this
main_dir="/Users/isa/Experiments/BOF/helicopter_providence/L1_gauss";
#################################################################################################################################





################################################################################
#1.  Obtain mean scene
################################################################################
if $compute_expected_scene; then

  export PYTHONPATH=$VXL_PYTHONPATH;
  echo "PYTHONPATH=" $PYTHONPATH

  # an xml file containing a list a model directories and model names
  scenes_info=$main_dir"/boxm_mog3_grey_scenes.xml" 
  num_cores=1;
  python '/Projects/voxels-at-lems/scripts/boxm/compute_expected_color_batch.py' --scenes_info $scenes_info --num_cores $num_cores

fi
  


################################################################################
#2b. Run Taylor kernels and 10-d basis scenes
################################################################################
taylor_dir=$main_dir"/global_taylor";
aux_scene_dir=$main_dir"/aux_dirs";

if $init_taylor_global; then
    export PYTHONPATH=$VXL_PYTHONPATH;
    echo "PYTHONPATH=" $PYTHONPATH

    python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/taylor/taylor_global/init_global_taylor.py --taylor_dir $taylor_dir
fi

if  $project_taylor; then

    export PYTHONPATH=$VXL_PYTHONPATH;
    echo "PYTHONPATH=" $PYTHONPATH

    num_cores=4;
    python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/taylor/taylor_global/compute_taylor_coefficients.py --taylor_dir $taylor_dir --num_cores $num_cores
    python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/taylor/taylor_global/extract_coefficient.py --taylor_dir $taylor_dir --aux_scene_dir $aux_scene_dir
fi




export PYTHONPATH=$LEMS_PYTHONPATH;
echo "PYTHONPATH=" $PYTHONPATH


for num_means in 20
do

    ################################################################################
    #3b. Learn Taylor codebook
    ################################################################################
    bof_dir=$main_dir"/bof";
    init_k_means_dir=$bof_dir"/init_k_means_"$num_means
    k_means_dir=$bof_dir"/k_means_"$num_means
    fraction_subsamples=0.001;
    J=10;  #number of subsamples
    max_it=500; #max number of iteration for k-means

    #init bof xml file
    if $init_bof_from_taylor_info; then
       python '/Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_codebook/refined_init_k_means/init_bof_info.py' --taylor_dir $taylor_dir --bof_dir $bof_dir --num_means $num_means 
    fi

    #3.a.a Init K-means
    if  $init_k_means; then
        python '/Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_codebook/refined_init_k_means/rnd_sample_init_k_means.py' --bof_dir $bof_dir --init_k_means_dir $init_k_means_dir --num_means $num_means
        
        num_cores=4;
        python '/Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_codebook/refined_init_k_means/k_means_on_rnd_subsamples.py' --bof_dir $bof_dir --init_k_means_dir $init_k_means_dir --fraction_subsamples $fraction_subsamples --max_it $max_it --num_subsamples $J --num_cores $num_cores
        
        num_cores=4;
        python '/Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_codebook/refined_init_k_means/k_means_on_CM_means.py' --init_k_means_dir $init_k_means_dir --num_mean_files $J --num_cores $num_cores --max_it $max_it
        
        python '/Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_codebook/refined_init_k_means/choose_min_distortion_FM.py' --init_k_means_dir $init_k_means_dir --k_means_dir $k_means_dir --num_mean_files $J 
        
        best_init_mean=$?;    
        echo "The Best mean Index"; echo $best_init_mean;
    fi

    #3.a.b K-means
    if $run_k_means; then
       num_cores=4;
       python '/Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_codebook/k_means/k_means_train.py' --bof_dir $bof_dir --k_means_dir $k_means_dir --max_it $max_it --num_cores $num_cores
       
       num_cores=8;  
       python '/Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_codebook/k_means/k_means_on_CM_means.py' --k_means_dir $k_means_dir --num_cores $num_cores --max_it $max_it
       
       python '/Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_codebook/k_means/choose_min_distortion_FM.py' --k_means_dir $k_means_dir
       best_init_mean=$?;    

    fi
       
    ################################################################################
    #4b. Learn distribution of Taylor categories
    ################################################################################       
    class_histograms_dir=$bof_dir"/class_histograms_"$num_means
    classification_dir=$bof_dir"/classification_"$num_means
    ncategories=5;
    
    if $learn_categories; then
      python /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_categories/plot_category_histograms.py --bof_dir $bof_dir --class_histograms_dir $class_histograms_dir
    fi
    
    ################################################################################
    #6b. Classify Taylor 
    ################################################################################
    
    if $classify; then
      python /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/classify/display_classification_results.py --classification_dir $classification_dir --ncategories $ncategories
    fi

done









END=$(date +%s)
DIFF=$(( $END - $START ))
echo "Shell script took $DIFF seconds"