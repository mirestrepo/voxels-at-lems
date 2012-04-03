# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 15:03:28 2011

@author: -
"""
import matplotlib.pyplot as plt
import plot_pca_functions;

error_file1 = "/Users/isa/Experiments/PCA/CapitolBOXMSmall/10/weights.txt"
error_file2_un = "/Users/isa/Experiments/BOF/learn_PCA/tests/weights.txt"



error1 = plot_pca_functions.read_vector(error_file1);
error2 = plot_pca_functions.read_vector(error_file2_un);

plot_pca_functions.plot_error_per_sample(error1,56432)
plot_pca_functions.plot_error_per_sample(error2,169296)
