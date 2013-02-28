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

create_scene_from_bundler=false;

create_scene_from_bundler=true;


#*******************************************************************************************************
# Grab the inputs and set local variables
#*******************************************************************************************************

nargs=$#;

echo $nargs

if [ $nargs -eq 2 ]
then
    flight=$1
    site=$2
else
    echo "Wrong number of arguments, exiting"
    exit -1
fi

root_dir="/data/CVG_PVD_DATA/EO_short/flight${flight}_sites/site_${site}"


echo "This is registration_eval/main.sh. Running with the following input arguments"
echo "Root directory:"
echo $root_dir



#*******************************************************************************************************
# Create BOXM2 scene parameter file
#*******************************************************************************************************
if $create_scene_from_bundler; then
   out_dir="/Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight${flight}_sites/site_${site}"
   boxm2_create_scene.py -c $root_dir/output_fixf_final.nvm -i "$root_dir" -a "boxm2_mog3_grey" -o "$out_dir" -p "$out_dir/scene_creation_log.txt"
fi