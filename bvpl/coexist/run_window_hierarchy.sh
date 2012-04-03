#!/bin/bash


export PYTHONPATH=/Projects/vxl/bin/Release/lib

echo "PYTHONPATH=" $PYTHONPATH


#echo "*****************Finding Corners *********************"
#data_dir="/Users/isa/Experiments/CapitolSFM/few_windows";
#output_dir="/Users/isa/Experiments/CapitolSFM/few_windows/ocp+app/all_directions";
#python find_corners.py $data_dir $output_dir



echo "*****************Find and Pair Corner*********************"
data_dir="/Users/isa/Experiments/CapitolSFM/smaller_capitol";
output_dir="/Users/isa/Experiments/CapitolSFM/smaller_capitol/ocp+app/corners";

directions="pi_over_2_corners";
num_corners=0;

python pair_corners.py $data_dir $output_dir $directions $num_corners

echo "*****************Pairs of Pair Corner*********************"
data_dir="/Users/isa/Experiments/CapitolSFM/smaller_capitol/ocp+app/corners";
output_dir="/Users/isa/Experiments/CapitolSFM/smaller_capitol/ocp+app/corners/layer1";

python pair_corner_pairs.py $data_dir $output_dir $directions $num_corners

echo "*****************Pairing Window primitives *********************"
data_dir="/Users/isa/Experiments/CapitolSFM/smaller_capitol/ocp+app/corners/layer1";
output_dir="/Users/isa/Experiments/CapitolSFM/smaller_capitol/ocp+app/corners/layer2";

python pair_window_primitives.py $data_dir $output_dir $directions $num_corners