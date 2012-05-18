#!/bin/bash

descriptor_type=FPFH;
for radius in 10; do
  for site in 2; do
    site_dir=/Users/isa/Experiments/shape_features_bmvc12/site_${site} 
    categories=${site_dir}/${descriptor_type}_${radius}/planes_90;
    zip -r ${categories}/descriptors.zip ${categories}/mesh*.txt
#    rm ${categories}/mesh*.txt
  done
done