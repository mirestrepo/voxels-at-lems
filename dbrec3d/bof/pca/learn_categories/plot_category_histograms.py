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



if __name__=="__main__":


  #Parse inputs
  print ("******************************Ploting Class Histograms***************************")
  parser = optparse.OptionParser(description='Init Category info');

  parser.add_option('--bof_dir', action="store", dest="bof_dir");
  parser.add_option('--class_histograms_dir', action="store", dest="class_histograms_dir");

  options, args = parser.parse_args();

  bof_dir = options.bof_dir;
  class_histograms_dir = options.class_histograms_dir;
  
  if not os.path.isdir(bof_dir +"/"):
    print "Invalid bof Dir"
    sys.exit(-1);
    
  if not os.path.isdir(class_histograms_dir +"/"):
    print "Invalid histogram Dir"
    sys.exit(-1);
    
  all_scenes_path = class_histograms_dir + "/all_scenes"  
  if not os.path.isdir(all_scenes_path +"/"):
    print "Invalid All scenes path"
    sys.exit(-1);
  
  hist_txt_files = glob.glob1(all_scenes_path, '*hist_plot.txt');
  nclasses = len(hist_txt_files);
  print ("Ploting " +str(nclasses) + " files");
  
#  plt.figure(1); #don't flush old display
#  plt.figure(2);
  i=1;
  for file in hist_txt_files:

    full_path_file= all_scenes_path+ "/" + file;
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
    
   
    plt.figure(i);
    i=i+1;
    plt.bar(x,y);
    plt.axis([0,len(x),0,0.2]); 
    figure_file = full_path_file.split('.')[0]
    figure_file = figure_file + '.pdf';
    plt.savefig(figure_file, transparent=True);
    f.close();
  
  print ("////////////////////////End Ploting Class Histograms/////////////////////////////")

