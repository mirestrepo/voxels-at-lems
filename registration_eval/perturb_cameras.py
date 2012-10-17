#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo

"""
import os, sys, glob

#set up enviroment
CONFIGURATION= "Release";
#CONFIGURATION= "Debug";
#export PYTHONPATH=/Projects/vxl/bin/$CONFIGURATION/lib:/Projects/vxl/src/contrib/brl/bseg/boxm2/pyscripts:/Projects/vxl/src/contrib/brl/bseg/boxm2/pyscripts/change:/Projects/vpcl/bin_make/$CONFIGURATION/lib:/Projects/vpcl/vpcl/pyscripts:/Projects/voxels-at-lems-git/boxm2:$PYTHONPATH

sys.path.append("/Projects/vxl/bin/" +CONFIGURATION +"/lib");
sys.path.append("/Projects/vxl/src/contrib/brl/bseg/boxm2/pyscripts");

from boxm2_scene_adaptor import *
from vpgl_adaptor import *
from bbas_adaptor import *

def perturb_cams(root_in, root_out, sigma):

  print "hello"

  in_cams = root_in + "/cams_krt/*.txt"
  out_cam_dir = root_out + "/cams_krt"

  if not os.path.isdir(out_cam_dir +"/"):
     os.makedirs(out_cam_dir + "/");

  cams = glob.glob(in_cams)
  cams.sort()
  pert_log = root_out  + "/pert_log.txt";
  fid = open(pert_log, 'a')

  # import code; code.interact(local=locals())

  for cam in cams:
    #load image and camera
    pcam = load_perspective_camera(cam);
    rng = initialize_rng();
    pert_cam, theta, phi = perturb_camera(pcam, sigma, rng );
    cam_out_name = out_cam_dir + "/" + os.path.basename(cam);
    print cam_out_name
    save_perspective_camera(pert_cam, cam_out_name);
    data = str(theta) + ' ' + str(phi) + '\n'
    fid.write(data)

  fid.close();

if __name__ == "__main__":


  sigma = 0.08
  trial = 4;

  root_in = "/Users/isa/Experiments/reg3d_eval/downtown_dan/original"
  root_out = "/Users/isa/Experiments/reg3d_eval/downtown_dan/pert_008_" + str(trial);

  perturb_cams(root_in, root_out, sigma)
