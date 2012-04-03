#! /usr/bin/env python


import os
import sys
import glob
import shutil

from_dir = "/Volumes/vision/video/helicopter_providence/3d_models_3_11"
to_dir  = "/Volumes/voxels_archive/Experiments/helicopter_providence/frames"



for site in [3, 5, 6, 7, 8, 10, 12, 16, 18, 20, 21, 22, 23, 25, 26, 27]:
  
  from_site_dir = from_dir + "/site" + str(site);
  to_site_dir = to_dir + "/site" + str(site);

  if not os.path.isdir(to_site_dir +"/"):
    os.mkdir(to_site_dir +"/");
    
    shutil.copytree(from_site_dir + "/frames_grey", to_site_dir + "/frames_grey");
    shutil.copytree(from_site_dir + "/cameras_KRT", to_site_dir + "/cameras_KRT");

    
    
  