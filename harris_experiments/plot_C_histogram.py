# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 14:38:46 2011
Plot pca test error vs train error
@author: Isabel Restrepo
"""


import os;
import optparse;
import time;
import sys;
import numpy as np
import matplotlib.pyplot as plt
import glob



if __name__=="__main__":


  full_path_file= '/Users/isa/Experiments/BOF/helicopter_providence/harris_test/aux_dirs/site22/bsta_hist_plot.txt';
  f = open(full_path_file, 'r');
  
  lines=[];
  lines = f.readlines();
  
  x=[];
  line0=lines[0]; 
  this_line = line0.split(", ");
  for j in this_line:
      x.append(float(j));
          
 
  y=[];
  line1 = lines[1];
  this_line = line1.split(", ");
  for j in this_line:
      y.append(float(j));
  
 
  plt.figure();
  plt.bar(x,y, (x[len(x)-1] - x[0])/100);
  #plt.xlim([x[0],x[len(x)-1]]); 
  figure_file = full_path_file.split('.')[0]
  figure_file = figure_file + '.pdf';
  plt.savefig(figure_file, transparent=True);
  f.close();
  
  print ("////////////////////////End Ploting Class Histograms/////////////////////////////")
