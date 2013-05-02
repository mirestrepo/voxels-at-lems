#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo
Set of common utilities for bmvc12 scripts

"""

from xml.etree.ElementTree import ElementTree


def parse_scene_resolution(scene_info_file):

    print 'Parsing: ' + scene_info_file

    #parse xml file
    scene_info_tree = ElementTree();
    scene_info_tree.parse(scene_info_file);

    #find scene paths
    res_elm = scene_info_tree.getroot().find('resolution');

    if res_elm is None:
      print "Invalid scene info file: No resolution element"
      sys.exit(-1);

    res = res_elm.get('val');

    return float(res);


def parse_train_objects(category, feature_name, percentile, trial, paths, feature_paths, verbose=False):

    info_file = "/Users/isa/Experiments/bof_bmvc12/trial_" + str(trial) + "/bof_category_train_info.xml"

    info_tree = ElementTree();
    info_tree.parse(info_file);


    scene_elms = info_tree.findall('scene');

    if verbose:
      print 'Found: ' + str(len(scene_elms)) + 'scenes'


    for scene in scene_elms:

      site_name = scene.get('site_name');

      obj_elms = scene.findall('object');

      if obj_elms is None:
        print "Invalid scene info file: No objects element"
        sys.exit(-1);

      if verbose:
        print 'Found: ' + str(len(obj_elms)) + 'objects'

      for elm in obj_elms:
          class_name = elm.get('class_name');
          if(class_name==category):
            mesh_name = elm.get('ply_name')
            ply_path = "/data/helicopter_providence_3_12/" + site_name + "/objects_with_aux/" + category + "_" + str(percentile) + "/" + mesh_name + ".ply";
            feature_path = "/Users/isa/Experiments/shape_features_bmvc12/" + site_name + "/" + feature_name + "/" + category + "_" + str(percentile) + "/" + mesh_name + ".npy";
            paths.append(ply_path);
            feature_paths.append(feature_path)


def parse_test_objects(category, feature_name, percentile, trial, paths, feature_paths):

  info_file = "/Users/isa/Experiments/bof_bmvc12/trial_" + str(trial) + "/bof_category_test_info.xml"

  info_tree = ElementTree();
  info_tree.parse(info_file);


  scene_elms = info_tree.findall('scene');
  print 'Found: ' + str(len(scene_elms)) + 'scenes'


  for scene in scene_elms:

    site_name = scene.get('site_name');

    obj_elms = scene.findall('object');

    if obj_elms is None:
      print "Invalid scene info file: No objects element"
      sys.exit(-1);

    print 'Found: ' + str(len(obj_elms)) + 'objects'

    for elm in obj_elms:
        class_name = elm.get('class_name');
        if(class_name==category):
          mesh_name = elm.get('ply_name')
          ply_path = "/data/helicopter_providence_3_12/" + site_name + "/objects_with_aux/" + category + "_" + str(percentile) + "/" + mesh_name + ".ply";
          feature_path = "/Users/isa/Experiments/shape_features_bmvc12/" + site_name + "/" + feature_name + "/" + category + "_" + str(percentile) + "/" + mesh_name + ".npy";
          paths.append(ply_path);
          feature_paths.append(feature_path)



def parse_train_objects_no_object(category, feature_name, percentile, trial, paths, feature_paths, verbose=False):

    info_file = "/Users/isa/Experiments/bof_bmvc12/trial_" + str(trial) + "/bof_category_train_info_no_object.xml"

    info_tree = ElementTree();
    info_tree.parse(info_file);


    scene_elms = info_tree.findall('scene');

    if verbose:
      print 'Found: ' + str(len(scene_elms)) + 'scenes'


    for scene in scene_elms:

      site_name = scene.get('site_name');

      obj_elms = scene.findall('object');

      if obj_elms is None:
        print "Invalid scene info file: No objects element"
        sys.exit(-1);

      if verbose:
        print 'Found: ' + str(len(obj_elms)) + 'objects'

      for elm in obj_elms:
          class_name = elm.get('class_name');
          if(class_name==category):
            mesh_name = elm.get('ply_name')
            ply_path = "/Users/isa/Experiments/helicopter_providence_3_12/" + site_name + "/objects_with_aux/" + category + "_" + str(percentile) + "/" + mesh_name + ".ply";
            feature_path = "/Users/isa/Experiments/shape_features_bmvc12/" + site_name + "/" + feature_name + "/" + category + "_" + str(percentile) + "/" + mesh_name + ".npy";
            paths.append(ply_path);
            feature_paths.append(feature_path)

    #append the other categories
    parse_train_objects(category, feature_name, percentile, trial, paths, feature_paths)



def parse_test_objects_no_object(category, feature_name, percentile, trial, paths, feature_paths):

  info_file = "/Users/isa/Experiments/bof_bmvc12/trial_" + str(trial) + "/bof_category_test_info_no_object.xml"

  info_tree = ElementTree();
  info_tree.parse(info_file);


  scene_elms = info_tree.findall('scene');
  print 'Found: ' + str(len(scene_elms)) + 'scenes'


  for scene in scene_elms:

    site_name = scene.get('site_name');

    obj_elms = scene.findall('object');

    if obj_elms is None:
      print "Invalid scene info file: No objects element"
      sys.exit(-1);

    print 'Found: ' + str(len(obj_elms)) + 'objects'

    for elm in obj_elms:
        class_name = elm.get('class_name');
        if(class_name==category):
          mesh_name = elm.get('ply_name')
          ply_path = "/Users/isa/Experimentshelicopter_providence_3_12/" + site_name + "/objects_with_aux/" + category + "_" + str(percentile) + "/" + mesh_name + ".ply";
          feature_path = "/Users/isa/Experiments/shape_features_bmvc12/" + site_name + "/" + feature_name + "/" + category + "_" + str(percentile) + "/" + mesh_name + ".npy";
          paths.append(ply_path);
          feature_paths.append(feature_path)

   #append the other categories
  parse_test_objects(category, feature_name, percentile, trial, paths, feature_paths)
