#!/bin/bash
"""
Created on August 8, 2012

@author:Isabel Restrepo

A script that encapsulates all steps for evaluation of 3d-registration in the PVL
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

compute_descriptor=false;
register_ia=false;
register_icp=false;
visualize_reg_ia=false;
visualize_reg_icp=false;

#compute_descriptor=true;
#register_ia=true;
#register_icp=true;
#compute_transformation=true;
#visualize_reg_ia=true;
#visualize_reg_icp=true;

#******************************************************************************************************* 
# Grab the inputs and set local variables
#*******************************************************************************************************

#nargs=$#;
#
#if [ $nargs -eq 1 ]; then
#    trial_number=$1
#else
#    echo "Need scene number as an input"
#    exit -1
#fi

trial_number=0;
scale=73;

root_dir="/data/reg3d_eval/downtown_dan/trial_$trial_number"
#root_dir="/data/reg3d_eval/downtown_dan/original"


echo "This is registration_eval/reg3d.sh."
echo "Root directory:"
echo $root_dir

descriptor="SHOT"
radius=30;
percentile=99;

#*******************************************************************************************************
#Compute Descriptors
#*******************************************************************************************************
if $compute_descriptor; then
  njobs=8;
  vpcl_compute_omp_descriptors.py -s $root_dir --basenameIn "gauss_233_normals_pvn" -r $radius -p $percentile -d $descriptor -j $njobs -v true
fi

#*******************************************************************************************************
#Compute Rigid Transformation
#*******************************************************************************************************
if $register_ia; then
  tgtRoot="/data/reg3d_eval/downtown_dan/original"
  ./register_ia_temp.py --srcRoot $root_dir --tgtRoot $tgtRoot --basenameIn "gauss_233_normals_pvn" -r $radius -p $percentile -d $descriptor -v true -s $scale
fi

if $register_icp; then
  tgtRoot="/data/reg3d_eval/downtown_dan/original"
  ./register_icp.py --srcRoot $root_dir --tgtRoot $tgtRoot --basenameIn "gauss_233_normals_pvn" -r $radius -p $percentile -d $descriptor
fi

if $visualize_reg_ia; then
  tgtRoot="/data/reg3d_eval/downtown_dan/original"
  tgt_cloud="$tgtRoot/gauss_233_normals_pvn_$percentile.ply"
  src_cloud="$root_dir/${descriptor}_${radius}/ia_cloud_$percentile.pcd"
  $VPCL_EXE_PATH/visualize $src_cloud $tgt_cloud
fi

if $visualize_reg_icp; then
  tgtRoot="/data/reg3d_eval/downtown_dan/original"
  tgt_cloud="$tgtRoot/gauss_233_normals_pvn_$percentile.ply"
  src_cloud="$root_dir/${descriptor}_${radius}/icp_cloud_$percentile.pcd"
  $VPCL_EXE_PATH/visualize $src_cloud $tgt_cloud
fi
