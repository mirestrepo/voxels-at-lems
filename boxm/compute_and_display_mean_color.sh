#!/bin/bash

CONFIG=Release;

export PYTHONPATH=/Projects/vxl/bin/$CONFIG/lib
echo "PYTHONPATH=" $PYTHONPATH

model_dir="/Users/isa/Experiments/CapitolBOXMSmall";

python compute_expected_color_scene.py $model_dir

#display the histogram
#/Projects/lemsvxl/bin/$CONFIG/contrib/dbrec_lib/dbrec3d/exe/dbrec3d_scene_statistics -scene "/Users/isa/Experiments/DowntownBOXM_4_4_1/mean_color_scene.xml"

