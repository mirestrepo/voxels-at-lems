#!/bin/bash

#for site in 1 2 3 6 7 8 10 11 12 16 18 21 22 23 25 26 27; do
#    ./add_aux_to_ply.py -s $site
#done

#for radius in 45; do
#    for site in 1 2 3 6 7 8 10 11 12 16 18 21 22 23 25 26 27; do
#        python ./descriptors/compute_spin_images.py -s $site -r $radius -p 90 -j 10
#    done
#done

#for radius in 10 15 20 30 45; do
#    for site in 1 2 3 6 7 8 10 11 12 16 18 21 22 23 25 26 27; do
#        python ./compute_shape_context.py -s $site -r $radius -p 90
#    done
#done

#for radius in 10 15 20 30 45; do
#   ./compute_omp_descriptors.py -r $radius -p 90
#done

CONFIGURATION=Release;
export PYTHONPATH=/Projects/lemsvxl/bin/$CONFIGURATION/lib:/Projects/lemsvxl/src/contrib/dbrec_lib/dbrec3d/pyscripts:/Projects/voxels-at-lems-git/bmvc12/utils:$PYTHONPATH

#for trial in 0 1 2 3 4; do
#  for radius in 10 15 20 30 45; do
#    python ./bof/learn_codebook_cp.py -r $radius -p 90 -t $trial -d "ShapeContext"
#  done
#done

#python ./bof/learn_codebook_cp.py -r 10 -p 90 -t 0 -d "ShapeContext"


python ./bof/collect_validation_results.py -r 30 -p 90 -d "SHOT" -k 500
