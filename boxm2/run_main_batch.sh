#!/bin/bash

#./main_busy.sh 9  10 4
#./main_busy.sh 10 22 2
#./main_busy.sh 11 17 3
#./main_busy.sh 12 21 2
#./main_busy.sh 13 15 3
#./main_busy.sh 14 13 3

#for (( i=1; i<32; i++ ))
for i in 3
do

./main_busy.sh $i

done

