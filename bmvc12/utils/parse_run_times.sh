#!/bin/bash

FEATURE="ShapeContext"

echo "# ${FEATURE}"
echo -ne "planes = [ "
find /Users/isa/Experiments/shape_features_bmvc12/*/${FEATURE}_45/planes_90/ -iname "*time_log.log" -type f | while read filepath
do
   count=`cat $filepath`
   length=${#count}
#   awk -v a="$count" -v b="real"#   ${count:position:length}
   pos=$(echo  $count | awk '{print index($0, "real")}');
#   pos=$(awk '{print index($count, "real")}')
   pos=$pos+4
#   echo "$count"
   echo -ne "${count:pos:length}, "
  done

echo "] "

echo -ne "cars = [ "
find /Users/isa/Experiments/shape_features_bmvc12/*/${FEATURE}_45/cars_90/ -iname "*time_log.log" -type f | while read filepath
do
   count=`cat $filepath`
   length=${#count}
#   awk -v a="$count" -v b="real"#   ${count:position:length}
   pos=$(echo  $count | awk '{print index($0, "real")}');
#   pos=$(awk '{print index($count, "real")}')
   pos=$pos+4
#   echo "$count"
   echo -ne "${count:pos:length}, "
  done

echo "] "

echo -ne "houses = [ "
find /Users/isa/Experiments/shape_features_bmvc12/*/${FEATURE}_45/residential_90/ -iname "*time_log.log" -type f | while read filepath
do
   count=`cat $filepath`
   length=${#count}
#   awk -v a="$count" -v b="real"#   ${count:position:length}
   pos=$(echo  $count | awk '{print index($0, "real")}');
#   pos=$(awk '{print index($count, "real")}')
   pos=$pos+4
#   echo "$count"
   echo -ne "${count:pos:length}, "
  done

echo "] "

echo -ne "buildings = [ "
find /Users/isa/Experiments/shape_features_bmvc12/*/${FEATURE}_45/buildings_90/ -iname "*time_log.log" -type f | while read filepath
do
   count=`cat $filepath`
   length=${#count}
#   awk -v a="$count" -v b="real"#   ${count:position:length}
   pos=$(echo  $count | awk '{print index($0, "real")}');
#   pos=$(awk '{print index($count, "real")}')
   pos=$pos+4
#   echo "$count"
   echo -ne "${count:pos:length}, "
  done

echo "] "

echo -ne "parking = [ "
find /Users/isa/Experiments/shape_features_bmvc12/*/${FEATURE}_45/parking_90/ -iname "*time_log.log" -type f | while read filepath
do
   count=`cat $filepath`
   length=${#count}
#   awk -v a="$count" -v b="real"#   ${count:position:length}
   pos=$(echo  $count | awk '{print index($0, "real")}');
#   pos=$(awk '{print index($count, "real")}')
   pos=$pos+4
#   echo "$count"
   echo -ne "${count:pos:length}, "
  done

echo "] "
