#!/bin/bash

#*******************************************************************************************************
# SET UP ENVIROMENT
#*******************************************************************************************************
CONFIGURATION=Release;
EXE_PATH=/Projects/vxl/bin/$CONFIGURATION/contrib/brl/bseg/boxm2/ocl/exe
export PYTHONPATH=/Projects/vxl/bin/$CONFIGURATION/lib:/Projects/vxl/src/contrib/brl/bseg/boxm2/pyscripts:/Projects/vxl/src/contrib/brl/bseg/boxm2/pyscripts/change:$PYTHONPATH

#*******************************************************************************************************
# RUN A SCRIPT
#*******************************************************************************************************

#python2.7 ./build_model.py -s "/data/downtown" -x "model/scene.xml" -i "png" -g "gpu1" -p 1 -r 0 -n 5
#python2.7 ./boxm2_update_scene.py
#python2.7 ./oclinfo.py
#python ./gauss_gradients_temp.py
#
#python ../../cvg_scripts/intensity_prob.py -s apartments -x model/uscene.xml -i /path/to/images -c /path/to/cameras


root_dir="/Users/isa/Experiments/reg3d_eval/downtown_dan/original";
cams_dir=$root_dir/cams_krt;
img_dir=$root_dir/imgs;
# python intensity_probe.py -i $img_dir -c $cams_dir

python corr_registration_tool.py -s $root_dir -x "model/scene.xml" -t "tif" -d "gpu0" --backproject true