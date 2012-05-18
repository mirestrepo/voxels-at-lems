#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo

"""
import os
import sys
import pickle
import time
import numpy as np
from bmvc12_adaptor import *
from sklearn.cluster import MiniBatchKMeans,  KMeans
from sklearn import preprocessing
from optparse import OptionParser



def quantize_descriptors(labels, K):
  quantized_obj = np.zeros(K);
  for i in range(0,K):
    quantized_obj[i] = np.sum(labels==i)
    
  return quantized_obj


#*********************Quantization on Test Data ************************
if __name__=="__main__":
  
  parser = OptionParser()
  parser.add_option("-r", "--radius", action="store", type="int", dest="radius", help="radius (multiple of resolution)");
  parser.add_option("-p", "--percent", action="store", type="int", dest="percentile", help="percentile of original samples");
  parser.add_option("-t", "--trial", action="store", type="int", dest="trial", help="trial number- corresponding to a validation set");
  parser.add_option("-d", "--descriptor", action="store", type="string", dest="descriptor_type", help="name of the descriptor i.e FPFH");
  parser.add_option("-k", "--nmeans", action="store", type="int", dest="K", help="number of means");
  (opts, args) = parser.parse_args()
  print opts
  print args
  
  ft=opts.descriptor_type;
  radius=opts.radius;
  trial=opts.trial;
  percentile=opts.percentile;
  K=opts.K;
  
  class_names = ["planes", "cars", "residential", "buildings", "parking"];

  
  feature_name = ft + "_" + str(radius);
  
  descriptor_dir = "/Users/isa/Experiments/bof_bmvc12/" + "/trial_" + str(trial) + "/" + feature_name   + "/percentile_" + str(percentile)  
  kmeans_dir = descriptor_dir + "/k_means_" + str(K);
  k_means_file = kmeans_dir+ "/k_means_class.pkl"; 
  
  #*****************Load KMeans Model********************/
  fis = open(k_means_file, 'rb');
  estimator = pickle.load(fis); #-1 refers to highest protocol available
  fis.close()
  #******************************************************/

  #*************Quatization for every object*************/
  #paths of all testig objects
  ply_paths = [];
  all_feature_paths = [];

  #collect all train objects
  for obj_class in class_names:
    parse_train_objects(obj_class, feature_name,  percentile, trial, ply_paths, all_feature_paths);
  
  ply_paths = [];
  #add  all test objects
  for obj_class in class_names:
    parse_test_objects(obj_class, feature_name,  percentile, trial, ply_paths, all_feature_paths);
  
  ply_paths = [];
 
   
  print "Number of objects: " + str(len(all_feature_paths));  

  mark1 = time.time();

  #for every object
  for p in range(0,len(all_feature_paths)):
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
    
    descriptors_normalized = preprocessing.normalize(descriptors, norm='l1')

    labels = estimator.predict(descriptors_normalized);
    
    quantized_object = quantize_descriptors(labels, K);
    
    file_out = all_feature_paths[p][:-len(".npy")]   
    file_out = file_out  + "_k_means " +str(K) + "_trial_" + str(trial) + ".txt";
    fos = open(file_out, 'w')  
    np.savetxt(fos, quantized_object);     
    fos.close()   
    #print(quantized_object)
  
  mark2 = time.time();
  fos = open(kmeans_dir + "/quantization_time.txt", 'w')  
  fos.write(str(mark2-mark1));     
  fos.close() 
  
  print "Quantization took " + str(mark2-mark1) + "seconds"

      
