#!/bin/bash

from_dir="/Volumes/vision/video/helicopter_providence/3d_models_3_12"
to_dir="/data/helicopter_providence_3_12"

for((i=16; i <17; i++))
  do
    if [ ! -d "$to_dir/site_$i" ]; then
       mkdir $to_dir/site_$i
    fi
    cp $from_dir/site_$i/output_fixf_final.nvm $to_dir/site_$i/output_fixf_final.nvm
done



    
    
  