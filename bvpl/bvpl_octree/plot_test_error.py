# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 14:38:46 2011
Plot pca test error as a function of components used for capitol and downtown
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
  
  dirs=[];
  dirs.append('/Users/isa/Experiments/PCA/site22/10');
  dirs.append('/Users/isa/Experiments/PCA/site22/20');
  dirs.append('/Users/isa/Experiments/PCA/site22/50');
  dirs.append('/Users/isa/Experiments/PCA/site22/80');
  dirs.append('/Users/isa/Experiments/PCA/site22/100');
  labels=[];
  labels.append('10% of samples');
  labels.append('20% of samples');
  labels.append('50% of samples');
  labels.append('80% of samples');
  labels.append('100% of samples');
  dim=125;
  i= 0;
  
  fig = plt.figure(1);
  
  for pca_dir in dirs:
      
    print (pca_dir)
    
    if not os.path.isdir( pca_dir + '/'):
        sys.exit(-1);
      
    error = plot_pca_functions.read_test_error(pca_dir, dim);
      
    plt.title('Error over entire scene ',fontsize= 14);
    x = np.arange(0, (len(error)*5), 5);
    y = plt.plot(x, error, label=labels[i]);
    plt.hold(True);
    
    i=i+1;
         
  plt.xlabel('Number of components used for reconstruction',fontsize= 14);
  plt.ylabel('Average error per featurevector',fontsize= 14);  
  plt.legend();  
  plt.show();  
 
