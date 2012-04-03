 #!/bin/bash
"""
Created on Mon Feb 14, 2011

@author:Isabel Restrepo

A script that encapsulates all steps needed to learn and classify based on pca features
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


#steps to run
init_global_pca=false;
learn_pca=false;
project_pca=false;

init_bof_from_pca_info=false;

#Stop here you need to make sure the bof_info.xml is accurate 
init_k_means=false;
run_k_means=false;


init_categories_info=false;   #inits xml and category_scene cells

#Stop here you need to make sure the bof_categories_info.xml is accurate 
learn_categories=false;
classify=true;

#main directories - all other dirs are relative to this
main_dir="/Users/isa/Experiments/BOF/helicopter_providence/pca";




################################################################################
#2a. Learn PCA kernels and obtain 10-d projection scenes
################################################################################
pca_dir=$main_dir"/global_pca";

if  $init_global_pca; then

    export PYTHONPATH=$VXL_PYTHONPATH;
    echo "PYTHONPATH=" $PYTHONPATH

    python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/pca_global/init_global_pca.py --pca_dir $pca_dir
fi


if  $learn_pca; then

    export PYTHONPATH=$VXL_PYTHONPATH;
    echo "PYTHONPATH=" $PYTHONPATH;

    num_cores=3;
    python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/pca_global/compute_stats_pass0.py --pca_dir $pca_dir --num_cores $num_cores
    num_cores=10;
    python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/pca_global/combine_stats_pairwise.py --pca_dir $pca_dir --num_cores $num_cores
    python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/pca_global/set_up_pca.py --pca_dir $pca_dir
fi

if $project_pca; then
   
    export PYTHONPATH=$VXL_PYTHONPATH;
    echo "PYTHONPATH=" $PYTHONPATH;
    num_cores=4;
    python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/PCA/pca_global/pca_project.py --pca_dir $pca_dir --num_cores $num_cores
fi


################################################################################
#3a. Learn PCA codebook
################################################################################

export PYTHONPATH=$LEMS_PYTHONPATH;
echo "PYTHONPATH=" $PYTHONPATH

for num_means in 10 20 50 100 200 
do
  bof_dir=$main_dir"/bof";
  init_k_means_dir=$bof_dir"/init_k_means_"$num_means
  k_means_dir=$bof_dir"/k_means_"$num_means
  fraction_subsamples=0.001;
  J=10;  #number of subsamples
  max_it=500; #max number of iteration for k-means

  #init bof xml file
  if $init_bof_from_pca_info; then
     python /Projects/voxels-at-lems/scripts/dbrec3d/bof/pca/learn_codebook/refined_init_k_means/init_bof_info.py --pca_dir $pca_dir --bof_dir $bof_dir --num_means $num_means 
  fi

  #3.a.a Init K-means
  if  $init_k_means; then
  
  
      T=$(date +%s)
      python /Projects/voxels-at-lems/scripts/dbrec3d/bof/pca/learn_codebook/refined_init_k_means/rnd_sample_init_k_means.py --bof_dir $bof_dir --init_k_means_dir $init_k_means_dir --num_means $num_means
      DIFF=$(( $(date +%s) - $T ))
      echo "k_means_on_rnd_subsamples.py took $DIFF seconds"
      
      num_cores=8;
      T=$(date +%s)
      python /Projects/voxels-at-lems/scripts/dbrec3d/bof/pca/learn_codebook/refined_init_k_means/k_means_on_rnd_subsamples.py --bof_dir $bof_dir --init_k_means_dir $init_k_means_dir --fraction_subsamples $fraction_subsamples --max_it $max_it --num_subsamples $J --num_cores $num_cores
      DIFF=$(( $(date +%s) - $T ))
      echo "k_means_on_rnd_subsamples.py took $DIFF seconds"
      
  
      python /Projects/voxels-at-lems/scripts/dbrec3d/bof/pca/learn_codebook/refined_init_k_means/k_means_on_CM_means.py --init_k_means_dir $init_k_means_dir --num_cores $num_cores --max_it $max_it
      
      
      python /Projects/voxels-at-lems/scripts/dbrec3d/bof/pca/learn_codebook/refined_init_k_means/choose_min_distortion_FM.py --init_k_means_dir $init_k_means_dir --k_means_dir $k_means_dir
      
  fi
  
  
  #3.a.b K-means
  if $run_k_means; then
     num_cores=8;
     T=$(date +%s)
     python /Projects/voxels-at-lems/scripts/dbrec3d/bof/pca/learn_codebook/k_means/k_means_train.py --bof_dir $bof_dir --k_means_dir $k_means_dir --max_it $max_it --num_cores $num_cores
     DIFF=$(( $(date +%s) - $T ))
     echo "k_means_train.py took $DIFF seconds"
     
     
     num_cores=8;  
     python /Projects/voxels-at-lems/scripts/dbrec3d/bof/pca/learn_codebook/k_means/k_means_on_CM_means.py --k_means_dir $k_means_dir --num_cores $num_cores --max_it $max_it
     
     python /Projects/voxels-at-lems/scripts/dbrec3d/bof/pca/learn_codebook/k_means/choose_min_distortion_FM.py --k_means_dir $k_means_dir

  fi
  
  

################################################################################
#4a. Learn distribution of PCA categories
################################################################################
  if $init_categories_info; then
     python /Projects/voxels-at-lems/scripts/dbrec3d/bof/pca/learn_categories/init_category_info.py --bof_dir $bof_dir
  fi

  class_histograms_dir=$bof_dir"/class_histograms_"$num_means

  if $learn_categories; then
    num_cores=8; 
    T=$(date +%s) 
    python /Projects/voxels-at-lems/scripts/dbrec3d/bof/pca/learn_categories/learn_categories.py --bof_dir $bof_dir --k_means_dir $k_means_dir --class_histograms_dir $class_histograms_dir --num_cores $num_cores
    DIFF=$(( $(date +%s) - $T ))
    echo "learn_categories.py took $DIFF seconds"
    python /Projects/voxels-at-lems/scripts/dbrec3d/bof/pca/learn_categories/combine_quatization.py --bof_dir $bof_dir --k_means_dir $k_means_dir --class_histograms_dir $class_histograms_dir
    python /Projects/voxels-at-lems/scripts/dbrec3d/bof/pca/learn_categories/plot_category_histograms.py --bof_dir $bof_dir --class_histograms_dir $class_histograms_dir
    #python /Projects/voxels-at-lems/scripts/dbrec3d/bof/pca/learn_categories/save_category_scenes_raw.py --bof_dir $bof_dir --num_cores $num_cores
  fi


################################################################################
#5a. Classify PCA
################################################################################

  if $classify; then
    num_cores=8;  
    ncategories=5;
    classification_dir=$bof_dir"/classification_"$num_means
    python /Projects/voxels-at-lems/scripts/dbrec3d/bof/pca/classify/classify.py --bof_dir $bof_dir --k_means_dir $k_means_dir --class_histograms_dir $class_histograms_dir --classification_dir $classification_dir --num_cores $num_cores --ncategories $ncategories
    python /Projects/voxels-at-lems/scripts/dbrec3d/bof/pca/classify/display_classification_results.py --classification_dir $classification_dir --ncategories $ncategories
  fi

done

END=$(date +%s)
DIFF=$(( $END - $START ))
echo "Shell script took $DIFF seconds"
