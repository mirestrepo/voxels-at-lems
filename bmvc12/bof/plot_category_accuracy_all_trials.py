#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo

"""
import os
import sys

import os;
import optparse;
import time;
import sys;
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import glob


main_dir="/Users/isa/Experiments/BOF/helicopter_providence";


clf_name = "svm_gamma_10.0_C100.00"
#ft="FPFH"
#ft="SHOT"
ft="SpinImage"
#ft="ShapeContext"
colors = ['magenta','blue','green', 'red', 'black'];

fig=plt.figure()
ax = fig.add_subplot(111);
plt.hold(True);
plt.autoscale(tight=True);
plt.axis(tight=True);

means = (20, 50, 100, 200, 500);
markers = ['--o', '--s', '--v', '--^']
m=0;

for radius in (10, 20, 30, 45):
  
  feature_name = ft +'_'+ str(radius)
  acc_curve = [];
  yerr_up=[];
  yerr_down=[];
  
  for K in means:
      avg_classification_dir = "/Users/isa/Experiments/bof_bmvc12/average/" + feature_name   + "/percentile_90"
      avg_classification_dir = avg_classification_dir + "/classification_" + str(K);
      prf1s_file = avg_classification_dir +'/' + clf_name + "_prf1s.txt"
      recall_file = avg_classification_dir +'/' + clf_name + "_recall.txt"
      support_file = avg_classification_dir +'/' + clf_name + "_support.txt"

      fis = open(prf1s_file, 'r');
      prfs = np.genfromtxt(fis);
      fis.close();
      fis = open(recall_file, 'r');
      recall = np.genfromtxt(fis);
      fis.close();
      fis = open(support_file, 'r');
      support = np.genfromtxt(fis);
      fis.close();
      acc = np.average(prfs[:,1], weights=prfs[:,3]);
      acc_curve.append(acc)
      avg_recall = np.average(recall, axis=1, weights=support);
      print recall;
      print avg_recall;
      yerr_up.append(np.max(avg_recall) - acc);
      yerr_down.append(acc - np.min(avg_recall));

  ax.errorbar(means, acc_curve, yerr=[yerr_down, yerr_up], fmt=markers[m], label=feature_name, capsize=12, ms=10, linewidth=2, markeredgewidth=2)
  m=m+1;
#  ax.errorbar(x, harris_k3_k_means.mean(1), yerr=[yerr_down, yerr_up], fmt='--o', label=labels[3], color=colors[3], capsize=12);


ax.set_xlabel('Number of Clusters',fontsize= 20);
ax.set_ylabel('Recall',fontsize= 20);  
#classes= ['Plane', 'House', 'Building', 'Car', 'Parking Lot'];
ax.set_xlim((0,505) );
ax.set_ylim((0.0,1.0));

#ylabels = np.arange(0,1.2,0.2);
plt.setp(ax.get_yticklabels(), fontsize=18)
plt.setp(ax.get_xticklabels(), fontsize=18)

plt.legend(loc='lower center', frameon=False);  
plt.show();

