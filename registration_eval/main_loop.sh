#!/bin/bash

for trial in 3; do ./reg3d_main.sh "downtown_dan" "pert_005" $trial "" 0 0; done

# # find "/Users/isa/Experiments/reg3d_eval/downtown_dan" -name '*aux*.bin' -delete

# for trial in 3 4 5 6 7 8 9; do
#   ./reg3d_main.sh "pert_01" $trial
# done

# find "/Users/isa/Experiments/reg3d_eval/downtown_dan" -name '*aux*.bin' -delete

# for trial in 1 2 3 4 5 6 7 8 9; do
#   ./reg3d_main.sh "pert_015" $trial
# done

# find "/Users/isa/Experiments/reg3d_eval/downtown_dan" -name '*aux*.bin' -delete

# ./reg3d_main.sh "capitol_dan" "png" 15 0
# ./reg3d_main.sh "scili_3_12" "" 0 0


#note downtown dan 10,3 - capitol 15,5
#scli-li used  scene from bmvc  experiments