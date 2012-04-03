# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 14:38:46 2011
Plot pca training error as a function of percentage of samples used
@author: -
"""

# Computes the gaussian gradients on a boxm_alpha_scene

import os;
import optparse;
import time;
import sys;
import plot_pca_functions;
import numpy as np
import matplotlib.pyplot as plt
import math

if __name__=="__main__":


  #Parse inputs
#  parser = optparse.OptionParser(description='Compute PCA basis');
#
#  parser.add_option('--pca_dir', action="store", dest="pca_dir");
#  options, args = parser.parse_args();
#
#  pca_dir = options.pca_dir;
  
  pca_dir = '/Users/isa/Experiments/PCA/CapitolBOXM_6_4_4';
  print (pca_dir)

  if not os.path.isdir( pca_dir + '/'):
    sys.exit(-1);
  
  
  fig = plt.figure(10);

  
  for frac in range(1,6):
      
    this_pca_dir = pca_dir + '/' +str(int(frac*10));
    if not os.path.isdir( this_pca_dir + '/'):
        sys.exit(-1);
    
    error_file = this_pca_dir + "/normalized_training_error.txt";
    error= plot_pca_functions.read_vector(error_file);
    
    plt.title('Training Error ');
    x = np.arange(0, len(error), 1);
    y = plt.plot(x, error, label=(str(int(frac*10)) +'% of total samples'));
    plt.hold(True);
    
  plt.xlabel('Number of components used for reconstruction');
  plt.ylabel('Average error per feature vector');  
  a = plt.gca()
  a.set_xlim([1,125])
  plt.legend();  
  plt.show();  
 
