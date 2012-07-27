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
#matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import glob


main_dir="/Users/isa/Experiments/BOF/helicopter_providence";

clf_name = "svm_gamma_10.0_C100.00"
#ft="FPFH"
#ft="SHOT"
ft="SpinImage"
#ft="ShapeContext"
#colors = ['magenta','blue','green', 'red', 'black'];
radius = 30;
K=500

fig=plt.figure()
ax = fig.add_subplot(111);
plt.hold(True);
plt.autoscale(tight=True);
plt.axis(tight=True);

  
feature_name = ft +'_'+ str(radius)
acc_curve = [];
yerr_up=[];
yerr_down=[];
labels =  ["Nearest Neighbor", "Naive Bayes", "SVM" ]; 
markers = ['--o', '--s', '--v']
x=np.arange(0,5);

l=0
for clf_name in ("1nn", "bayes", "svm_gamma_10.0_C100.00" ):
  
    avg_classification_dir = "/Users/isa/Experiments/bof_bmvc12/average/" + feature_name   + "/percentile_90"
    avg_classification_dir = avg_classification_dir + "/classification_" + str(K);
    prf1s_file = avg_classification_dir +'/' + clf_name + "_prf1s.txt"
    recall_file = avg_classification_dir +'/' + clf_name + "_recall.txt"
    support_file = avg_classification_dir +'/' + clf_name + "_support.txt"

    fis = open(recall_file, 'r');
    recall = np.genfromtxt(fis);
    fis.close();
    fis = open(support_file, 'r');
    support = np.genfromtxt(fis);
    fis.close();
    avg_recall = np.average(recall, axis=0, weights=support);
    print recall;
    print avg_recall;
    yerr_up = np.max(recall, axis =0) - avg_recall;
    yerr_down = avg_recall - np.min(recall, axis =0);

    ax.errorbar(x, avg_recall, yerr=[yerr_down, yerr_up], fmt=markers[l], ms=10, linewidth=2, label=labels[l], capsize=12, markeredgewidth=2)
    l=l+1;
#  ax.errorbar(x, harris_k3_k_means.mean(1), yerr=[yerr_down, yerr_up], fmt='--o', label=labels[3], color=colors[3], capsize=12);


ax.set_xlabel('Object Category', fontsize= 20);
ax.set_ylabel('Recall', fontsize= 20);  
class_names = ["Plane", "Car", "House", "Buildings", "Parking"];
ax.set_xticks(x)
ax.set_xticklabels(class_names ,fontsize= 18)
ax.set_xlim( (-0.2,4.2) );
ax.set_ylim((0.0,1.02));
plt.setp(ax.get_yticklabels(), fontsize=18)
plt.setp(ax.get_xticklabels(), fontsize=18)

#ylabels = np.arange(0,1.2,0.2);
#ax.set_yticklabels(ylabels, fontsize= 14)
plt.legend(loc='lower center', frameon=False);  
plt.show();
