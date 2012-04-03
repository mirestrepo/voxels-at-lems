#!/bin/bash

for SCENE_ID in 8
do
  boxm2_scene="/Users/isa/Experiments/helicopter_providence/boxm2_scenes/site"$SCENE_ID"/scene_cropped.xml"
  boxm_dir="/Users/isa/Experiments/helicopter_providence/boxm_scenes/site"$SCENE_ID
  mkdir $boxm_dir
  /Projects/vxl/bin/Release/contrib/brl/bseg/boxm_bridge/boxm2_to_boxm_exe -scene $boxm2_scene -out $boxm_dir
done