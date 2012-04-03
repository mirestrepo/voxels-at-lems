#!/bin/bash

echo "PYHTONPATH before:" $PYTHONPATH
export PYTHONPATH=/Projects/vxl/bin/Debug/lib:/Projects/vxl/src/contrib/brl/bseg/boxm2/pyscripts:$PYTHONPATH
echo "PYHTONPATH after:" $PYTHONPATH

#python2.7 ./build_model.py -s "/data/downtown" -x "model/scene.xml" -i "png" -g "gpu1" -p 1 -r 0 -n 5 
#python2.7 ./boxm2_update_scene.py
python2.7 ./oclinfo.py