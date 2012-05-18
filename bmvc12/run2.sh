#!/bin/bash
#
#for radius in 10; do
##   python ./compute_omp_descriptors.py -r $radius -p 90
#    python pickle_descritor.py -r $radius -p 90
#done

#for trial in 0 1 2 3 4; do
#  for radius in 10 15 20 30 45; do
#     python ./stack_test_features.py -r $radius -p 90 -t $trial
#  done
#done

#for radius in 30; do
#    for site in 12 16 18 21 22 23 25 26 27; do
#        python ./descriptors/compute_spin_images.py -s $site -r $radius -p 90 -j 4
#    done
#done

for radius in 45; do
    for site in 25 26 27; do
        python ./descriptors/compute_shape_context.py -s $site -r $radius -p 90
    done
done