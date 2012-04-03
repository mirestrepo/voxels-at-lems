import sys
import os, os.path

###############################################
# scene_registry.py
# holds my list of scenes to directory maps
###############################################

#SCENE PATHS
scene_paths = {}

data_candidates = [ 
                    "/data/",
                    "/data/models",
                    os.path.expanduser("~/data/"),
                    os.path.expanduser("~/data/models/")
                  ]


def scene_root(scene_name):
  if not scene_name or scene_name == "": 
    print "NO SCENE GIVEN!"
    sys.exit(-1)
  for cand in data_candidates:
    if os.path.exists( cand+"/"+scene_name ):
      return cand+"/"+scene_name
  
  #otherwise no path, throw error
  print "SCENE: ", scene_name, " not found!!!!"
  print_scenes()
  sys.exit(-1)

def print_scenes():
  for cand in data_candidates:
    print "Checking for data in: ", cand
    if os.path.exists(cand):
      print os.listdir(cand)
    else:
      print "  ... ", cand, " not found!"
  
