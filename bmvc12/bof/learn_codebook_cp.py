#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo
May 1, 2012
Learn a feature dictionary using mini-batch k-means
"""

#*******************The Main Algorithm ************************#
if __name__=="__main__":

  import os
  import sys
  import pickle
  import time
  import numpy as np
  from bmvc12_adaptor import *
  from sklearn.cluster import MiniBatchKMeans,  KMeans
  from sklearn import preprocessing
  from optparse import OptionParser
  from scipy.sparse import coo_matrix


  
  parser = OptionParser()
  parser.add_option("-r", "--radius", action="store", type="int", dest="radius", help="radius (multiple of resolution)");
  parser.add_option("-p", "--percent", action="store", type="int", dest="percentile", help="percentile of original samples");
  parser.add_option("-t", "--trial", action="store", type="int", dest="trial", help="trial number- corresponding to a validation set");
  parser.add_option("-d", "--descriptor", action="store", type="string", dest="descriptor_type", help="name of the descriptor i.e FPFH");

  (opts, args) = parser.parse_args()
  print opts
  print args
  

  #all categories
  class_names = ["planes", "cars", "residential", "buildings", "parking"];
  percentile = opts.percentile;
  trial=opts.trial;
  ft = opts.descriptor_type;
  radius = opts.radius;
  feature_name = ft + "_" + str(radius);
  verbose = False;

  descriptor_dir = "/Users/isa/Experiments/bof_bmvc12/" + "/trial_" + str(trial) + "/" + feature_name   + "/percentile_" + str(percentile)  
  descriptors_file = descriptor_dir + "/train_descriptors.npy" ; 

  #################Stack the train descriptors
  #paths of all trainig objects
  train_paths = [];
  all_feature_paths = [];

  #collect all paths
  for obj_class in class_names:
    parse_train_objects(obj_class, feature_name,  percentile, trial, train_paths, all_feature_paths);

  print "Number of training objects: " + str(len(all_feature_paths));  
  mark = time.time();
  train_descriptors = np.zeros((1900000, 1980), dtype=float)
  start_row=0;
  end_row=0
    
  for p in range(0,len(all_feature_paths)):
    if verbose: 
      print all_feature_paths[p]
    if not os.path.exists(all_feature_paths[p]):
      print "Warning: File not found!"
      continue;
    fis = open(all_feature_paths[p], 'rb')
    descriptors= np.load(fis);
    fis.close()
    rows, cols = descriptors.shape;
    end_row = start_row + rows;
    train_descriptors[np.arange(start_row, end_row), :]=descriptors;
    start_row = end_row;
      
    
  train_descriptors.resize((end_row,1980));
  rows, cols = train_descriptors.shape;

  print "Dimension of training data: (" + str(rows) + ',' + str(cols) + ")" ;
  print train_descriptors

  #Detect NAN rows
#  nan_rows = np.sum(np.isnan(train_descriptors), axis=1) > 0;
#  if (np.sum(nan_rows)>0):
#    print "Number of NAN rows: " + str(sum(nan_rows))
#    train_descriptors = train_descriptors[np.logical_not(nan_rows)];
#    print train_descriptors.shape
#  nan_rows=[];
#  rows, cols = train_descriptors.shape;
#
  mark1 = time.time();
  print "Reading train descriptors took " + str(mark1-mark) + "seconds"
  print "Dimension of training data: (" + str(rows) + ',' + str(cols) + ")" ;
  print train_descriptors
   
  #****************KMeans Clustering***************************
#  estimator = KMeans(init='random',k=K, n_init=10);
  train_descriptors_sparse = coo_matrix(train_descriptors).tocsr()
  train_descriptos=[];
  descriptors_normalized = preprocessing.normalize(train_descriptors_sparse, norm='l1')
    
  mark2 = time.time();
  print "Convertin to sparse took " + str(mark2-mark1) + "seconds"
 
  for K in (20, 50, 100, 200, 500):
    print "Starting K-means with K: " + str(K);

    batch_s = 50 * K;
    estimator = MiniBatchKMeans(init='random',k=K, batch_size=batch_s, n_init=5, max_no_improvement=10, max_iter=500);
    estimator.fit(descriptors_normalized);

    #save the k-means estimator
    output_dir = descriptor_dir + "/k_means_" + str(K);
    
    if not os.path.exists(output_dir + "/"):
      os.makedirs(output_dir);
      
    file_out = output_dir+ "/k_means_class.pkl"; 
    means_file_out = output_dir + "/cluster_centers.txt"

    fos = open(file_out, 'wb');
    pickle.dump(estimator, fos, -1); #-1 refers to highest protocol available which makes it more efficient?
    fos.close()
     
    means_fos = open(means_file_out, 'w')  
    np.savetxt(means_fos, estimator.cluster_centers_);     
    means_fos.close()   
    
    mark3 = time.time();
    print "MinibatchKmeans took " + str(mark3-mark2) + "seconds"
  #  print "Means:"; 
    
    fos = open(output_dir + "/MinibatchKmeans_time.txt", 'w')  
    fos.write(str(mark2-mark1));     
    fos.close()   
    
  #  print  estimator.cluster_centers_ 
  #  print  estimator.labels_
  #  print  np.min(estimator.labels_)
  #  print  np.max(estimator.labels_)

                     
