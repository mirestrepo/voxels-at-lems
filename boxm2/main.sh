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
EXE_PATH=/Projects/vxl/bin/$CONFIGURATION/contrib/brl/bseg/boxm2/ocl/exe
export PYTHONPATH=/Projects/vxl/bin/$CONFIGURATION/lib:/Projects/vxl/src/contrib/brl/bseg/boxm2/pyscripts:/Projects/vxl/src/contrib/brl/bseg/boxm2/pyscripts/change:$PYTHONPATH
SCRIPTS_PATH=/Projects/voxels-at-lems-git;

#*******************************************************************************************************
# DEFINE STEPS TO BE RUN
#*******************************************************************************************************

crop_scene=false;
convert_to_grey=false;
create_scene_from_bundler=false;
create_scene_from_xml=false;
build_model=false;
crop_scene=false;
render_circle=false;
render=false;
render_cropped=false;
render_interactive=false;
render_trajectory=false;
compute_gauss_gradients=false;
compute_normals=false;
flip_normals=false;
export_scene=false;
thresh_PLY=false;
use_probe=false;


# create_scene_from_xml=true;
#build_model=true;
crop_scene=true;
#render=true;
#render_cropped=true;
# render_interactive=true;
#render_circle=true;
#render_trajectory=true;
# compute_gauss_gradients=true;
#compute_normals=true;
# flip_normals=true;
# export_scene=true;
# thresh_PLY=true;
#use_probe=true;



#*******************************************************************************************************
# DEFINE PATHS
#*******************************************************************************************************
#Top directory containing frams_original
#root_dir="/volumes/vision/video/helicopter_providence/3d_models_3_12/site_1";
root_dir="/Users/isa/Experiments/reg3d_eval/res_middletown/trial_9";
# root_dir="/data/hemenways"
# directory where boxm2 scene is stored
model_dirname="model";
boxm2_dir=$root_dir/$model_dirname;


# Size of images
NI=1280;
NJ=720;

#*******************************************************************************************************
# Crop boxm2_scene to a half-open interval [min, max)
#*******************************************************************************************************
min_i=0;
min_j=0;
min_k=1;

max_i=4;
max_j=5;
max_k=5;

if $crop_scene; then
    python boxm2_crop_scene.py --boxm2_dir $boxm2_dir --min_i $min_i --min_j $min_j --min_k $min_k --max_i $max_i --max_j $max_j --max_k $max_k
fi


#*******************************************************************************************************
# Convert images to grey
#*******************************************************************************************************
if $convert_to_grey; then
    python rgb_to_grey.py --rgb_dir $root_dir/frames --grey_dir $root_dir/frames_grey
fi

#*******************************************************************************************************
# Create BOXM2 scene parameter file
#*******************************************************************************************************
if $create_scene_from_bundler; then
   python boxm2_create_scene.py -c $root_dir/output_fixf_final.nvm -i "$root_dir/frames_jpg" -a "boxm2_mog3_grey" -o "$root_dir/nvm_out" -p "$root_dir/scene_creation_log.txt"
fi


if $create_scene_from_xml; then
   XML_FILE=$root_dir/scene_info.xml;
   echo "XML_FILE = $XML_FILE"
   python boxm2_create_scene_from_XML_info.py --boxm2_dir $boxm2_dir --scene_info $XML_FILE
fi
#*******************************************************************************************************
# Build the Scene
#*******************************************************************************************************
if $build_model; then

    #To build the model we brake the image set in chucks because leaks on the GPU cache can corrupt the scene
    #We are specially conservative while we refine

    scene_file="scene.xml"
    imtype="jpg"
    device_name="gpu1";

    #Train and refine
    CHUNKS=12;


    failed=0;
    failed_r=0;
    failed_u=0;
    for((i=0; i < 3; i++))
    do
        echo "Iteration = $i --Refine ON"
        for((chunk=0; chunk < CHUNKS; chunk++))
        do
           python build_model.py -s $root_dir -x "$model_dirname/$scene_file" --imtype "$imtype" -g $device_name -v .06 --initFrame $chunk --skipFrame $CHUNKS --clearApp 1

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
            python build_model.py -s $root_dir -x "$model_dirname/$scene_file" --imtype "$imtype" -g $device_name -v .06 --refineoff 1 --initFrame $chunk --skipFrame $CHUNKS

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
#compute_gauss_gradients
#*******************************************************************************************************
if $compute_gauss_gradients; then
  scene_file="scene.xml"
  imtype="jpg"
  device_name="gpu1";
  python $SCRIPTS_PATH/boxm2/boxm2_compute_gauss_gradients.py -s $root_dir -x "$model_dirname/$scene_file" -g $device_name --export_file "gauss_233_normals.ply" --use_sum true --p_thresh 0.1
fi

#*******************************************************************************************************
# Compute Normals
#*******************************************************************************************************
if $compute_normals; then
  T=$(date +%s);
  log_file="$root_dir/compute_normals_log.txt"
  scene_file="scene.xml"
  device_name="gpu1";
  $SCRIPTS_PATH/boxm2/boxm2_compute_normals.py -s $root_dir -x "$model_dirname/$scene_file" -g $device_name
  DIFF=$(( $(date +%s) - $T ))
  time_file=$root_dir/"compute_normals_run_time.txt";
  echo "compute_normals.py took (in seconsd) \n $DIFF" > $time_file;
fi

if $flip_normals; then
  scene_file="scene.xml"
  device_name="gpu1";
  flipped=0;
  attempt=0;
  try=1;
  while [ $try -eq 1 ];
  do
    log_file="$root_dir/flip_normals_log.txt"
    $SCRIPTS_PATH/boxm2/boxm2_flip_normals.py -s $root_dir -x "$model_dirname/$scene_file" -g $device_name --use_sum true -p $log_file
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
    scene_file="scene.xml"
    device_name="gpu1";
    $SCRIPTS_PATH/boxm2/boxm2_export_scene_to_PLY.py -s $root_dir -x "$model_dirname/$scene_file" -g $device_name --exportFile "gauss_233_normals.ply" --p_thresh 0.1
fi

#*******************************************************************************************************
#Threshold PLY --thresholds are specified within the scrip
#*******************************************************************************************************
if $thresh_PLY; then
$SCRIPTS_PATH/ply_util/thresh_ply.py -s $root_dir -i "$root_dir/gauss_233_normals.ply" -o "$root_dir/gauss_233_normals_pvn"
fi



#*******************************************************************************************************
# Render Viewing Trajectory
#*******************************************************************************************************
if $render_circle; then
    scene_file="scene.xml"
    imtype="png"
    device_name="gpu1";
    python boxm2_render_circle.py -s $root_dir -x "$model_dirname/$scene_file" --imtype "$imtype" -g $device_name
fi

#*******************************************************************************************************
# Render
#*******************************************************************************************************
if $render; then
    $EXE_PATH/boxm2_ocl_render_view  -scene $boxm2_dir/uscene.xml -ni $NI -nj $NJ -gpu_idx 1
fi

#*******************************************************************************************************
# Render Cropped
#*******************************************************************************************************
if $render_cropped; then
    $EXE_PATH/boxm2_ocl_render_view -scene $boxm2_dir/rscene.xml -ni $NI -nj $NJ -gpu_idx 1
fi

#*******************************************************************************************************
# Interactive render
#*******************************************************************************************************
if $render_interactive; then
    $EXE_PATH/boxm2_ocl_render_view  -scene $boxm2_dir/scene.xml -ni $NI -nj $NJ -camdir $root_dir/cams_krt -imgdir $root_dir/imgs -gpu_idx 1
fi


#*******************************************************************************************************
# Render spacetime using a trajectory
#*******************************************************************************************************
if $render_trajectory; then
    python boxm2_render_traj.py --root_dir $root_dir --boxm2_dir $boxm2_dir
fi

#*******************************************************************************************************
# Use intensity probe
#*******************************************************************************************************
if $use_probe; then
    root_dir="/data/helicopter_providence_3_12/site_1";
    scene_file="scene.xml"
    cams_dir=$root_dir/cams_krt;
    img_dir=$root_dir/imgs;
    python intensity_probe.py -i $img_dir -c $cams_dir
fi
