 #!/bin/bash
"""
Created on Mon Feb 14, 2011

@author:Isabel Restrepo

A script that encapsulates all steps needed to learn and classify based on corners features
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


#steps to run:
#-------------


#init all steps to false
compute_corner_measure=false;
compute_beaudet_measure=false;
threshold_corner_measure=false;
init_k_means=false;
run_k_means=false;
init_categories_info=false;   #inits xml and category_scene cells
learn_categories=false;
classify=false;

#----Set to true what you want to run---------
#compute_corner_measure=true;
#compute_beaudet_measure=true;
threshold_corner_measure=true;
init_k_means=true;  #Make sure the bof_info.xml is accurate 
run_k_means=true;
learn_categories=true;  #Make sure the bof_categories_info.xml is accurate 
classify=true;


################################################################################
# Set main directories - all other dirs are relative to this
main_dir="/Users/isa/Experiments/BOF/helicopter_providence";
################################################################################



################################################################################
# Compute harris measure and filter top % responses
################################################################################

taylor_dir=$main_dir"/taylor/global_taylor";
#param_dir=$main_dir"/corners/k_3";
param_dir=$main_dir"/beaudet_corners";
corners_dir=$param_dir"/global_corners";

if $compute_corner_measure; then

   export PYTHONPATH=$VXL_PYTHONPATH;
   echo "PYTHONPATH=" $PYTHONPATH
  
   num_cores=4;
   python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/corners/global_corners/compute_harris_measure.py --taylor_dir $taylor_dir --corners_dir $corners_dir --num_cores $num_cores
   num_cores=8;
   python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/corners/global_corners/explore_harris_measure_scenes.py --taylor_dir $taylor_dir --corners_dir $corners_dir --num_cores $num_cores
fi


if $compute_beaudet_measure; then

   export PYTHONPATH=$VXL_PYTHONPATH;
   echo "PYTHONPATH=" $PYTHONPATH
  
   num_cores=4;
   python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/corners/global_corners/compute_beaudet_measure.py --taylor_dir $taylor_dir --corners_dir $corners_dir --num_cores $num_cores
   num_cores=8;
   python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/corners/global_corners/explore_harris_measure_scenes.py --taylor_dir $taylor_dir --corners_dir $corners_dir --num_cores $num_cores
fi

if $threshold_corner_measure; then

   export PYTHONPATH=$VXL_PYTHONPATH;
   echo "PYTHONPATH=" $PYTHONPATH
  
   num_cores=8;
   python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/corners/global_corners/threshold_corners.py --taylor_dir $taylor_dir --corners_dir $corners_dir --num_cores $num_cores
fi


export PYTHONPATH=$LEMS_PYTHONPATH;
echo "PYTHONPATH=" $PYTHONPATH


for num_thresh in 50
do
    
    bof_dir=$param_dir"/bof/thresh_"$num_thresh;

    for num_means in 20
    do
      init_k_means_dir=$bof_dir"/init_k_means_"$num_means
      k_means_dir=$bof_dir"/k_means_"$num_means
      fraction_subsamples=0.01;
      J=10;  #number of subsamples
      max_it=500; #max number of iteration for k-means


      ################################################################################
      # Learn corners codebook
      ################################################################################

      #Init K-means
      if  $init_k_means; then
      
      
          T=$(date +%s)
          python /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_codebook/refined_init_k_means/rnd_sample_init_k_means.py --bof_dir $bof_dir --init_k_means_dir $init_k_means_dir --num_means $num_means
          DIFF=$(( $(date +%s) - $T ))
          echo "k_means_on_rnd_subsamples.py took $DIFF seconds"
          
          num_cores=8;
          T=$(date +%s)
          python /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_codebook/refined_init_k_means/k_means_on_rnd_subsamples.py --bof_dir $bof_dir --init_k_means_dir $init_k_means_dir --fraction_subsamples $fraction_subsamples --max_it $max_it --num_subsamples $J --num_cores $num_cores
          DIFF=$(( $(date +%s) - $T ))
          echo "k_means_on_rnd_subsamples.py took $DIFF seconds"
          
          T=$(date +%s)
          python /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_codebook/refined_init_k_means/k_means_on_CM_means.py --init_k_means_dir $init_k_means_dir --num_cores $num_cores --max_it $max_it
          DIFF=$(( $(date +%s) - $T ))
          echo "k_means_on_CM_means.py took $DIFF seconds"

          T=$(date +%s)
          python /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_codebook/refined_init_k_means/choose_min_distortion_FM.py --init_k_means_dir $init_k_means_dir --k_means_dir $k_means_dir
          DIFF=$(( $(date +%s) - $T ))
          echo "choose_min_distortion_FM.py took $DIFF seconds"
      fi
      
      purge
      
      #K-means
      if $run_k_means; then
         num_cores=8;
         T=$(date +%s)
         python /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_codebook/k_means/k_means_train.py --bof_dir $bof_dir --k_means_dir $k_means_dir --max_it $max_it --num_cores $num_cores
         DIFF=$(( $(date +%s) - $T ))
         echo "k_means_train.py took $DIFF seconds"
         
         
         num_cores=8;  
         python /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_codebook/k_means/k_means_on_CM_means.py --k_means_dir $k_means_dir --num_cores $num_cores --max_it $max_it
         python /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_codebook/k_means/choose_min_distortion_FM.py --k_means_dir $k_means_dir

      fi
      
      purge

    ################################################################################
    # Learn distribution of corners categories
    ################################################################################
      class_histograms_dir=$bof_dir"/class_histograms_"$num_means

      if $learn_categories; then
        num_cores=8; 
        T=$(date +%s) 
        python /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_categories/learn_categories.py --bof_dir $bof_dir --k_means_dir $k_means_dir --class_histograms_dir $class_histograms_dir --num_cores $num_cores
        DIFF=$(( $(date +%s) - $T ))
        echo "learn_categories.py took $DIFF seconds"
        python /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_categories/combine_quatization.py --bof_dir $bof_dir --k_means_dir $k_means_dir --class_histograms_dir $class_histograms_dir
        python /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/learn_categories/plot_category_histograms.py --bof_dir $bof_dir --class_histograms_dir $class_histograms_dir
        #python /Projects/voxels-at-lems/scripts/dbrec3d/bof/corners/learn_categories/save_category_scenes_raw.py --bof_dir $bof_dir --num_cores $num_cores
      fi

      purge
      
    ################################################################################
    #Classify corners
    ################################################################################

      if $classify; then
        num_cores=8;  
        ncategories=5;
        classification_dir=$bof_dir"/classification_"$num_means
        python /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/classify/classify.py --bof_dir $bof_dir --k_means_dir $k_means_dir --class_histograms_dir $class_histograms_dir --classification_dir $classification_dir --num_cores $num_cores --ncategories $ncategories
        python /Projects/voxels-at-lems/scripts/dbrec3d/bof/taylor/classify/display_classification_results.py --classification_dir $classification_dir --ncategories $ncategories
      fi
      
      purge

    done #num_means
    
done #num_thresh

END=$(date +%s)
DIFF=$(( $END - $START ))
echo "Shell script took $DIFF seconds"
