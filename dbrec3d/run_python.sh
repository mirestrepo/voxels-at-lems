#!/bin/bash

if [ $1 = "-r" ] ; then
  export PYTHONPATH=/Projects/lemsvxl/bin/Release/lib:/Projects/pcl_dev/pcl/trunk/install_release/lib
else
  if [ $1 = "-d" ] ; then
      export PYTHONPATH=/Projects/lemsvxl/bin/Debug/lib
  else
      echo "Need a flag, either -d or -r";
  fi 
fi

echo "PYTHONPATH=" $PYTHONPATH

#*************************BOF related ******************************#

#python /Projects/voxels-at-lems/scripts/dbrec3d/bof/examine_ground_truth.py
#python /Projects/voxels-at-lems/scripts/dbrec3d/bof/set_up_ply_files.py


#for trial in 0 2 3 4 5 6 7 8 9 
#do
	#bof_dir="/Users/isa/Experiments/BOF/helicopter_providence/taylor/bof_cross_validation/trial_"$trial
	#python2.7 /Projects/voxels-at-lems/scripts/dbrec3d/bof/random_split_test_train.py --bof_dir $bof_dir
#done

#bof_dir="/Users/isa/Experiments/BOF/helicopter_providence/taylor/bof_cross_validation/trial_0"
#python2.7 /Projects/voxels-at-lems/scripts/dbrec3d/bof/compute_object_level.py --bof_dir $bof_dir 

#*************************PCL related ******************************#
  
#python2.7 /Projects/voxels-at-lems/scripts/dbrec3d/pcl/scene_to_pcl.py
#python2.7 /Projects/voxels-at-lems/scripts/dbrec3d/pcl/compute_fpfh.py
python2.7 /Projects/voxels-at-lems/scripts/dbrec3d/pcl/compute_spin_image.py

#python2.7 /Projects/voxels-at-lems/scripts/dbrec3d/pcl/k_means_on_fpfh.py
#python2.7 /Projects/voxels-at-lems/scripts/dbrec3d/pcl/assign_to_cluster_fpfh.py
#python2.7 /Projects/voxels-at-lems/scripts/dbrec3d/pcl/convert_id_to_rgb_cloud.py
#python2.7 /Projects/voxels-at-lems/scripts/dbrec3d/pcl/normalize_object_lcf.py
#python2.7 /Projects/voxels-at-lems/scripts/dbrec3d/pcl/PLY_to_pcd.py
#python2.7 /Projects/voxels-at-lems/scripts/dbrec3d/pcl/split_points_and_normals.py
