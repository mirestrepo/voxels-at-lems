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

#  class_histograms_dir = "/Users/isa/Experiments/BOF/helicopter_providence/pmvs/original/bof_cross_validation/trial_6/class_histograms_20";
  class_histograms_dir = "/Users/isa/Experiments/BOF/helicopter_providence/taylor/bof_cross_validation/trial_6/class_histograms_20";
  #class_histograms_dir="/Users/isa/Experiments/BOF/helicopter_providence/pca_cross_validation/trial_6/bof/class_histograms_20";
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
  i=0;
  colors = ['r','b','cyan', 'g', 'yellow'];
  labels = ['Plane','House','Building', 'Car', 'Parking Lot'];
  width=0.15;
  
  fig = plt.figure()
  ax = fig.add_subplot(111)
  class_handle =np.zeros(5);
  x=np.arange(20);
  for file in hist_txt_files:

    full_path_file= all_scenes_path+ "/" + file;
    f = open(full_path_file, 'r');
    
    lines=[];
    lines = f.readlines();
    
#    x=[];
#    line0=lines[0]; 
#    this_line = line0.split(", ");
#    for j in this_line:
#        x.append(float(j) + width*i);
#    print x;
            
   
    y=[];
    line1 = lines[1];
    this_line = line1.split(", ");
    for j in this_line:
        y.append(float(j));
    
   
    #plt.figure(i);
    rects=ax.bar(x+width*i,y, width, color=colors[i], alpha=0.5, label=labels[i]);
    plt.hold(True);
    i=i+1;

    #plt.axis([0,len(x),0,1.0]); 
#  figure_file = all_scenes_path + "/all_classes_hist.pdf"
#  plt.savefig(figure_file, transparent=True);
#  f.close();
  
  print ("////////////////////////End Ploting Class Histograms/////////////////////////////")
  ax.set_xlabel('Volumetric word entry', fontsize= 18)
  ax.set_ylabel('$P(v_j | C_l)$', fontsize= 18)
  #ax.set_title('Distribution of volumetric vocabulary for all object categories',fontsize= 'large')  
  ax.set_xticklabels( x , fontsize=14)
  ax.set_xticks(x+0.37)
  
  y=np.arange(0,0.36,0.05);
  ax.set_yticklabels(y , fontsize=14)
  ax.set_yticks(y)
  
 
  #ax.legend( (rects, rects), ('Men', 'Women') )
  #ax.legend( ('label1', 'label2', 'label3','l4', 'l5') )
  plt.hold(False);
  handles, labels = ax.get_legend_handles_labels()
  ax.legend(handles, labels, 'upper right')
  leg = plt.gca().get_legend()
  ltext  = leg.get_texts()  # all the text.Text instance in the legend
  plt.setp(ltext, fontsize=18)    # the legend text fontsize
 
  plt.show();
  
  figure_file = all_scenes_path + "/all_classes_hist.pdf"
  plt.savefig(figure_file, transparent=True);
  f.close();