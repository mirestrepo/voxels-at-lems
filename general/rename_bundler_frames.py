#! /usr/bin/env python


import os
import sys
import glob
import shutil

filtered_frames_dir = "/Users/isa/Experiments/helicopter_providence/frames_original_brandon/frames_grey"
frames_1_dir = "/Users/isa/Experiments/helicopter_providence/frames_original_brandon/frames1"

if not os.path.isdir(frames_1_dir +"/"):
  os.mkdir(frames_1_dir +"/");
  

filtered_frames= glob.glob1(filtered_frames_dir, 'frames*')

files_missing = [128, 133, 134, 138, 140, 141, 145, 157, 163, 168]

#1. rename to start at 1

#for file_idx  in range(0, len(filtered_frames)):
#    this_file = "frames_%05d.tif" %file_idx;
#    new_file = "frames_%05d.tif" %(file_idx+1);
#    print('This file: ' + this_file);
#    print('New file: ' + new_file)
#    shutil.copy(filtered_frames_dir + '/' + this_file, frames_1_dir + '/' +new_file);


#2. Insert missing files
#inc = 0;
#for file in files_missing:
#    dir1 = "/Users/isa/Experiments/helicopter_providence/frames_original_brandon/frames_original_bad_cams_removed_" + str(inc)
#    dir2 = "/Users/isa/Experiments/helicopter_providence/frames_original_brandon/frames_original_bad_cams_removed_" + str(inc + 1)
#
#    os.mkdir(dir2 +"/");
#
#    for file_idx  in range(file, 362 + inc):
#        this_file = "frames_%05d.tif" %file_idx;
#        new_file = "frames_%05d.tif" %(file_idx+1);
#        print('This file: ' + this_file);
#        print('New file: ' + new_file)
#        c   
#    inc = inc +1;


dir1 = "/Users/isa/Experiments/helicopter_providence/frames_original_brandon/frames_original_bad_cams_removed"
#os.mkdir(dir1 +"/");


for inc in range(0, 11):
    dir2 = "/Users/isa/Experiments/helicopter_providence/frames_original_brandon/frames_original_bad_cams_removed_" + str(inc)
    
    files = glob.glob1(dir2, 'frames*')

    for this_file  in files:
        shutil.copy(dir2 + '/' + this_file, dir1 + '/' +this_file);    
    inc = inc +1;