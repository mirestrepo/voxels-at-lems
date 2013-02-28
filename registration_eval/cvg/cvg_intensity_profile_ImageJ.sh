#!/bin/bash
"""
Created on Dec 6, 2012

@author:Isabel Restrepo

Open ImageJ to get intensity profiles within regions
"""

#----------------------------------------
# BH
#----------------------------------------

# copyroot="/Users/isa/Experiments/reg3d_eval/cvg_eo_data/profiles/BH"
# mkdir -p $copyroot

# site=1

# flight=2
# sceneroot="/Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight${flight}_sites/site_${site}"
# img_file=$sceneroot/imgs/010417.png
# img_file_cp=$copyroot/BHF2_010417.png
# cp -fv $img_file $img_file_cp

# flight=4
# sceneroot="/Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight${flight}_sites/site_${site}"
# img_file=$sceneroot/imgs/010179.png
# img_file_cp=$copyroot/BHF4_010179.png
# cp -fv $img_file $img_file_cp

# flight=5
# sceneroot="/Users/isa/Experiments/reg3d_eval/cvg_eo_data/flight${flight}_sites/site_${site}"
# img_file=$sceneroot/imgs/049440.png
# img_file_cp=$copyroot/BHF5_049440.png
# cp -fv $img_file $img_file_cp


# cd /Applications/ImageJ/ImageJ64.app/Contents/Resources/Java
# copyroot="/Users/isa/Experiments/reg3d_eval/cvg_eo_data/profiles/flight${flight}_sites/site_${site}"
# img_file_cp=$copyroot/010417.png
# echo $img_file_cp
# java -jar ij.jar $img_file_cp

#----------------------------------------
# APARTMENTS
#----------------------------------------

copyroot="/Users/isa/Experiments/reg3d_eval/cvg_eo_data/profiles/Apartmens"
mkdir -p $copyroot

site=2
