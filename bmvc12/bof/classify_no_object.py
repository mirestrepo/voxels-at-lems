#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo
May 2, 2012
Classify objects using Knn-Classifier
"""
import os
import sys
import time
from optparse import OptionParser
import numpy as np
from bmvc12_adaptor import *
from sklearn import preprocessing, neighbors, svm
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import *
from sklearn.multiclass import OneVsRestClassifier
import matplotlib.pyplot as plt
import matplotlib.cm as cmt

def save_results(true_labels, predicted_labels, clf_name, classification_dir):
  cm_int = confusion_matrix (true_labels, predicted_labels);
  cm_float = cm_int/np.apply_along_axis(np.sum, 1, cm_int).astype('float');
  report = classification_report(true_labels, predicted_labels, np.arange(0,len(class_names)), class_names);
  # Save results
  plt.imsave(classification_dir + '/' + clf_name + "_cm.png", cm_float ,  cmap=cmt.gray)
  float_cm_file = classification_dir +'/' + clf_name + "_float_cm.txt"
  fos = open(float_cm_file, 'w');
  np.savetxt(fos,cm_float);
  fos.close();
  int_cm_file = classification_dir +'/' + clf_name + "_int_cm.txt"
  fos = open(int_cm_file, 'w');
  np.savetxt(fos,cm_int);
  fos.close();
  report_file = classification_dir +'/' + clf_name + "_report.txt"
  fos = open(report_file, 'w');
  fos.write(report);
  fos.close();
  labels_file = classification_dir +'/' + clf_name + "_labels.txt"
  fos = open(labels_file, 'w');
  np.savetxt(fos,np.column_stack((true_labels,predicted_labels)));
  fos.close();

  p, r, f1, s = precision_recall_fscore_support(true_labels, predicted_labels,labels=np.arange(0,len(class_names)))
  prf1s_file = classification_dir +'/' + clf_name + "_prf1s.txt"
  fos = open(prf1s_file, 'w');
  np.savetxt(fos,np.column_stack((p, r, f1, s)));
  fos.close();



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
  knn_nn = [1,2,3];  #we'll run k-nn fo these cases of k

  class_names = ["planes", "cars", "residential", "buildings", "parking", "background"];
  feature_name = ft + "_" + str(radius);
  descriptor_dir = "/Users/isa/Experiments/bof_bmvc12/" + "/trial_" + str(trial) + "/" + feature_name   + "/percentile_" + str(percentile)
  classification_dir = descriptor_dir + "/classification_no_object_" + str(K);
  if not os.path.exists(classification_dir + "/"):
    os.makedirs(classification_dir);

  mark1 = time.time();

  #*******************Collect Train Data************************************#
  num_objects=np.zeros(len(class_names), dtype=int)
  all_feature_paths=[];
  for ci in range(0, len(class_names)):
    ply_paths=[];
    obj_class = class_names[ci]
    parse_train_objects_no_object(obj_class, feature_name,  percentile, trial, ply_paths, all_feature_paths);
    num_objects[ci]=len(ply_paths);


  train_data = np.zeros([np.sum(num_objects),K], dtype=float)
  train_labels = np.ones([np.sum(num_objects)],dtype=int);
  train_labels[np.arange(0, num_objects[0])] = np.tile(0, (num_objects[0]));
  for li in range (1, len(num_objects)):
    i= sum(num_objects[0:li])
    j= sum(num_objects[0:li+1])
    train_labels[np.arange(i,j)] = np.tile(li,(num_objects[li]));


  #get the data
  for p in range(0,len(all_feature_paths)):
    print all_feature_paths[p]
    if not os.path.exists(all_feature_paths[p]):
      print "Warning: File not found!"
      continue;

    vq_file = all_feature_paths[p][:-len(".npy")]
    vq_file = vq_file  + "_k_means " +str(K) + "_trial_" + str(trial) + ".txt";
    fis = open(vq_file, 'r')
    vq_object= np.genfromtxt(fis);
    fis.close()

    train_data[p,:]=vq_object

  train_data_normalized = preprocessing.normalize(train_data, norm='l1')

  #*******************Collect Test Data************************************#
  num_objects=np.zeros(len(class_names), dtype=int)
  all_feature_paths=[];
  for ci in range(0, len(class_names)):
    ply_paths=[];
    obj_class = class_names[ci]
    parse_test_objects_no_object(obj_class, feature_name,  percentile, trial, ply_paths, all_feature_paths);
    num_objects[ci]=len(ply_paths);


  test_data = np.zeros([np.sum(num_objects),K], dtype=float)
  test_labels = np.ones([np.sum(num_objects)],dtype=int);
  test_labels[np.arange(0, num_objects[0])] = np.tile(0, (num_objects[0]));
  for li in range (1, len(num_objects)):
    i= sum(num_objects[0:li])
    j= sum(num_objects[0:li+1])
    test_labels[np.arange(i,j)] = np.tile(li,(num_objects[li]));


  #get the data
  for p in range(0,len(all_feature_paths)):
    print all_feature_paths[p]
    if not os.path.exists(all_feature_paths[p]):
      print "Warning: File not found!"
      continue;

    vq_file = all_feature_paths[p][:-len(".npy")]
    vq_file = vq_file  + "_k_means " +str(K) + "_trial_" + str(trial) + ".txt";
    fis = open(vq_file, 'r')
    vq_object= np.genfromtxt(fis);
    fis.close()

    test_data[p,:]=vq_object

  test_data_normalized = preprocessing.normalize(test_data, norm='l1')

  for nn in knn_nn:
    knn_clf = neighbors.KNeighborsClassifier(nn, weights='uniform')
    knn_clf.fit(train_data_normalized, train_labels);
    knn_labels = knn_clf.predict(test_data_normalized)
    print "Number of mislabeled objects (KNN) : %d" % (test_labels != knn_labels).sum()
    save_results(test_labels, knn_labels, str(nn) +"nn", classification_dir)


  mnb_clf = MultinomialNB (fit_prior=False)
  mnb_clf.fit(train_data, train_labels)
  mnb_labels = mnb_clf.predict(test_data)
  print "Number of mislabeled objects (MNB) : %d" % (test_labels != mnb_labels).sum()
  save_results(test_labels, mnb_labels, "bayes", classification_dir)

  gamma_range = [10. ** -1, 1, 10. ** 1]
  C_range = [10. ** -2, 1, 10. ** 2]
  for C in C_range:
      for gamma in gamma_range:
        svm_clf = OneVsRestClassifier(svm.SVC(kernel='rbf', gamma=gamma, C=C))
        svm_clf.fit(train_data_normalized, train_labels)
        svm_labels = svm_clf.predict(test_data_normalized)
        print "Number of mislabeled objects (SVM) : %d" % (test_labels != svm_labels).sum()
        save_results(test_labels, svm_labels, "svm_ova_gamma_%.1f_C%.2f" % (gamma, C), classification_dir)

  mark2 = time.time();
  fos = open(classification_dir + "/classification_time.txt", 'w')
  fos.write(str(mark2-mark1));
  fos.close()
  print "Classification took " + str(mark2-mark1) + "seconds"
