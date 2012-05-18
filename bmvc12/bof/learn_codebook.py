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

  
  parser = OptionParser()
  parser.add_option("-r", "--radius", action="store", type="int", dest="radius", help="radius (multiple of resolution)");
  parser.add_option("-p", "--percent", action="store", type="int", dest="percentile", help="percentile of original samples");
  parser.add_option("-t", "--trial", action="store", type="int", dest="trial", help="trial number- corresponding to a validation set");
  parser.add_option("-d", "--descriptor", action="store", type="string", dest="descriptor_type", help="name of the descriptor i.e FPFH");
  parser.add_option("-k", "--nmeans", action="store", type="int", dest="K", help="number of means");

  (opts, args) = parser.parse_args()
  print opts
  print args

  #all categories
  class_names = ["planes", "cars", "residential", "buildings", "parking"];
  percentile = opts.percentile;
  K = opts.K; #the number of means
  batch_s = 100 * K;
  trial=opts.trial;
  ft = opts.descriptor_type;
  radius = opts.radius;
  feature_name = ft + "_" + str(radius);

  descriptor_dir = "/Users/isa/Experiments/bof_bmvc12/" + "/trial_" + str(trial) + "/" + feature_name   + "/percentile_" + str(percentile)  
  descriptors_file = descriptor_dir + "/train_descriptors.npy" ; 

  mark = time.time();
  fis = open(descriptors_file, 'rb')
  train_descriptors = np.load(fis);
  fis.close();
  rows, cols = train_descriptors.shape;

  mark1 = time.time();
  print "Reading train descriptors took " + str(mark1-mark) + "seconds"
  print "Dimension of training data: (" + str(rows) + ',' + str(cols) + ")" ;
#  print train_descriptors
   
  #****************KMeans Clustering***************************
  estimator = MiniBatchKMeans(init='random',k=K, batch_size=batch_s, n_init=10, max_no_improvement=20, max_iter=500);
#  estimator = KMeans(init='random',k=K, n_init=10);

  descriptors_normalized = preprocessing.normalize(train_descriptors, norm='l1')
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
  
  mark2 = time.time();
  print "MinibatchKmeans took " + str(mark2-mark1) + "seconds"
#  print "Means:"; 
  
  fos = open(output_dir + "/MinibatchKmeans_time.txt", 'w')  
  fos.write(str(mark2-mark1));     
  fos.close()   
  
#  print  estimator.cluster_centers_ 
#  print  estimator.labels_
#  print  np.min(estimator.labels_)
#  print  np.max(estimator.labels_)

                     
