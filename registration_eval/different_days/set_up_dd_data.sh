#!/bin/bash
"""
Created on October 17, 2012

@author:Isabel Restrepo

Train scenes for different days experiments
For manual registration see manual_alignment.sh
"""


#***********Capitol 2011
#I. Process original scene

#1. train the scene 15 refine chuncks 2 iterations
# Trained for BMVC

#2. Compute normals and descriptors
# ./compute_geometry.sh "capitol_2011"



#***********BH 2006

#I. Process original scene

#1. train the scene 15 refine chuncks 2 iterations
# ./train_scenes.sh "BH_2006" "png" 15 2

#2. Compute normals and descriptors
# ./compute_geometry.sh "BH_2006"



#***********Downtown 2011
#I. Process original scene

#1. train the scene 15 refine chuncks 2 iterations
# Trained for BMVC - used the following to produce imgs_360
# ./train_scenes.sh "downtown_2011" "png" 0 0


#2. Compute normals and descriptors
./compute_geometry.sh "downtown_2011"





