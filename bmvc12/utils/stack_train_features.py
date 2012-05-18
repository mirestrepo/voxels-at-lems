#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo
May 2, 2012 
A script to parse training features from all categories and stack them into a singe array
"""



#*******************The Main Algorithm ************************#
if __name__=="__main__":
  
  import os
  import sys
  import time
  import numpy as np
  from bmvc12_adaptor import *
  from sklearn.cluster import MiniBatchKMeans
  from sklearn.externals import joblib
  from optparse import OptionParser

  
  parser = OptionParser()
  parser.add_option("-r", "--radius", action="store", type="int", dest="radius", help="radius (multiple of resolution)");
  parser.add_option("-p", "--percent", action="store", type="int", dest="percentile", help="percentile of original samples");
  parser.add_option("-t", "--trial", action="store", type="int", dest="trial", help="trial number- corresponding to a validation set");
  parser.add_option("-d", "--descriptor", action="store", type="string", dest="descriptor_type", help="name of the descriptor i.e FPFH");

  (opts, args) = parser.parse_args()

  #all categories
  class_names = ["planes", "cars", "residential", "buildings", "parking"];
  radius = opts.radius;
  percentile = opts.percentile;
  trial=opts.trial;
  ft=opts.descriptor_type
  
  feature_name = ft + "_" + str(radius);

  #paths of all trainig objects
  train_paths = [];
  all_feature_paths = [];

  #collect all paths
  for obj_class in class_names:
    parse_train_objects(obj_class, feature_name,  percentile, trial, train_paths, all_feature_paths);
   
 
  print "Number of training objects: " + str(len(all_feature_paths));  

  start_time = time.time();

  #add al descriptors to huge matrix
  fis = open(all_feature_paths[0], 'rb')
  train_descriptors=np.load(fis);
  nan_rows = np.sum(np.isnan(train_descriptors), axis=1) > 0;
  print train_descriptors.shape
  if (np.sum(nan_rows)>0):
    print "Number of NAN rows: " + str(sum(nan_rows))
    train_descriptors = train_descriptors[np.logical_not(nan_rows)];
    print train_descriptors.shape
  fis.close();


  for p in range(1,len(all_feature_paths)):
    print all_feature_paths[p]
    if not os.path.exists(all_feature_paths[p]):
      print "Warning: File not found!"
      continue;
    fis = open(all_feature_paths[p], 'rb')
    descriptors= np.load(fis);
    #Detect NAN rows
    nan_rows = np.sum(np.isnan(descriptors), axis=1) > 0;
    print descriptors.shape
    if (np.sum(nan_rows)>0):
      print "Number of NAN rows: " + str(sum(nan_rows))
      descriptors = descriptors[np.logical_not(nan_rows)];
      print descriptors.shape
    fis.close()
    train_descriptors =np.vstack((train_descriptors, descriptors));
    
  rows, cols = train_descriptors.shape;
    
  #**************Save to File ****************#
  descriptor_dir = "/Users/isa/Experiments/bof_bmvc12" + "/trial_" + str(trial) + "/" + feature_name   + "/percentile_" + str(percentile)  
  if not os.path.exists(descriptor_dir + "/"):
    os.makedirs(descriptor_dir);
    
  descriptors_file = descriptor_dir + "/train_descriptors.npy" ; 
  print "Dimension of training data: (" + str(rows) + ',' + str(cols) + ")" ;
  print "Saving file to : " + descriptors_file;

  fos = open(descriptors_file, 'wb')
  np.save(fos, train_descriptors);
  fos.close();

  print("Time stacking descriptors")
  print(time.time() - start_time);

  print train_descriptors;