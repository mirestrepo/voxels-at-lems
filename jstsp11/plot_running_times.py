# -*- coding: utf-8 -*-
"""
Created on April 11, 2012
@author: Isabel Restrepo
"""

# Computes the gaussian gradients on a boxm_alpha_scene

import os;
import optparse;
import time;
import sys;
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import glob

#plot k_means running times




x=[1,5,10,20,50, 75, 90];
labels = ['DoH','Harris $(\kappa=0.01)$' , 'Harris $(\kappa=0.0075)$', 'Harris $(\kappa=0.005)$'];
colors = ['red', 'magenta','blue','green'];



fig=plt.figure(0)
ax = fig.add_subplot(111);
plt.hold(True);
plt.autoscale(tight=False);
plt.axis(tight=False);

hessian_k_means = np.array([[369, 295, 314, 336, 382], [459, 349, 440, 584, 520], [708, 383, 561, 619, 653], [853, 580, 855, 662, 112], [895, 1115, 1101, 1950, 1216], [1792, 1779, 2073, 3128, 2811], [2054, 2217, 2687, 3934, 3319]]);
yerr_up=hessian_k_means.max(1) - hessian_k_means.mean(1);
yerr_down=hessian_k_means.mean(1) - hessian_k_means.min(1);
ax.errorbar(x, hessian_k_means.mean(1), yerr=[yerr_down, yerr_up], fmt='--o', label=labels[0], color=colors[0], capsize=12);

harris_k1_k_means=np.array([[644,621,525,641,618],[785,586,668,737,700],[1182,645,672,1073,1382] ,[2029,976,1285,1456,1144],[2584,1278,2182,2355,1873],[4623,2561,3076,4083,2596],[4467,3062,3898,5350,5096]]);
yerr_up=harris_k1_k_means.max(1) - harris_k1_k_means.mean(1);
yerr_down=harris_k1_k_means.mean(1) - harris_k1_k_means.min(1);
ax.errorbar(x, harris_k1_k_means.mean(1), yerr=[yerr_down, yerr_up], fmt='--s', label=labels[1], color=colors[1], capsize=12);

harris_k2_k_means=np.array([[1073,344,311,337,363],[1160,381,376,446,494],[1120,440,453,588,468],[1467,490,599,830,828],[2209,779,986,1546,1581],[3296,1257,1958,2871,2971],[3362,2130,2500,2966,3611]]);
yerr_up=harris_k2_k_means.max(1) - harris_k2_k_means.mean(1);
yerr_down=harris_k2_k_means.mean(1) - harris_k2_k_means.min(1);
ax.errorbar(x, harris_k2_k_means.mean(1), yerr=[yerr_down, yerr_up], fmt='--^', label=labels[2], color=colors[2], capsize=12);


harris_k3_k_means=np.array([[1054,544,572,644,550],[1162,638,611,784,651],[1173,762,833,806,880],[1466,805,687,883,825],[2643,1551,2007,1735,1566],[4546,1647,2617,2312,3693],[6650,3042,3634,5909,4813]]);

yerr_up=harris_k3_k_means.max(1) - harris_k3_k_means.mean(1);
yerr_down=harris_k3_k_means.mean(1) - harris_k3_k_means.min(1);
ax.errorbar(x, harris_k3_k_means.mean(1), yerr=[yerr_down, yerr_up], fmt='--v', label=labels[3], color=colors[3], capsize=12);

#Set up figure
ax.set_xlabel('Percentage of salient features    ',fontsize= 18);
ax.set_ylabel('Running time (seconds)',fontsize= 18);  
xticks=np.arange(0,100,10);#[1,5,10,20,50,75,90];
ax.set_xticklabels(xticks, fontsize= 14);
ax.set_xticks(xticks)
ax.set_xlim((0, 100));


[b,t]=ax.get_ylim();
ax.set_ylim((b-100, t+100));
plt.setp(ax.get_yticklabels(), fontsize=14)
#ax.set_yticklabels(, fontsize= 14)

plt.legend(loc='upper center', frameon=False);  
########################################Learn categories#####################################################################

fig=plt.figure(1)
ax = fig.add_subplot(111);
plt.hold(True);
plt.autoscale(tight=False);
plt.axis(tight=False);
hessian_codebook= np.array([[587,352,414,446,489],[422,356,415,431,573],[446,356,401,438,481],[439,352,415,437,469],[440,346,409,439,465],[434,348,412,451,478],[445,364,419,453,483]])
yerr_up=hessian_codebook.max(1) - hessian_codebook.mean(1);
yerr_down=hessian_codebook.mean(1) - hessian_codebook.min(1);
ax.errorbar(x, hessian_codebook.mean(1), yerr=[yerr_down, yerr_up], fmt='--o', label=labels[0], color=colors[0], capsize=12);


harris_k1_codebook=np.array([[730,335,379,388,413],[512,335,380,396,412],[581,335,379,282,412],[735,336,421,261,406],[114,337,396,621,408],[973,245,563,406,405],[1007,339,387,408,412]]);
yerr_up=harris_k1_codebook.max(1) - harris_k1_codebook.mean(1);
yerr_down=harris_k1_codebook.mean(1) - harris_k1_codebook.min(1);
ax.errorbar(x, harris_k1_codebook.mean(1), yerr=[yerr_down, yerr_up], fmt='--s', label=labels[1], color=colors[1], capsize=12);

harris_k2_codebook = np.array([[528,453,398,427,441],[495,397,410,436,460],[567,421,406,434,459],[638,429,402,428,474],[502,359,404,434,466],[520,359,401,449,463],[836,364,419,458,473]]);
yerr_up=harris_k2_codebook.max(1) - harris_k2_codebook.mean(1);
yerr_down=harris_k2_codebook.mean(1) - harris_k2_codebook.min(1);
ax.errorbar(x, harris_k2_codebook.mean(1), yerr=[yerr_down, yerr_up], fmt='--^', label=labels[2], color=colors[2], capsize=12);

harris_k3_codebook = np.array([[636,335,386,393,379],[531,335,381,390,380],[460,337,384,389,380],[473,334,378,390,381],[664,338,386,390,386],[1203,337,385,392,388],[610,339,388,555,383]]);
yerr_up=harris_k3_codebook.max(1) - harris_k3_codebook.mean(1);
yerr_down=harris_k3_codebook.mean(1) - harris_k3_codebook.min(1);
ax.errorbar(x, harris_k3_codebook.mean(1), yerr=[yerr_down, yerr_up], fmt='--v', label=labels[3], color=colors[3], capsize=12);

#Set up figure
ax.set_xlabel('Percentage of salient features    ',fontsize= 18);
ax.set_ylabel('Running time (seconds)',fontsize= 18);  
xticks=np.arange(0,100,10);#[1,5,10,20,50,75,90];
ax.set_xticklabels(xticks, fontsize= 14);
ax.set_xticks(xticks)
ax.set_xlim((0, 100));


[b,t]=ax.get_ylim();
ax.set_ylim((100, 1300));
plt.setp(ax.get_yticklabels(), fontsize=14)
#ax.set_yticklabels(, fontsize= 14)

plt.legend(loc='upper center', frameon=False);  


########################################Classify#####################################################################


fig=plt.figure(2)
ax = fig.add_subplot(111);
plt.hold(True);
plt.autoscale(tight=False);
plt.axis(tight=False);
hessian_classify=np.array([[387,424,370,346,394],[373,426,373,350,359],[387,431,369,347,354],[369,428,367,356,366],[376,428,368,357,357],[380,421,373,353,358],[376,421,369,352,353]]);
yerr_up=hessian_classify.max(1) - hessian_classify.mean(1);
yerr_down=hessian_classify.mean(1) - hessian_classify.min(1);
ax.errorbar(x, hessian_classify.mean(1), yerr=[yerr_down, yerr_up], fmt='--o', label=labels[0], color=colors[0], capsize=12);

harris_k1_classify=np.array([[386,386,514,484,542],[346,346,522,669,532],[346,358,543,473,562],[342,342,586,666,511],[352,352,523,553,525],[659,529,523,620,530],[569,565,514,497,504]]);
yerr_up=harris_k1_classify.max(1) - harris_k1_classify.mean(1);
yerr_down=harris_k1_classify.mean(1) - harris_k1_classify.min(1);
ax.errorbar(x, harris_k1_classify.mean(1), yerr=[yerr_down, yerr_up], fmt='--s', label=labels[1], color=colors[1], capsize=12);


harris_k2_classify=np.array([[395,729,369,347,351],[416,483,369,351,352],[418,487,372,354,352],[440,503,363,357,361],[441,429,370,358,357],[432,419,362,355,350],[460,412,364,347,359]]);
yerr_up=harris_k2_classify.max(1) - harris_k2_classify.mean(1);
yerr_down=harris_k2_classify.mean(1) - harris_k2_classify.min(1);
ax.errorbar(x, harris_k2_classify.mean(1), yerr=[yerr_down, yerr_up], fmt='--^', label=labels[2], color=colors[2], capsize=12);


harris_k3_classify=np.array([[443,546,528,503,513],[414,569,491,481,520],[412,596,524,487,505],[427,568,516,485,530],[457,574,503,475,527],[653,565,519,532,533],[325,584,521,529,504]]);
yerr_up=harris_k3_classify.max(1) - harris_k3_classify.mean(1);
yerr_down=harris_k3_classify.mean(1) - harris_k3_classify.min(1);
ax.errorbar(x, harris_k3_classify.mean(1), yerr=[yerr_down, yerr_up], fmt='--v', label=labels[3], color=colors[3], capsize=12);

#Set up figure
ax.set_xlabel('Percentage of salient features    ',fontsize= 18);
ax.set_ylabel('Running time (seconds)',fontsize= 18);  
xticks=np.arange(0,100,10);#[1,5,10,20,50,75,90];
ax.set_xticklabels(xticks, fontsize= 14);
ax.set_xticks(xticks)
ax.set_xlim((0, 100));


[b,t]=ax.get_ylim();
ax.set_ylim((100, 1300));
plt.setp(ax.get_yticklabels(), fontsize=14)
#ax.set_yticklabels(, fontsize= 14)

#handles, labels = ax.get_legend_handles_labels()
#ax.legend(handles, labels,'upper left')
plt.legend(loc='upper center', frameon=False);  

plt.show();
