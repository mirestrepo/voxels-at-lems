#!/bin/bash
#This script is meant to call bmvc12_main.sh for multiple scenes


#for site in 1 2; do
#  category=planes;
#  ./bmvc12_main.sh $site $category &
#done



#for site in 3 6; do
#  category=cars;
#  ./bmvc12_main.sh $site $category &
#done
#
##for site in 7 8 11; do
##  category=residential;
##  ./bmvc12_main.sh $site $category &
##done
#
##for site in 16 18 21 22 23 25; do
##  category=buildings;
##  ./bmvc12_main.sh $site $category &
##done
#
##./bmvc12_main.sh 25 $category
#
##for site in 26; do
##  category=parking;
##  ./bmvc12_main.sh $site $category &
##done
#
#wait

for site in 1 2 3 6 7 8 10 11 12 16 18 21 22 23 25 26 27; do
   ./bmvc12_main.sh $site
done