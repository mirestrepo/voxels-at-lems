#! /usr/bin/env python

import os
import sys
import glob
import shutil

sr2_frames = "/Users/isa/Experiments/super3d/sr2_needed"


#1. rename to start at 1

for file_idx  in range(0, 249, 8):
    this_file = "sr2_%03d.png" %file_idx;
    new_file = "frame_%05d.png" %(file_idx);
    print('This file: ' + this_file);
    print('New file: ' + new_file)
    os.rename(sr2_frames + '/' + this_file, sr2_frames + '/' +new_file); 