#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo

"""


import os
import sys
import numpy as np
from bmvc12_adaptor import *
from sklearn.cluster import MiniBatchKMeans
from sklearn.externals import joblib
import code;
filename="/Users/isa/Experiments/shape_features_bmvc12/site_1/FPFH_10/planes_90/mesh_0.txt";

#confusion matrix percent
#obj= np.genfromtxt(filename, skiprows=1);

paths = [];
feature_paths = [];
parse_train_objects("planes", "SpinImage_10",  90, 0, paths, feature_paths);

class_descriptors=np.genfromtxt(feature_paths[0], skiprows=1);

for p in range(1,len(paths)):
#  print paths[p]
  print feature_paths[p]
  obj= np.genfromtxt(feature_paths[p], skiprows=1);
  print obj.shape
  class_descriptors =np.append(class_descriptors, obj, axis=0);
  
rows, cols = class_descriptors.shape;
batch_size = rows*0.1;
  
estimator = MiniBatchKMeans(init='random', k=3, batch_size=batch_size,
                      n_init=10, max_no_improvement=10, verbose=0)
estimator.fit(class_descriptors); 
#code.interact(local=locals())
print estimator.cluster_centers_;

output = open('test.pkl', 'w')
joblib.dump(estimator, output) 
output.close();
output = open('test.pkl', 'r')

estimator2=pickle.load(output) 
print estimator2.cluster_centers_;

print estimator.labels_;

#print class_descriptors.shape
#print class_descriptors