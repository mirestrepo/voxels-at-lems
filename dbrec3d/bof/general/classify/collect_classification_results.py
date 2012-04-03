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


#Parse inputs
print ("******************************Averaging Accuracy***************************")


#trials_dir = "/Users/isa/Experiments/BOF/helicopter_providence/taylor/bof_cross_validation";
#trials_dir = "/Users/isa/Experiments/BOF/helicopter_providence/corners/k_3/bof_cross_validation"
trials_dir = "/Users/isa/Experiments/BOF/helicopter_providence/beaudet_corners/bof_cross_validation";

#trials = [0,1,2,3,4,5,6,7,8,9];
trials = [0,1,2,3,4];

ncategories = 5;
classes= ['Plane', 'House', 'Building', 'Car', 'Parking'];
x = [0,1,2,3,4];

  
if not os.path.isdir(trials_dir +"/"):
  print "Invalid trials Dir"
  sys.exit(-1);

#confusion matrix percent
cm_avg = np.zeros((ncategories,ncategories));
cm_var = np.zeros((ncategories,ncategories));

accuracy = np.zeros((ncategories,len(trials)));

for t in trials:
    
    #cm_file=trials_dir +"/trial_" + str(t) + "/classification_20/confussion_matrix.txt";
    #cm_file=trials_dir +"/trial_" + str(t) + "/bof/classification_20/confussion_matrix.txt";
    cm_file=trials_dir +"/trial_" + str(t) + "/thresh_75/classification_20/confussion_matrix.txt";
    
    #confusion matrix percent
    cm = np.genfromtxt(cm_file);
         
    cm_avg = cm_avg + cm;
    cm_var = cm_var +  cm*cm;    
      
    accuracy[:,t] =cm.diagonal(); 
    plt.plot(x, cm.diagonal(), label=('Trial ' + str(t)));
    plt.xlabel('Object Category' ,fontsize= 'large');

    plt.ylabel('Accuracy',fontsize= 'large');  
    plt.hold(True);


plt.legend(loc='lower right');  
plt.show(); 
plt.hold(False);
         
cm_avg = cm_avg/len(trials);
cm_var = cm_var/len(trials) - cm_avg*cm_avg;
 
np.set_printoptions(precision=4)
print cm_avg
np.set_printoptions(precision=4)
print cm_var
print 'Accuracy'
print accuracy;
np.set_printoptions(precision=4)
print np.mean(accuracy,0);
np.set_printoptions(precision=4)
print np.mean(accuracy);
np.set_printoptions(precision=4)
print np.std(accuracy);

plt.imsave(trials_dir + "/avg_confussion_matrix.png", cm_avg ,  cmap=cmt.gray)
plt.imsave(trials_dir + "/var_confussion_matrix.png", cm_var ,  cmap=cmt.gray)


cm_file = trials_dir + "/avg_confussion_matrix.txt"
np.savetxt(cm_file, cm_avg);

cm_file = trials_dir + "/var_confussion_matrix.txt"
np.savetxt(cm_file, cm_var); 
cm_file = trials_dir + "/std_confussion_matrix.txt"
np.savetxt(cm_file, np.sqrt(cm_var));