#!/bin/bash
"""
Created on August 8, 2012

@author:Isabel Restrepo

A script that encapsulates all steps for building the scenes
needed for registration experiments in the PVM
"""


#*******************************************************************************************************
# SET UP ENVIROMENT
#*******************************************************************************************************
CONFIGURATION=Release;
#CONFIGURATION=Debug;

EXE_PATH=/Projects/vxl/bin/$CONFIGURATION/contrib/brl/bseg/boxm2/ocl/exe
VPCL_EXE_PATH=/Projects/vpcl/bin_make/$CONFIGURATION/bin
export PYTHONPATH=/Projects/vxl/bin/$CONFIGURATION/lib:/Projects/vxl/src/contrib/brl/bseg/boxm2/pyscripts:/Projects/vxl/src/contrib/brl/bseg/boxm2/pyscripts/change:/Projects/vpcl/bin_make/$CONFIGURATION/lib:/Projects/vpcl/vpcl/pyscripts:/Projects/voxels-at-lems-git/boxm2:$PYTHONPATH

export PATH=$PATH:/Projects/voxels-at-lems-git/boxm2:/Projects/voxels-at-lems-git/vpcl:/Projects/voxels-at-lems-git/ply_util


echo $PATH

compute_normals=false;
export_scene=false;
thresh_PLY=false;
flip_normals=false;
compute_descriptors=false;


compute_normals=true;
flip_normals=true;
export_scene=true;
thresh_PLY=true;
compute_descriptors=true;

#*******************************************************************************************************
# Grab the inputs and set local variables
#*******************************************************************************************************

nargs=$#;

echo $nargs

if [ $nargs -eq 3 ]
then
    root_basename=$1
    trial_basename=$2
    trial_number=$3
elif [ $nargs -eq 1 ]
then
    root_basename=$1
    trial_number=-1
    echo "Here too"
else
    echo "Wrong number of arguments, exiting"
    exit -1
fi

if [ $trial_number -eq -1 ]; then
   root_dir="/Users/isa/Experiments/reg3d_eval/${root_basename}/original"
else
   root_dir="/Users/isa/Experiments/reg3d_eval/${root_basename}/${trial_basename}_${trial_number}"
fi

echo "This is registration_eval/main.sh. Running with the following input arguments"
echo "Root directory:"
echo $root_dir

model_dirname=model;
boxm2_dir=$root_dir/$model_dirname;
scene_file="scene.xml"
device_name="gpu1";

#*******************************************************************************************************
#compute_gauss_gradients
#*******************************************************************************************************
if $compute_normals; then
  T=$(date +%s);
  log_file="$root_dir/compute_normals_log.log"
  boxm2_compute_normals.py -s $root_dir -x "$model_dirname/$scene_file" -g $device_name -p $log_file

  DIFF=$(( $(date +%s) - $T ))
  time_file=$root_dir/"compute_normals_run_time.txt";
  echo "compute_normals.py took (in seconsd) \n $DIFF" > $time_file;
fi

if $flip_normals; then
    flipped=0;
    log_file="$root_dir/flip_normals_log.log"
    boxm2_flip_normals.py -s $root_dir -x "$model_dirname/$scene_file" -g $device_name --use_sum true -p $log_file
    status=${?}
    echo "Status: $status"
    if [ $status -eq 0 ]; then
      flipped=1;
      echo "Succeeded!"
    else
      echo "Failed to flip normals, quitting"
      exit -1
    fi
fi

#*******************************************************************************************************
#export to PLY
#*******************************************************************************************************
if $export_scene; then
 boxm2_export_scene_to_PLY.py -s $root_dir -x "$model_dirname/$scene_file" -g $device_name --exportFile "gauss_233_normals.ply" --p_thresh 0.1
fi

#*******************************************************************************************************
#Threshold PLY --thresholds are specified within the scrip
#*******************************************************************************************************
if $thresh_PLY; then
 thresh_ply.py -i "$root_dir/gauss_233_normals.ply" -o "$root_dir/gauss_233_normals_pvn"
fi

#*******************************************************************************************************
#Compute Descriptors
#*******************************************************************************************************
if $compute_descriptors; then
  njobs=8;
  radius=30;
  percentile=99
  vpcl_compute_omp_descriptors.py -s $root_dir --basenameIn "gauss_233_normals_pvn" -r $radius -p $percentile -d "FPFH" -j $njobs -v true
  vpcl_compute_omp_descriptors.py -s $root_dir --basenameIn "gauss_233_normals_pvn" -r $radius -p $percentile -d "SHOT" -j $njobs -v true
fi
