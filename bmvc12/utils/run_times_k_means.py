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
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import glob
#FPFH_10 

ft="SpinImage"
#colors = ['magenta','blue','green', 'red', 'black'];
radius = 30;
K=500

fig=plt.figure()
ax = fig.add_subplot(111);
plt.hold(True);
plt.autoscale(tight=True);
plt.axis(tight=True);
x=(20,50, 100, 200, 500)


# FPFH
means_20 = [ 16.2249782085, 15.1312880516, 16.5236909389, 12.8444638252, 13.4461491108] 
means_50 = [ 23.8720850945, 21.8416278362, 24.3672001362, 22.4630770683, 23.5004911423] 
means_100 = [ 33.2164580822, 44.273982048, 43.1350309849, 41.4949531555, 36.129117012] 
means_200 = [ 94.8332238197, 85.2601461411, 87.7464978695, 66.1452999115, 71.3466069698] 
means_500 = [ 205.611297846, 289.443452835, 320.973904133, 259.297035933, 298.435438156] 
 
y = [np.average(means_20), np.average(means_50), np.average(means_100), np.average(means_200), np.average(means_500)];

yerr_up = [np.max(means_20) - np.average(means_20), np.max(means_50) - np.average(means_50), np.max(means_100) - np.average(means_100), np.max(means_200)-np.average(means_200), np.max(means_500)-np.average(means_500)];
yerr_down = [np.average(means_20) - np.min(means_20), np.average(means_50) - np.min(means_50), np.average(means_100) - np.min(means_100), np.average(means_200) - np.min(means_200), np.average(means_500) - np.min(means_500)];

ax.errorbar(x, y, yerr=[yerr_down, yerr_up], fmt='--o', label="FPFH", capsize=12)
#ax.plot(x, np.log(y), '^', label="Spin Image")


# SHOT
means_20 = [ 57.2709200382, 36.0257430077, 63.3647248745, 56.2832710743, 68.9899458885, ] 
means_50 = [ 82.6634149551, 86.1610281467, 82.089192152, 37.6616699696, 75.6602878571] 
means_100 = [ 98.4440200329, 104.054612875, 114.435255051, 42.9674088955, 101.036782026] 
means_200 = [ 131.788237095, 123.114695072, 159.383648157, 130.453483105, 174.793975115] 
means_500 = [ 435.135483027, 396.978031874, 417.469758034, 311.603000164, 287.949268103] 

y = [np.average(means_20), np.average(means_50), np.average(means_100), np.average(means_200), np.average(means_500)];

yerr_up = [np.max(means_20) - np.average(means_20), np.max(means_50) - np.average(means_50), np.max(means_100) - np.average(means_100), np.max(means_200)-np.average(means_200), np.max(means_500)-np.average(means_500)];
yerr_down = [np.average(means_20) - np.min(means_20), np.average(means_50) - np.min(means_50), np.average(means_100) - np.min(means_100), np.average(means_200) - np.min(means_200), np.average(means_500) - np.min(means_500)];

ax.errorbar(x, y, yerr=[yerr_down, yerr_up], fmt='--^', label="SHOT", capsize=12)

# SpinImage
means_20 = [ 36.712695837, 26.2004470825, 32.5318748951] 
means_50 = [ 49.3694200516, 41.7106099129, 45.076474905] 
means_100 = [ 71.0625460148, 76.2126779556, 61.7807269096] 
means_200 = [ 113.964242935, 93.8135280609, 123.387079954] 
means_500 = [ 315.586436987, 305.119965076, 330.27335]

y = [np.average(means_20), np.average(means_50), np.average(means_100), np.average(means_200), np.average(means_500)];

yerr_up = [np.max(means_20) - np.average(means_20), np.max(means_50) - np.average(means_50), np.max(means_100) - np.average(means_100), np.max(means_200)-np.average(means_200), np.max(means_500)-np.average(means_500)];
yerr_down = [np.average(means_20) - np.min(means_20), np.average(means_50) - np.min(means_50), np.average(means_100) - np.min(means_100), np.average(means_200) - np.min(means_200), np.average(means_500) - np.min(means_500)];

ax.errorbar(x, y, yerr=[yerr_down, yerr_up], fmt='--x', label="Spin Image", capsize=12)

# ShapeContext
means_20 = [ 322.923263073, 328.371750116, 176.858063936, 116.450598001] 
means_50 = [ 322.923263073, 328.371750116, 176.858063936, 116.450598001] 
means_100 = [ 322.923263073, 328.371750116, 176.858063936, 116.450598001] 
means_200 = [ 322.923263073, 328.371750116, 176.858063936, 116.450598001] 
means_500 = [ 322.923263073, 328.371750116, 176.858063936, 116.450598001] 

y = [np.average(means_20), np.average(means_50), np.average(means_100), np.average(means_200), np.average(means_500)];

yerr_up = [np.max(means_20) - np.average(means_20), np.max(means_50) - np.average(means_50), np.max(means_100) - np.average(means_100), np.max(means_200)-np.average(means_200), np.max(means_500)-np.average(means_500)];
yerr_down = [np.average(means_20) - np.min(means_20), np.average(means_50) - np.min(means_50), np.average(means_100) - np.min(means_100), np.average(means_200) - np.min(means_200), np.average(means_500) - np.min(means_500)];

ax.errorbar(x, y, yerr=[yerr_down, yerr_up], fmt='--*', label="Shape Context", capsize=12)

ax.set_xlabel('Number of Clusters', fontsize= 18);
ax.set_ylabel('Time (seconds)', fontsize= 18);  
#ax.set_xticks(x)
#ax.set_xticklabels(class_names ,fontsize= 14)
#ax.set_xlim( (-0.2,4.2) );
#ax.set_ylim((-4.5,9));

#ylabels = np.arange(0,1.2,0.2);
#ax.set_yticklabels(ylabels, fontsize= 14)
plt.legend(loc='upper left', frameon=True);  
plt.show();