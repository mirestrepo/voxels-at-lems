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



if __name__=="__main__":


  #Parse inputs
  print ("******************************Ploting Class Histograms***************************")
  parser = optparse.OptionParser(description='Init Category info');

  parser.add_option('--classification_dir', action="store", dest="classification_dir");
  parser.add_option('--ncategories', action="store", dest="ncategories", type="int", default=0);

  options, args = parser.parse_args();

  classification_dir = options.classification_dir;
  ncategories = options.ncategories;
  
    
  if not os.path.isdir(classification_dir +"/"):
    print "Invalid classification Dir"
    sys.exit(-1);
    
 
  cfiles = []
  for root, dirs, files in os.walk(classification_dir):
    for file in files:
      print file
      if file=='classification.txt':
        cfiles.append(os.path.join(root, file))
  
  #confusion matrix percent
  cm = np.zeros((ncategories,ncategories));
  
  #confusion matrix int
  cm_int = np.zeros((ncategories,ncategories));
  
  #objects matrix
  om = np. zeros((ncategories,1));
  
  correct_class = 0;
  nobjects = 0;
  
  for file in cfiles:
    
    f = open(file, 'r');
    
    lines=[];
    lines = f.readlines();
    
    for line in lines:
      
      this_line = line.split(" ");
      j = int(this_line[0]);
      i = int(this_line[1])
      cm[i,j] = cm[i,j] + 1;
      cm_int[i,j] = cm_int[i,j] + 1;
      om[j] = om[j] + 1;
      nobjects = nobjects + 1;
      if (i==j):
        correct_class = correct_class + 1;
        
      
    
    f.close();
    
  print cm
  
  sums = np.sum(cm, axis=0);
  
  for i in range (0, ncategories):
    print sums[i]
    print cm[:, i]
    cm[:,i] = cm[:,i]/sums[i];
   
  print cm
  
  plt.imsave(classification_dir + "/confussion_matrix.png", cm ,  cmap=cmt.gray)
  
  cm_file = classification_dir + "/confussion_matrix.txt"
  np.savetxt(cm_file,cm);
  #f = open(cm_file, 'w');
  #f.write(str(cm));
  #f.close();
  
  cm_file = classification_dir + "/confussion_matrix_int.txt"
  #f = open(cm_file, 'w');
  #f.write(str(cm_int));
  #f.close();
  np.savetxt(cm_file,cm_int);

  
  om_file = classification_dir + "/classes_matrix.txt"
  #f = open(om_file, 'w');
  #f.write(str(om));
  #f.close();
  np.savetxt(om_file,om);

  accuracy_file = classification_dir + "/accuracy.txt"
  f = open(accuracy_file, 'w');
  f.write(str(correct_class));
  f.write("\n");
  f.write(str(nobjects));
  f.close();
      
    