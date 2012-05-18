#!/bin/bash

FEATURE="ShapeContext"

echo "# ${FEATURE}"
echo -ne "means_20 = [ "
find /Users/isa/Experiments/bof_bmvc12/*/${FEATURE}_30/percentile_90/k_means_20 -iname "MinibatchKmeans_time.txt" -type f | while read filepath
do
   count=`cat $filepath`
   echo -ne "${count}, "
  done

echo "] "

echo -ne "means_50 = [ "
find /Users/isa/Experiments/bof_bmvc12/*/${FEATURE}_30/percentile_90/k_means_50 -iname "MinibatchKmeans_time.txt" -type f | while read filepath
do
   count=`cat $filepath`
   echo -ne "${count}, "
  done

echo "] "

echo -ne "means_100 = [ "
find /Users/isa/Experiments/bof_bmvc12/*/${FEATURE}_30/percentile_90/k_means_100 -iname "MinibatchKmeans_time.txt" -type f | while read filepath
do
   count=`cat $filepath`
   echo -ne "${count}, "
  done

echo "] "

echo -ne "means_200 = [ "
find /Users/isa/Experiments/bof_bmvc12/*/${FEATURE}_30/percentile_90/k_means_200 -iname "MinibatchKmeans_time.txt" -type f | while read filepath
do
   count=`cat $filepath`
   echo -ne "${count}, "
  done

echo "] "

echo -ne "means_500 = [ "
find /Users/isa/Experiments/bof_bmvc12/*/${FEATURE}_30/percentile_90/k_means_500 -iname "MinibatchKmeans_time.txt" -type f | while read filepath
do
   count=`cat $filepath`
   echo -ne "${count}, "
  done

echo "] "