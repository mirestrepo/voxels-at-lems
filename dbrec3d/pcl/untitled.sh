#!/bin/sh

#  Created by Isabel Restrepo on 11/8/11.
#  Copyright (c) 2011 Brown University. All rights reserved.

#*******************************************************************************************************
# SET UP ENVIROMENT
#*******************************************************************************************************
CONFIGURATION=Release;
export PYTHONPATH=/Projects/lemsvxl/bin/$CONFIGURATION/lib:/Projects/lemsvxl/src/contrib/dbrec_lib/dbrec3d/pyscripts:$PYTHONPATH
SCRIPTS_PATH=/Projects/voxels-at-lems-git/dbrec3d_pcl;

python test_spin_image.py