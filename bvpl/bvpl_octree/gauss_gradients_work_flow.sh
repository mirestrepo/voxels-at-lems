 #!/bin/bash
"""
Created on Mon Feb 14, 2011

@author:Isabel Restrepo

A script that encapsulates all steps needed to learn and classify based on pca features
"""

if [ $1 = "-r" ] ; then
  VXL_PYTHONPATH=/Projects/vxl/bin/Release/lib
else
  if [ $1 = "-d" ] ; then
       VXL_PYTHONPATH=/Projects/vxl/bin/Debug/lib
  else
      echo "Need a flag, either -d or -r";
  fi 
fi

export PYTHONPATH=$VXL_PYTHONPATH;
echo "PYTHONPATH=" $PYTHONPATH

model_dir="/Users/isa/Experiments/super3d/sr2_3scene_sr2_images/boxm"


#Split scene
python /Projects/voxels-at-lems/scripts/boxm/split_scene.py --model_dir $model_dir

#compute the gradients
python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/compute_gauss_gradient_alpha.py --model_dir $model_dir

#save
python /Projects/voxels-at-lems/scripts/bvpl/bvpl_octree/gauss_gradient_to_binary.py --model_dir $model_dir