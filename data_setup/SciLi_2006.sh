#!/bin/bash
"""
Created on January 8, 2018

@author:Isabel Restrepo

Set up data for B.H-2006
"""


#************ Extract frames from video ************
# cd /data
# vlc --intf=rc --video-filter=scene --start-time=74 --stop-time=165 --scene-ratio=1 --scene-prefix=frame --scene-path=SciLi_2006/imgs vid15_brown_campus.m2t

#************Convert to jpg ************
# root_dir="/data/SciLi_2006/imgs"
# folder_out=$root_dir/jpg
# cd $root_dir

# if [ ! -d "$folder_out" ]; then
#     mkdir $folder_out
# else
#     continue;
# fi

# for img in *.png; do
#     filename=${img%.*}
#     file_out=$folder_out/$filename.jpg;
#     echo "Converting:"
#     echo $filename
#     echo "to"
#     echo $file_out
#     convert "$filename.png" "$file_out"
# done

#************ Run Bundler ************
# Run visual SFM - compute_sfm.bat is the script I used


#************ Set up site from bundler output file ************
CONFIGURATION=Release;
EXE_PATH=/Projects/vxl/bin/$CONFIGURATION/contrib/brl/bseg/boxm2/ocl/exe
export PYTHONPATH=/Projects/vxl/bin/$CONFIGURATION/lib:/Projects/vxl/src/contrib/brl/bseg/boxm2/pyscripts:/Projects/vxl/src/contrib/brl/bseg/boxm2/pyscripts/change:$PYTHONPATH
SCRIPTS_PATH=/Projects/voxels-at-lems-git;


root_dir="/data/SciLi_2006"
python $SCRIPTS_PATH/boxm2/boxm2_create_scene.py -c $root_dir/output_fixf_final.nvm -i "$root_dir/imgs" -a "boxm2_mog3_grey" -o "$root_dir/nvm_out" -p "$root_dir/nvm_out/scene_creation_log.txt"

#************ Train the scene **********************

