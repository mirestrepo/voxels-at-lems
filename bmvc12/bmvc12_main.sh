 #!/bin/bash
#*******************************************************************************************************
#Created on Mon April 23, 2011
#
#author:Isabel Restrepo
#
#A script that encapsulates all steps needed to create a boxm2 scene from bundler output.
#You need to set up the main path, where there should be a folder called frames original with all original images (those used by bundler).
#In the top directory there should also be bundler output file bundleX.out where X is the focal length used by bundler.
#*******************************************************************************************************

#*******************************************************************************************************
# SET UP ENVIROMENT
#*******************************************************************************************************
CONFIGURATION=Release;
export PYTHONPATH=/Projects/vxl/bin/$CONFIGURATION/lib:/Projects/vxl/src/contrib/brl/bseg/boxm2/pyscripts:/Projects/vxl/src/contrib/brl/bseg/boxm2/pyscripts/change:$PYTHONPATH
SCRIPTS_PATH=/Projects/voxels-at-lems-git;

#*******************************************************************************************************
# DEFINE STEPS TO BE RUN
#*******************************************************************************************************
export_objects=false;
export_scene=false;
compute_normals_export_objects=false;
compute_normals=false;


#export_objects=true;
#export_scene=true;
#compute_normals_export_objects=true;
compute_normals=true;




#******************************************************************************************************* 
# DEFINE PATHS
#*******************************************************************************************************
#Top directory containing frams_original
#root_dir="/volumes/vision/video/helicopter_providence/3d_models_3_12/site_1";
site_number=$1;
root_dir="/data/helicopter_providence_3_12/site_${site_number}";

# directory where boxm2 scene is stored
model_dirname="model";
boxm2_dir=$root_dir/$model_dirname;


#*******************************************************************************************************
#compute_gauss_gradients
#*******************************************************************************************************
if $export_objects; then
  scene_file="scene.xml"
  device_name="gpu1";
  category=$2;
  dir_in="/Volumes/vision/video/helicopter_providence/ground_truth_3_12/ground_truth_original/site${site_number}/${category}";
  dir_out="/data/helicopter_providence_3_12/site_${site_number}/objects/${category}"
  python ./export_object_to_PLY.py -s $root_dir -x "$model_dirname/$scene_file" -g $device_name --dir_in $dir_in --dir_out $dir_out --p_thresh 0.05
fi


if $export_scene; then
  scene_file="scene.xml"
  device_name="gpu1";
  python ./export_scene_to_PLY.py -s $root_dir -x "$model_dirname/$scene_file" -g $device_name --exportFile "gauss_233_normals.ply" --p_thresh 0.05
fi

#*******************************************************************************************************
#compute_gauss_gradients
#*******************************************************************************************************
if $compute_normals_export_objects; then
  T=$(date +%s);
  scene_file="scene.xml"
  device_name="gpu1";
  category=$2;
  dir_in="/Volumes/vision/video/helicopter_providence/ground_truth_3_12/ground_truth_original/site${site_number}/${category}";
  dir_out="/data/helicopter_providence_3_12/site_${site_number}/objects/${category}"
  log_file="./logs/log_${T}.log"
  python ./compute_normals_export_objects.py -s $root_dir -x "$model_dirname/$scene_file" -g $device_name --dir_in $dir_in --dir_out $dir_out --use_sum true --p_thresh 0.1 -p $log_file
  DIFF=$(( $(date +%s) - $T ))
  time_file=$root_dir/"compute_normals_run_time.txt";
  echo "compute_normals_export_obects.py took (in seconsd) \n $DIFF" > $time_file; 
fi


#*******************************************************************************************************
#compute_gauss_gradients
#*******************************************************************************************************
if $compute_normals; then
  T=$(date +%s);
  scene_file="scene.xml"
  device_name="gpu1";
  log_file="./logs/log_${T}.log"
  python ./compute_normals.py -s $root_dir -x "$model_dirname/$scene_file" -g $device_name --use_sum true -p $log_file
  DIFF=$(( $(date +%s) - $T ))
  time_file=$root_dir/"compute_normals_run_time.txt";
  echo "compute_normals.py took (in seconsd) \n $DIFF" > $time_file; 
fi