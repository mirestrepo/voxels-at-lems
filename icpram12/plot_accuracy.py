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


main_dir="/Users/isa/Experiments/BOF/helicopter_providence/pca";
bof_dir=main_dir +"/bof";

accuracy = [];

nobjects = 120;

means = [2, 4, 8, 10, 20, 50, 100];

fig=plt.figure()
ax = fig.add_subplot(111);

for num_means in means: 

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
    
ax.plot(means, accuracy, label='PCA');
x = np.arange(1, len(accuracy), 1);

plt.hold(True);

#****************************Taylor*************************************#
main_dir="/Users/isa/Experiments/BOF/helicopter_providence/taylor";
bof_dir=main_dir +"/bof";

accuracy = [];

nobjects = 120;

means = [2, 4, 8, 10, 20, 50, 100];

for num_means in means: 

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
    
ax.plot(means, accuracy, label='Taylor');
x = np.arange(1, len(accuracy), 1);
ax.set_xlabel('Number of clusters used for recognition',fontsize= 18);
ax.set_ylabel('Accuracy',fontsize= 18);  
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels,'lower right')

ax.set_ylim((0,1.01));
ylabels = np.arange(0,1.1, 0.2);
ax.set_yticklabels(ylabels, fontsize= 14)

xlabels = np.arange(0,101, 20);
ax.set_xticklabels(xlabels, fontsize= 14)

plt.show(); 