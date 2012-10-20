#!/bin/bash

# for dir in  5; do

#     root_dir=/volumes/vision/video/helicopter_providence/3d_models_3_12/site_$dir
#     folder_out=$root_dir/frames_jpg
#     cd $root_dir

#     for folder_png in frames; do

#         cd $folder_png;

#         if [ ! -d "$folder_out" ]; then
#             mkdir $folder_out
#         else
#             continue;
#         fi

#         for img in *.png; do
#             filename=${img%.*}
#             file_out=$folder_out/$filename.jpg;
#             echo "Converting:"
#             echo $filename
#             convert "$filename.png" "$file_out"
#         done
#     done
# done

# echo "Done!"

###CVGDATA
for flight in 4 5 ; do

    for site in 1 2 3 4 5 7; do
        root_dir=/data/CVG_PVD_DATA/EO/flight${flight}_sites/site_${site}
        folder_out=$root_dir/jpg
        cd $root_dir

        if [ ! -d "$folder_out" ]; then
            mkdir $folder_out
        else
            continue;
        fi

        for img in *.png; do
            filename=${img%.*}
            file_out=$folder_out/$filename.jpg;
            echo "Converting:"
            echo $filename
            echo "to"
            echo $file_out
            convert "$filename.png" "$file_out"
        done

    done
done

echo "Done!"