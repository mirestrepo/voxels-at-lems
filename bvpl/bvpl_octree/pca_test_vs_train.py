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
  #dirs.append('/Users/isa/Experiments/PCA/CapitolBOXM_6_4_4/10');
  #dirs.append('/Users/isa/Experiments/PCA/DowntownBOXM_3_3_1/10');
  labels=[];
  #labels.append('Capitol Train');
  #labels.append('Capitol Overall');
  labels.append('Downtown Training Error');
  labels.append('Downtown Overall Error');
  dim=125;
  i= 0;
  
  fig = plt.figure(1);
  for pca_dir in dirs:
      
    print (pca_dir)
    
    if not os.path.isdir( pca_dir + '/'):
        sys.exit(-1);
      
    train_error_file =  pca_dir + "/normalized_training_error.txt";

    overall_error = plot_pca_functions.read_test_error(pca_dir, dim);
    train_error =  plot_pca_functions.read_vector(train_error_file);
    
    print(train_error);
    print(overall_error);

    x = np.arange(0, len(train_error), 1);
    plt.plot(x, train_error, label=labels[i]);
    plt.hold(True);
    x = np.arange(0, len(train_error)+1, 5);
    plt.plot(x, overall_error, label=labels[i+1]);

    
    i=i+2;

  plt.title('Overall error vs training error ',fontsize= 14);
       
  plt.xlabel('Number of components used for reconstruction', fontsize= 14);
  a = plt.gca()
  a.set_xlim([0,125])
  plt.ylabel('Average error per feature vector',fontsize= 14); 
  plt.legend();  
  plt.show();  
 
