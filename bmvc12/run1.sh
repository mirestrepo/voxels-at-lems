#!/bin/bash

#for radius in 30; do
#    for site in 18 21 22 23 25 26 27; do
#        python ./descriptors/compute_shape_context.py -s $site -r $radius -p 90
#    done
#done

for radius in 45; do
    for site in 16 18 21 22 23; do
        python ./descriptors/compute_shape_context.py -s $site -r $radius -p 90
    done
done