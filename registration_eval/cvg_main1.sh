#!/bin/bash
"""
Created on October 20, 2012

@author:Isabel Restrepo

Experiments for cvg data (variation in illumination)
"""

#*******************************************************
#I. Set up the scene files and model directories

#1. Read bundler output and output imgs/ cams_krt/ and model/
# for flight in 2; do
#     for site in 2 3 4 7; do
#         ./set_up_cvg_scenes.sh $flight $site
#     done
# done

# for flight in 4; do
#     for site in 1 2 3 4 5 7; do
#         ./set_up_cvg_scenes.sh $flight $site &
#     done
# done

# wait

# for flight in 5; do
#     for site in 1 2 3 4 5 7; do
#         ./set_up_cvg_scenes.sh $flight $site &
#     done
# done
# wait


#2. Use matlab to plot the points and cameras

#3. Manually assemble a scene.xml

#*******************************************************
#II Train scenes

for flight in 2; do
    for site in 1 2 3 4 7; do
        ./train_cvg_scenes.sh $flight $site 17 2
    done
done

for flight in 4; do
    for site in 1 2 3 4 5 7; do
        ./train_cvg_scenes.sh $flight $site 17 2
    done
done

for flight in 5; do
    for site in 1 2 3 4 5 7; do
        ./train_cvg_scenes.sh $flight $site 17 2
    done
done