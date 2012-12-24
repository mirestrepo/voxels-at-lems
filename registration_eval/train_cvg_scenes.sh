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

create_scene_from_xml=true;
build_model=true;
render_circle=true;

#*******************************************************************************************************
# Grab the inputs and set local variables
#*******************************************************************************************************

nargs=$#;

echo $nargs

if [ $nargs -eq 4 ]
then
    flight=$1
    site=$2
    refine_chuncks=$3
    refine_repeat=$4
else
    echo "Wrong number of arguments, exiting"
    exit -1
fi

# flight=5
# site=7

root_dir="/Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight${flight}_sites/site_${site}"

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
device_name="gpu1";
imtype="png"

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
           log_file="$root_dir/scene_refining_log.log"
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

    Train without refining
    CHUNKS=10
    failed2=0;
    failed_r2=0;
    failed_u2=0;
    for((i=0; i < 1; i++))
    do
        echo "Iteration = $i --Refine OFF"
        for((chunk=0; chunk < CHUNKS; chunk++))
        do
          log_file="$root_dir/scene_updating_log.log"
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
    boxm2_render_circle.py -s $root_dir -x "$model_dirname/$scene_file" --imtype "$imtype" -g $device_name --skipFrame 5
fi
