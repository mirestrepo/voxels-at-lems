# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 14:38:46 2011
Plot pca test error vs train error
@author: -
"""

# Computes the gaussian gradients on a boxm_alpha_scene

import os;
import optparse;
import time;
import sys;
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cmt
import glob


main_dir="/Users/isa/Experiments/BOF/helicopter_providence";

nobjects = 120;

thresh = [1, 2, 5, 10, 20];

num_means=20;

k_label = ['$\kappa=0.01$' , '$\kappa=0.0075$', '$\kappa=0.005$'];

for k in range(1,4):
  param_dir= main_dir + "/corners/k_" + str(k);
  #param_dir= main_dir + "/beaudet_corners";
  corners_dir= param_dir+ "/global_corners";
  
  accuracy = [];
  for t in thresh: 

    bof_dir=param_dir +"/bof/thresh_" + str(t);
    classification_dir=bof_dir +"/classification_" + str(num_means)
    accuracy_file = classification_dir + "/accuracy.txt"

    f = open(accuracy_file, 'r');
      
    lines=[];
    lines = f.readlines();
    
    print lines
    print str(int(lines[0]))
      
    accuracy.append(float(lines[0])/ nobjects);
    
    if (int(lines[1]) != nobjects):
      print "error in: " + classification_dir
  
  x = [1, 2, 5, 10, 50];
     
  plt.plot(x, accuracy, label=k_label[k-1]);
  plt.xlabel('Percentage of samples used for recognition',fontsize= 'large');

  plt.ylabel('Accuracy',fontsize= 'large');  
  plt.hold(True);

plt.legend(loc='lower right');  
plt.show(); 
plt.hold(False);
