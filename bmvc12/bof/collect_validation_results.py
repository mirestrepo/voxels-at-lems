#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo

"""

import os
import sys
import time
from optparse import OptionParser
import numpy as np
from sklearn import preprocessing, neighbors, svm
from sklearn.naive_bayes import MultinomialNB 
from sklearn.metrics import *
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.cm as cmt


def save_results(true_labels, predicted_labels, clf_name, classification_dir):
  cm_int = confusion_matrix (true_labels, predicted_labels);

  p, r, f1, s = precision_recall_fscore_support(true_labels, predicted_labels,labels=np.arange(0,len(class_names)))
  cm_float = cm_int.transpose().astype('float');
#  print cm_float

  for col in range(0,5):
    cm_float[:,col]=cm_float[:,col]/s[col]; 
    
#  import code; code.interact(local=locals())

  report = classification_report(true_labels, predicted_labels, np.arange(0,len(class_names)), class_names);
  # Save results
  plt.imsave(classification_dir + '/' + clf_name + "_cm.png", cm_float ,  cmap=cmt.gray)
  float_cm_file = classification_dir +'/' + clf_name + "_float_cm.txt"
  fos = open(float_cm_file, 'w');
  np.savetxt(fos,cm_float);
  fos.close();
  # Show confusion matrix
  fig = plt.figure()
  ax = fig.add_subplot(111)
  cax = ax.matshow(cm_float, cmap=cmt.gray)
  classes = ['Plane', 'Car', 'House', "Building", "Parking"];
  ax.set_xticks(np.arange(0,5))
  ax.set_yticks(np.arange(0,5))
  ax.set_xticklabels(classes ,fontsize= 12)
  ax.set_yticklabels(classes ,fontsize= 12)
  ax.axis('image')
  plt.colorbar(cax)
  plt.autoscale(tight=True);
  plt.axis(tight=True);
#  plt.show()
  plt.savefig(classification_dir +'/' + clf_name + "_float_cm.pdf")
  plt.savefig(classification_dir +'/' + clf_name + "_float_cm.tif")
  plt.savefig(classification_dir +'/' + clf_name + "_float_cm.svg")

  plt.close();
  
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
  
  prf1s_file = classification_dir +'/' + clf_name + "_prf1s.txt"
  fos = open(prf1s_file, 'w');
  np.savetxt(fos,np.column_stack((p, r, f1, s)));
  fos.close();


#*******************The Main Algorithm ************************#
if __name__=="__main__":

  parser = OptionParser()
  parser.add_option("-r", "--radius", action="store", type="int", dest="radius", help="radius (multiple of resolution)");
  parser.add_option("-p", "--percent", action="store", type="int", dest="percentile", help="percentile of original samples");
  parser.add_option("-d", "--descriptor", action="store", type="string", dest="descriptor_type", help="name of the descriptor i.e FPFH");
  parser.add_option("-k", "--nmeans", action="store", type="int", dest="K", help="number of means");
  (opts, args) = parser.parse_args()
  print opts
  print args

  ft=opts.descriptor_type;
  radius=opts.radius;
  percentile=opts.percentile;
  K=opts.K;
  trials = (0,3,4)
#  trials = (0,1, 2, 3,4)
#  trials = (0,1, 2, 3)

#  ft="ShapeContext";
#  radius=30;
#  percentile=90;
#  K=500;
#  trials = (0,1, 2, 3)



#*************************************************************************
# Read all labels and get average confusion matrix and average report
#*************************************************************************
  class_names = ["planes", "cars", "residential", "buildings", "parking"];
  feature_name = ft + "_" + str(radius);
   
  #Where results will be saved
  avg_classification_dir = "/Users/isa/Experiments/bof_bmvc12/" + "/average/" + feature_name   + "/percentile_" + str(percentile) 
  avg_classification_dir = avg_classification_dir + "/classification_" + str(K);

  if not os.path.exists(avg_classification_dir + "/"):
    os.makedirs(avg_classification_dir);

  #*************************************************************************
  # Bayes
  #*************************************************************************
  bayes_clf_name="bayes"

  descriptor_dir = "/Users/isa/Experiments/bof_bmvc12/" + "/trial_" + str(0) + "/" + feature_name   + "/percentile_" + str(percentile) 
  classification_dir = descriptor_dir + "/classification_" + str(K)
  labels_file = classification_dir +'/' + bayes_clf_name + "_labels.txt"
  fis = open(labels_file, 'r');
  labels = np.genfromtxt(fis);
  fis.close();


  for trial in trials:
    descriptor_dir = "/Users/isa/Experiments/bof_bmvc12/" + "/trial_" + str(trial) + "/" + feature_name   + "/percentile_" + str(percentile) 
    classification_dir = descriptor_dir + "/classification_" + str(K);
    labels_file = classification_dir +'/' + bayes_clf_name + "_labels.txt"
    fis = open(labels_file, 'r');
    labels = np.vstack((labels, np.genfromtxt(fis)));
    fis.close();
    
   
  save_results(labels[:,0], labels[:,1], bayes_clf_name, avg_classification_dir)

  #*************************************************************************
  # SVM
  #*************************************************************************

  gamma_range = [10. ** -1, 1, 10. ** 1]
  C_range = [10. ** -2, 1, 10. ** 2]
  for C in C_range:
      for gamma in gamma_range:
        labels=[];
        descriptor_dir = "/Users/isa/Experiments/bof_bmvc12/" + "/trial_" + str(0) + "/" + feature_name   + "/percentile_" + str(percentile) 
        labels_file = classification_dir +'/' + "svm_gamma_%.1f_C%.2f" % (gamma, C)  + "_labels.txt"
        fis = open(labels_file, 'r');
        labels = np.genfromtxt(fis);
        fis.close();
        
        for trial in trials:
          descriptor_dir = "/Users/isa/Experiments/bof_bmvc12/" + "/trial_" + str(trial) + "/" + feature_name   + "/percentile_" + str(percentile) 
          classification_dir = descriptor_dir + "/classification_" + str(K);
          labels_file = classification_dir +'/' + "svm_gamma_%.1f_C%.2f" % (gamma, C) + "_labels.txt"
          fis = open(labels_file, 'r');
          labels = np.vstack((labels, np.genfromtxt(fis)));
          fis.close();

            
        save_results(labels[:,0], labels[:,1], "svm_gamma_%.1f_C%.2f" % (gamma, C), avg_classification_dir)

  #*************************************************************************
  # Knn
  #*************************************************************************

  clf_name="knn"

  knn_nn = [1,2,3];  #we'll run k-nn fo these cases of k
  for nn in knn_nn: 
    labels=[]
    descriptor_dir = "/Users/isa/Experiments/bof_bmvc12/" + "/trial_" + str(0) + "/" + feature_name   + "/percentile_" + str(percentile) 
    labels_file = classification_dir +'/' + str(nn) +"nn" + "_labels.txt"
    fis = open(labels_file, 'r');
    labels = np.genfromtxt(fis);
    fis.close();   
    for trial in trials:
      descriptor_dir = "/Users/isa/Experiments/bof_bmvc12/" + "/trial_" + str(trial) + "/" + feature_name   + "/percentile_" + str(percentile) 
      classification_dir = descriptor_dir + "/classification_" + str(K);
      labels_file = classification_dir +'/' + str(nn) +"nn" + "_labels.txt"
      fis = open(labels_file, 'r');
      labels = np.vstack((labels, np.genfromtxt(fis)));
      fis.close();

        
    save_results(labels[:,0], labels[:,1], str(nn) +"nn", avg_classification_dir)

  