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


create_scene_from_xml=true;
#build_model=true;
#crop_scene=true;
#render=true; 
#render_cropped=true;
#render_interactive=true;
#render_trajectory=true;


#******************************************************************************************************* 
# DEFINE PATHS
#*******************************************************************************************************
#Top directory containing frams_original
#root_dir="/volumes/vision/video/helicopter_providence/3d_models_3_12/site_1";
#root_dir="/data/helicopter_providence_3_12/site_12";

# directory where boxm2 scene is stored
model_dirname=model;
boxm2_dir=$root_dir/$model_dirname;


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
    #device_name="cpp";

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
    $EXE_PATH/boxm2_ocl_render_view  -scene $boxm2_dir/scene.xml -ni $NI -nj $NJ -camdir $root_dir/cams_krt -imgdir $root_dir/imgs -gpu_idx 1
fi
    

#*******************************************************************************************************
# Render spacetime using a trajectory
#*******************************************************************************************************
if $render_trajectory; then
    python boxm2_render_traj.py --root_dir $root_dir --boxm2_dir $boxm2_dir
fi


