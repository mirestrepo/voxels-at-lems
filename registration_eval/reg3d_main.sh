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

export PATH=$PATH:/Projects/voxels-at-lems-git/boxm2:/Projects/voxels-at-lems-git/vpcl

echo $PATH

create_scene_from_xml=false;
build_model=false;
render_circle=false;
compute_normals=false;
export_scene=false;
thresh_PLY=false;
flip_normals=false;
compute_descriptors=false;

# create_scene_from_xml=true;
build_model=true;
render_circle=true;
# compute_normals=true;
# flip_normals=true;
# export_scene=true;
# thresh_PLY=true;
# compute_descriptors=true;

#*******************************************************************************************************
# Grab the inputs and set local variables
#*******************************************************************************************************

nargs=$#;

if [ $nargs -eq 2 ]; then
    trial_basename=$1
    trial_number=$2
    refine_chuncks=10
    refine_repeat=3
else
    trial_number=-1
    refine_chuncks=10
    refine_repeat=3
fi

if [ $trial_number -eq -1 ]; then
   root_dir="/Users/isa/Experiments/reg3d_eval/downtown_dan/original"
else
    root_dir="/Users/isa/Experiments/reg3d_eval/downtown_dan/${trial_basename}_${trial_number}"
fi

echo "This is registration_eval/main.sh. Running with the following input arguments"
echo "Root directory:"
echo $root_dir
echo "refine_chuncks:"
echo $refine_chuncks
echo "refine_repeat:"
echo $refine_repeat

model_dirname=model;
boxm2_dir=$root_dir/$model_dirname;
scene_file="scene.xml"
imtype="tif"
device_name="gpu1";

#*******************************************************************************************************
# Create BOXM2 scene parameter file
#*******************************************************************************************************
if $create_scene_from_xml; then
   XML_FILE=$root_dir/scene_info.xml;
   echo "XML_FILE = $XML_FILE"
   boxm2_create_scene_from_XML_info.py --boxm2_dir $boxm2_dir --scene_info $XML_FILE
fi

#*******************************************************************************************************
# Build the Scene
#*******************************************************************************************************
if $build_model; then

    #To build the model we brake the image set in chucks because leaks on the GPU cache can corrupt the scene
    #We are specially conservative while we refine
    #Train and refine
    CHUNKS=$refine_chuncks;


    failed=0;
    failed_r=0;
    failed_u=0;
    for((i=0; i < $refine_repeat; i++))
    do
        echo "Iteration = $i --Refine ON"
        for((chunk=0; chunk < CHUNKS; chunk++))
        do
           log_file="$root_dir/scene_refining_log.txt"
           boxm2_build_model.py -s $root_dir -x "$model_dirname/$scene_file" --imtype "$imtype" -g $device_name -v .06 --initFrame $chunk --skipFrame $CHUNKS --clearApp 1 -p $log_file

           status=${?}
           if [ $status -eq 1 ]; then
                echo "status: $status"
                failed=$(($failed+1))
                failed_r=$(($failed_r+1))
                echo "[Error] Something Failed. Refine ON. Iteration $i, Chunck $chunk. Num errors $failed"
                #exit -1
           fi
           if [ $status -eq 2 ]; then
                failed=$(($failed+1))
                failed_u=$(($failed_u+1))
                echo "[Error] Something Failed. Refine ON. Iteration $i, Chunck $chunk. Num errors $failed"
                #exit -1
           fi
        done
    done

    #Train without refining
    CHUNKS=3
    failed2=0;
    failed_r2=0;
    failed_u2=0;
    for((i=0; i < 1; i++))
    do
        echo "Iteration = $i --Refine OFF"
        for((chunk=0; chunk < CHUNKS; chunk++))
        do
          log_file="$root_dir/scene_updating_log.txt"
           boxm2_build_model.py -s $root_dir -x "$model_dirname/$scene_file" --imtype "$imtype" -g $device_name -v .06 --refineoff 1 --initFrame $chunk --skipFrame $CHUNKS -p $log_file

            status=${?}
            echo "status: $status"
            if [ $status -eq 1 ]; then
                failed2=$(($failed2+1))
                failed_r2=$(($failed_r2+1))
                echo "[Error] Something Failed. Refine OFF. Iteration $i, Chunck $chunk. Num errors $failed2"
                #exit -1
            fi
            if [ $status -eq 2 ]; then
                failed2=$(($failed2+1))
                failed_u2=$(($failed_u2+1))
                echo "[Error] Something Failed. Refine OFF. Iteration $i, Chunck $chunk. Num errors $failed2"
                #exit -1
            fi
        done
     done

    status_file=$root_dir/"train_status.txt";
    echo -e "Refine ON errors: u-$failed_u, r-$failed_r, t-$failed \nRefine OFF errors: u-$failed_u2, r-$failed_r2, t-$failed2" > $status_file;


fi

#*******************************************************************************************************
# Render Viewing Trajectory
#*******************************************************************************************************
if $render_circle; then
    boxm2_render_circle.py -s $root_dir -x "$model_dirname/$scene_file" --imtype "$imtype" -g $device_name
fi

#*******************************************************************************************************
#compute_gauss_gradients
#*******************************************************************************************************
if $compute_normals; then
  T=$(date +%s);
  log_file="$root_dir/compute_normals_log.txt"
  boxm2_compute_normals.py -s $root_dir -x "$model_dirname/$scene_file" -g $device_name -p $log_file

  DIFF=$(( $(date +%s) - $T ))
  time_file=$root_dir/"compute_normals_run_time.txt";
  echo "compute_normals.py took (in seconsd) \n $DIFF" > $time_file;
fi

if $flip_normals; then
  flipped=0;
  attempt=0;
  try=1;
  while [ $try -eq 1 ];
  do
    log_file="$root_dir/flip_normals_log.txt"
    boxm2_flip_normals.py -s $root_dir -x "$model_dirname/$scene_file" -g $device_name --use_sum true -p $log_file
    status=${?}
    echo "Status: $status"
    if [ $status -eq 0 ]; then
      flipped=1;
      echo "Succeeded!"
    fi
    attempt=$(($attempt+1));
    try=$(($((! $flipped)) && $(($attempt<3))));
  done
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
 ./thresh_ply.py -s $root_dir -i "$root_dir/gauss_233_normals.ply" -o "$root_dir/gauss_233_normals_pvn"
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

#*******************************************************************************************************
#Compute Rigid Transformation -- Moved to reg3d_main.py
#*******************************************************************************************************

# if $compute_transformation; then
#   radius=30;
#   percentile=99
#   tgtRoot="/data/reg3d_eval/downtown_dan/original"

# #  ./compute_rigid_transform.py --srcRoot $root_dir --tgtRoot $tgtRoot --basenameIn "gauss_233_normals_pvn" -r $radius -p $percentile -d "FPFH" -v true -exePath $VPCL_EXE_PATH

#     ./register_svd.py --srcRoot $root_dir --tgtRoot $tgtRoot --basenameIn "gauss_233_normals_pvn" -r $radius -p $percentile -d "FPFH" -v true --exePath $VPCL_EXE_PATH
# fi

# if $register_ia; then
#   radius=30;
#   percentile=99
#   tgtRoot="/data/reg3d_eval/downtown_dan/original"
#   ./register_ia.py --srcRoot $root_dir --tgtRoot $tgtRoot --basenameIn "gauss_233_normals_pvn" -r $radius -p $percentile -d "FPFH"
# fi

# if $register_icp; then
#   radius=30;
#   percentile=99
#   tgtRoot="/data/reg3d_eval/downtown_dan/original"
#   ./register_icp.py --srcRoot $root_dir --tgtRoot $tgtRoot --basenameIn "gauss_233_normals_pvn" -r $radius -p $percentile -d "FPFH"
# fi

# if $visualize_reg; then
#   radius=30;
#   percentile=99
#   tgtRoot="/data/reg3d_eval/downtown_dan/original"
#   tgt_cloud="$tgtRoot/gauss_233_normals_pvn_99.ply"
#   src_cloud="$root_dir/FPFH_30/ia_cloud_99.pcd"
# #  src_cloud="$root_dir/FPFH_30/icp_cloud_99.pcd"

#   $VPCL_EXE_PATH/visualize $src_cloud $tgt_cloud
# fi
