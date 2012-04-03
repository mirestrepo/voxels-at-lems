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
import glob


main_dir="/Users/isa/Experiments/BOF/helicopter_providence";

nobjects = 120;

thresh = [1, 5, 10, 20, 50, 75, 90];
trials = [0,1,2,3,4];

num_means=20;

k_label = ['Harris $(\kappa=0.01)$' , 'Harris $(\kappa=0.0075)$', 'Harris $(\kappa=0.005)$'];
colors = ['magenta','blue','green'];

fig=plt.figure()
ax = fig.add_subplot(111)
plt.autoscale(tight=False);

for k in range(1,4):
  param_dir= main_dir + "/corners/k_" + str(k);
  #param_dir= main_dir + "/beaudet_corners";
  
  accuracy = np.zeros((len(trials),len(thresh)));
  row=0;
  for trial in trials:
      col=0;
      for t in thresh: 
    
        bof_dir=param_dir +"/bof_cross_validation/trial_"+str(trial) + "/thresh_" + str(t);
        classification_dir=bof_dir +"/classification_" + str(num_means)
        accuracy_file = classification_dir + "/accuracy.txt"
    
        f = open(accuracy_file, 'r');
          
        lines=[];
        lines = f.readlines();
        
        #print lines
        #print str(int(lines[0]))
          
        accuracy[row,col]=(float(lines[0])/ float(lines[1]));
        col=col+1;
    
      row=row+1;
    
     
  yerr_up =  accuracy.max(0)-accuracy.mean(0);
  yerr_down = accuracy.mean(0)-accuracy.min(0);
  ax.errorbar(thresh, accuracy.mean(0),yerr=[yerr_down, yerr_up], fmt='--o', label=k_label[k-1], color=colors[k-1], capsize=12)
  plt.hold(True);

#Plot det(Hessian)

param_dir= main_dir + "/beaudet_corners";
accuracy = np.zeros((len(trials),len(thresh)));
row=0;
for trial in trials:
  col=0;
  for t in thresh: 

    bof_dir=param_dir +"/bof_cross_validation/trial_"+str(trial) + "/thresh_" + str(t);
    classification_dir=bof_dir +"/classification_" + str(num_means)
    accuracy_file = classification_dir + "/accuracy.txt"

    f = open(accuracy_file, 'r');
      
    lines=[];
    lines = f.readlines();
    
    #print lines
    #print str(int(lines[0]))
      
    accuracy[row,col]=(float(lines[0])/ float(lines[1]));
    col=col+1;

  row=row+1;

 
yerr_up =  accuracy.max(0)-accuracy.mean(0);
yerr_down = accuracy.mean(0)-accuracy.min(0);
ax.errorbar(thresh, accuracy.mean(0),yerr=[yerr_down, yerr_up], fmt='--o', label='DoH', color='r', capsize=12)



ax.set_xlabel('Percentage of salient features    ',fontsize= 18);
ax.set_ylabel('Accuracy',fontsize= 18);  
x=np.arange(0,101,10);#[1,5,10,20,50,75,90];
ax.set_xticklabels(x, fontsize= 14);
ax.set_xticks(x)

ax.set_ylim((0,1.01));
ylabels = np.arange(0,1.2,0.2);
ax.set_yticklabels(ylabels, fontsize= 14)

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels,'lower right')
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
