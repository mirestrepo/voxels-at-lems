#! /usr/bin/env python


import os
import sys
import glob
import shutil

from_dir = "/Volumes/Hippo/helicopter_providence_3_12"
to_dir  = "/Users/isa/Desktop/3d_objects_3_12"



for site in range(1,32):

  from_site_dir = from_dir + "/site_" + str(site);
  to_site_dir = to_dir + "/site_" + str(site);

  if os.path.isdir(from_site_dir +"/"):

      print "Processing "  +  from_site_dir;
      if not os.path.isdir(to_site_dir +"/"):
        os.mkdir(to_site_dir +"/");

        # shutil.copytree(from_site_dir + "/imgs", to_site_dir + "/imgs");
        # shutil.copytree(from_site_dir + "/cams_krt", to_site_dir + "/cams_krt");
        # shutil.copy(from_site_dir + "/scene_info.xml",  to_site_dir + "/scene_info.xml")
        # shutil.copy(from_site_dir + "/bundleXY.png",  to_site_dir + "/bundleXY.png")
        # shutil.copy(from_site_dir + "/bundleYZ.png",  to_site_dir + "/bundleYZ.png")
        # shutil.copy(from_site_dir + "/output_fixf_final.nvm",  to_site_dir + "/output_fixf_final.nvm")
        if os.path.isdir(from_site_dir + "/objects_with_aux"):
            shutil.copytree(from_site_dir + "/objects_with_aux", to_site_dir + "/objects_with_aux")




