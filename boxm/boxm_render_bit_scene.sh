#!/bin/bash

camera_fname="/Volumes/vision/video/dec/capitol_sfm_rotated/cameras_KRT/camera_00040.txt";
scene_fname="/Users/isa/Experiments/tests/bit_scene/scene.xml"

#run executable

/Projects/vxl/bin/Release/contrib/brl/bseg/boxm/ocl/exe/boxm_ocl_render_bit_view -cam $camera_fname -scene $scene_fname -ni 1280 -nj 740
