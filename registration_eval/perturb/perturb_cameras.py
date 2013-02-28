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

def perturb_cams(root_in, root_out, sigma, rng):

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
    pert_cam, theta, phi = perturb_camera(pcam, sigma, rng );
    cam_out_name = out_cam_dir + "/" + os.path.basename(cam);
    print cam_out_name
    save_perspective_camera(pert_cam, cam_out_name);
    data = str(theta) + ' ' + str(phi) + '\n'
    fid.write(data)

  fid.close();

if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument("--root_dir",       action="store",   type=str,
      dest="root_dir",
      default="",
      help="Path to root directory")
  parser.add_argument("--si",          action="store",   type=int,
        dest="si",       default=0,
        help="Sigma index, where sigma = [0.05, 0.1, 0.15] ")
  args = parser.parse_args()

  print args

  gt_root_dir = args.root_dir + "/original"
  sigma = [0.05, 0.1, 0.15]
  sigma_str = ["005", "01", "015"]
  descriptor_type = args.descriptor
  radius = 30
  percentile = 99
  rng = initialize_rng();


  if args.perturb:
      import perturb_cameras
      print "Peturbing cameras"
      for si in range(0, len(sigma)):
          for ti in range(0, 9):
              root_in = gt_root_dir
              root_out = args.root_dir + "/pert_" + sigma_str[si] + "_" + str(ti)
              perturb_cameras.perturb_cams(root_in, root_out, sigma[si], rng)

