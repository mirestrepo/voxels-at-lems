#!/bin/bash
"""
Created on Mon April 23, 2011

@author:Isabel Restrepo

A script that encapsulates all steps needed to create a boxm2 scene from bundler output.
You need to set up the main path, where there should be a folder called frames original with all original images (those used by bundler).
In the top directory there should also be bundler output file bundleX.out where X is the focal length used by bundler.
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


#*******************************************************************************************************
# DEFINE STEPS TO BE RUN
#*******************************************************************************************************

create_scene_file=false;
train_scene=false;
render=false;
render_cropped=false;
render_circle=false;
render_interactive=false;

#create_scene_file=true;
#train_scene=true;
#render=true;
#render_cropped=true;
#render_circle=true;
#render_interactive=true;



#*******************************************************************************************************

#*******************************************************************************************************
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!DEFINE PATHS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!MUST DO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#*******************************************************************************************************
#Top directory containing frames_original


model_dir="/home/osman/Desktop/site12/boxm2_site"
boxm2_dir=$model_dir
imgs_dir="/home/osman/Desktop/super3d/scili_experiments_bicubic/superresolved_imgs";
cams_dir="/home/osman/Desktop/super3d/scili_experiments_bicubic/superresolved_cams";
#Size of images
NI=2560;
NJ=1440;


# model_dir="C:/Users/osman/Desktop/super3d/scene"
# boxm2_dir=$model_dir
# imgs_dir="C:/Users/osman/Desktop/super3d/frames_grey";
# cams_dir="C:/Users/osman/Desktop/super3d/sfm_rotated_cam";
# NI=1280;
# NJ=720

#*******************************************************************************************************
#Create BOXM2 scene parameter file
#*******************************************************************************************************
if $create_scene_file; then
XML_FILE=$model_dir/scene_info.xml;
echo "XML_FILE = $XML_FILE"
python './boxm2_create_scene.py' --boxm2_dir $boxm2_dir --scene_info $XML_FILE
fi

#*******************************************************************************************************
#Train Scene
#*******************************************************************************************************
if $train_scene; then
for((i=0; i <=0; i++))
do
python './boxm2_update_and_refine_super3d.py' --model_dir $model_dir --boxm2_dir $boxm2_dir --imgs_dir $imgs_dir --cams_dir $cams_dir --NI $NI --NJ $NJ --repeat $i
done

fi

#*******************************************************************************************************
# Crop boxm2_scene to a half-open interval [min, max)
#*******************************************************************************************************
min_i=1;
min_j=1;
min_k=0;
max_i=4;
max_j=4;
max_k=2;

if $crop_scene; then
python './boxm2_crop_scene.py' --boxm2_dir $boxm2_dir --min_i $min_i --min_j $min_j --min_k $min_k --max_i $max_i --max_j $max_j --max_k $max_k
fi

#*******************************************************************************************************
# Render expected images around the scene and save (uses cropped_scene.xml)
#*******************************************************************************************************
if $render_circle; then
python_d boxm2_render_circle.py --model_dir $model_dir --boxm2_dir $boxm2_dir

fi


#*******************************************************************************************************
# Render scene.xml
#*******************************************************************************************************
if $render; then
boxm2_ocl_render_view -scene $boxm2_dir/scene.xml -ni $NI -nj $NJ 
fi

#*******************************************************************************************************
# Render Cropped scene_cropped.xml
#*******************************************************************************************************
if $render_cropped; then
boxm2_ocl_render_view.exe -scene $boxm2_dir/scene_cropped.xml -ni $NI -nj $NJ
fi


#*******************************************************************************************************
# Convert to boxm
#*******************************************************************************************************
if $convert_to_boxm; then
boxm_dir=$model_dir/boxm;
mkdir $boxm_dir;
boxm2_to_boxm_exe -scene $boxm2_dir/scene_cropped.xml -out $boxm_dir
fi
    
#*******************************************************************************************************
# Interactive render
#*******************************************************************************************************
if $render_interactive; then
    boxm2_ocl_render_view.exe --mfc-use-gl -scene $boxm2_dir/scene.xml -ni $NI -nj $NJ -camdir $model_dir/cameras_KRT -imgdir $model_dir/frames_grey 
fi
    
