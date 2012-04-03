#!/bin/bash


export PYTHONPATH=/Projects/vxl/bin/Release/lib
echo "PYTHONPATH=" $PYTHONPATH

# Assuminig the boxm_scene-4-4-1 works what i need to run next is

./boxm/split_and_convert.py #this is to split the scene into alpha scene and gaussian scene
./boxm/merge_mog.py #this is to merge the gaussian mixture into an univariate gaussian
./dbrec3d/find_edges.py