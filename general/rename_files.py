#! /usr/bin/env python

import os
import sys
import glob
import shutil

dir = "/Users/isa/Experiments/reg3d_eval/downtown_dan"


files = glob.glob(dir + '/trial_*/SHOT_30/ia_cloud_99.pcd')

for this_file  in files:
  new_file = this_file[:-4]
  new_file = new_file + "_200.pcd"
  print new_file
  # shutil.move(this_file, new_file);
