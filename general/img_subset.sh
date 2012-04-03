#!/bin/bash
dir=30;
root_dir=/volumes/vision/video/helicopter_providence/3d_models_3_12/site_$dir
folder_in=$root_dir/frames_jpg
folder_out=$root_dir/frames_jpg_subset

if [ ! -d "$folder_out" ]; then
   mkdir $folder_out
fi


cd $root_dir
nframes=433

for((i=1; i <$nframes; i=$i+2))
  do
    frame=`printf "frame%03d.jpg" $i`
    echo $frame   
    cp $folder_in/$frame $folder_out/$frame
done

echo "Done!"