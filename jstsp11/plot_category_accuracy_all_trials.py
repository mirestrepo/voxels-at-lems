# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 14:38:46 2011
Plot pca test error vs train error
@author: Isabel Restrepo
Brown University
"""

import os;
import optparse;
import time;
import sys;
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import glob


main_dir="/Volumes/voxels_archive/Experiments/BOF/helicopter_providence";




nobjects = 120;

trials = [0,1,2,4,5,6,7,8];

num_means=20;

k_label = ['Taylor - EVM' , 'Taylor - PVM', 'Taylor - PMVS' , 'Taylor - PMVS+smoothing'];
colors = ['magenta','blue','green', 'red'];
ncategories = 5;
fig=plt.figure()
ax = fig.add_subplot(111);
plt.hold(True);
plt.autoscale(tight=True);
plt.axis(tight=True);
x=np.arange(0,ncategories);
param_dir= main_dir + "/taylor";
#param_dir= main_dir + "/beaudet_corners";

print "Taylor - EVM";
accuracy = np.zeros((len(trials),ncategories));
row=0;
for trial in trials:
  
    bof_dir=param_dir +"/bof_cross_validation/trial_"+str(trial);
    classification_dir=bof_dir +"/classification_" + str(num_means)
    cm_file=classification_dir + "/confussion_matrix.txt";
    #confusion matrix percent
    cm = np.genfromtxt(cm_file);  
    accuracy[row,:]=cm.diagonal();
    row = row+1;
   
yerr_up =  accuracy.max(0)-accuracy.mean(0);
yerr_down = accuracy.mean(0)-accuracy.min(0);
ax.errorbar(x, accuracy.mean(0),yerr=[yerr_down, yerr_up], fmt='--o', label='Taylor - EVM', color=colors[0], capsize=15, markersize=6)
print accuracy;


#Plot Taylor - PMVS original
print "Taylor - PMVS original";
param_dir= main_dir + "/pmvs/original";

accuracy = np.zeros((len(trials),ncategories));
row=0;
for trial in trials:
  
    bof_dir=param_dir +"/bof_cross_validation/trial_"+str(trial);
    classification_dir=bof_dir +"/classification_" + str(num_means)
    cm_file=classification_dir + "/confussion_matrix.txt";
    #confusion matrix percent
    cm = np.genfromtxt(cm_file);  
    accuracy[row,:]=cm.diagonal();
    row = row+1;

   
yerr_up =  accuracy.max(0)-accuracy.mean(0);
yerr_down = accuracy.mean(0)-accuracy.min(0);
ax.errorbar(x, accuracy.mean(0),yerr=[yerr_down, yerr_up], fmt='--*', label='Taylor - PMVS [Furukawa and Ponce]', color=colors[2], capsize=18, markersize=8)
print accuracy;
print '----------'
print yerr_up;




#Plot Taylor - PMVS smoothing
print "Taylor - PMVS smoothing";
param_dir= main_dir + "/pmvs/gauss_1";

accuracy = np.zeros((len(trials),ncategories));

row=0;
for trial in trials:
  
    bof_dir=param_dir +"/bof_cross_validation/trial_"+str(trial);
    classification_dir=bof_dir +"/classification_" + str(num_means)
    cm_file=classification_dir + "/confussion_matrix.txt";
    #confusion matrix percent
    cm = np.genfromtxt(cm_file);  
    accuracy[row,:]=cm.diagonal();
    row = row+1;

   
yerr_up =  accuracy.max(0)-accuracy.mean(0);
yerr_down = accuracy.mean(0)-accuracy.min(0);
ax.errorbar(x, accuracy.mean(0),yerr=[yerr_down, yerr_up], fmt='--^', label='Taylor - PMVS+smoothing', color=colors[3], capsize=13,markersize=8)

print accuracy;
print '----------'
print yerr_up;

#Plot Taylor - Alpha
print "Taylor - Alpha";

param_dir= main_dir + "/taylor_alpha";
#param_dir= main_dir + "/beaudet_corners";

accuracy = np.zeros((len(trials),ncategories));
row=0;
for trial in trials:
  
    bof_dir=param_dir +"/bof_cross_validation/trial_"+str(trial);
    classification_dir=bof_dir +"/classification_" + str(num_means)
    cm_file=classification_dir + "/confussion_matrix.txt";
    #confusion matrix percent
    cm = np.genfromtxt(cm_file);  
    accuracy[row,:]=cm.diagonal();
    row=row + 1;
   
yerr_up =  accuracy.max(0)-accuracy.mean(0);
yerr_down = accuracy.mean(0)-accuracy.min(0);
ax.errorbar(x, accuracy.mean(0),yerr=[yerr_down, yerr_up], fmt='--v', label="Taylor - Occupancy", color=colors[1], capsize=15, markersize=8)

print accuracy;


ax.set_xlabel('Object Category',fontsize= 18);
ax.set_ylabel('Accuracy',fontsize= 18);  
ax.set_xticks(x)
classes= ['Plane', 'House', 'Building', 'Car', 'Parking Lot'];
ax.set_xticklabels(classes ,fontsize= 14)
ax.set_xlim( (-0.2,4.2) );
ax.set_ylim((0,1.01));

ylabels = np.arange(0,1.2,0.2);
ax.set_yticklabels(ylabels, fontsize= 14)
plt.legend(loc='lower center', frameon=False);  
plt.show();


#  plt.plot(x, accuracy, label=k_label[k-1]);
#  plt.xlabel('Percentage of samples used for recognition',fontsize= 'large');
#
#  plt.ylabel('Accuracy',fontsize= 'large');  
#  plt.hold(True);
#
#plt.legend(loc='lower right');  
#plt.show(); 
#plt.hold(False);
