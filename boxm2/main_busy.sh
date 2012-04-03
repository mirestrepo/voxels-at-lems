#!/bin/bash
"""
Created on Mon April 23, 2011

@author:Isabel Restrepo

A script that encapsulates all steps needed to create a boxm2 scene from bundler output.
You need to set up the main path, where there should be a folder called frames original with all original images (those used by bundler).
In the top directory there should also be bundler output file bundleX.out where X is the focal length used by bundler.
"""

#*******************************************************************************************************
# SET UP ENVIROMENT
#*******************************************************************************************************
CONFIGURATION=Release;
EXE_PATH=/Projects/vxl/bin/$CONFIGURATION/contrib/brl/bseg/boxm2/ocl/exe
export PYTHONPATH=/Projects/vxl/bin/$CONFIGURATION/lib:/Projects/vxl/src/contrib/brl/bseg/boxm2/pyscripts:/Projects/vxl/src/contrib/brl/bseg/boxm2/pyscripts/change:$PYTHONPATH

#*******************************************************************************************************
# DEFINE STEPS TO BE RUN
#*******************************************************************************************************

convert_to_grey=false;
create_scene_from_bundler=false;
create_scene_from_xml=false;
build_model=false;
render=false;
render_cropped=false;
render_circle=false;
render_interactive=false;
render_trajectory=false;
crop_scene=false;


#convert_to_grey=true;
#create_scene_from_bundler=true;
#create_scene_from_xml=true;
build_model=true;
#render=true;
#crop_scene=true;
#render_cropped=true;
#render_circle=true;
#render_interactive=true;
#render_trajectory=true;


#******************************************************************************************************* 
# DEFINE PATHS
#*******************************************************************************************************
#Top directory containing frams_original
#root_dir="/volumes/vision/video/helicopter_providence/3d_models_3_12/site_1";
root_dir="/data/helicopter_providence_3_12/site_1";

device_name="gpu1";
#device_name="gpu0";
#device_name="cpp";

XML_FILE=$root_dir/scene_info.xml;

# directory where boxm2 scene is stored
model_dirname=model;  
boxm2_dir=$root_dir/$model_dirname;

#img_dir
img_dir=$root_dir/imgs;


# Size of images
NI=1280;
NJ=720;

#*******************************************************************************************************
# Crop boxm2_scene to a half-open interval [min, max)
#*******************************************************************************************************
min_i=0;
min_j=1;
min_k=0;

max_i=5;
max_j=7;
max_k=1;

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
   python boxm2_create_scene.py -c $root_dir/output_fixf_final.nvm -i $img_dir -a "boxm2_mog3_grey" -o "$root_dir/nvm_out" -p "$root_dir/scene_creation_log.txt"
fi


if $create_scene_from_xml; then
   echo "XML_FILE = $XML_FILE"
   python boxm2_create_scene_from_XML_info.py --boxm2_dir $boxm2_dir --scene_info $XML_FILE
fi
#*******************************************************************************************************
# Build the Scene
#*******************************************************************************************************
if $build_model; then
    
     #To build the model we brake the image set in chucks because leaks on the GPU cache can corrupt the scene
     #We are specially conservative while we refine
    
#    #Train and refine
#    CHUNKS=25
#    failed=0;
#    for((i=0; i < 1; i++))
#    do
#        echo "Iteration = $i --Refine ON"
#        for((chunk=0; chunk < CHUNKS; chunk++))
#        do
#           python build_model.py -s $root_dir -x "$model_dirname/uscene.xml" --imtype "jpg" -g $device_name -v .06 --initFrame $chunk --skipFrame $CHUNKS --clearApp 1
#        if [ ${?} -ne 0 ]; then 
#            failed=$(($failed+1))
#            echo "[Error] Something Failed. Iteration $i, Chunck $chunk. Num errors $failed"
#            #exit -1
#        fi
#        done
#     done
    
    #Train without refining
    CHUNKS=2
    failed2=0;
    for((i=0; i <= 1; i++))
    do
        echo "Iteration = $i --Refine OFF"
        for((chunk=0; chunk < CHUNKS; chunk++))
        do
            python build_model.py -s $root_dir -x "model/uscene.xml" --imtype "jpg" -g $device_name -v .06 --refineoff 1 --initFrame $chunk --skipFrame $CHUNKS
            if [ ${?} -ne 0 ]; then 
                failed2=$(($failed2+1))
                echo "[Error] Something Failed --Refine OFF. Iteration $i, Chunck $chunk. Num errors $failed2"
                #exit -1
            fi
        done
     done

fi

#*******************************************************************************************************
# Render
#*******************************************************************************************************
if $render_circle; then
    python boxm2_render_circle.py --root_dir $root_dir --boxm2_dir $boxm2_dir

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
    $EXE_PATH/boxm2_ocl_render_view  -scene $boxm2_dir/uscene.xml -ni $NI -nj $NJ -camdir $root_dir/cams_krt -imgdir $root_dir/imgs -gpu_idx 1
fi
    

#*******************************************************************************************************
# Render spacetime using a trajectory
#*******************************************************************************************************
if $render_trajectory; then
    python boxm2_render_traj.py --root_dir $root_dir --boxm2_dir $boxm2_dir
fi


