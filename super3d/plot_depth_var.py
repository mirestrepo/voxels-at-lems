import os;
import optparse;
import time;
import sys;
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cmt
import glob


dirs = [];


dirs.append("/Users/isa/Experiments/super3d/sr2_3scene_sr2_images"); 
dirs.append("/Users/isa/Experiments/super3d/scene_sr2_images"); 
dirs.append("/Users/isa/Experiments/super3d/scene"); 

labels = ['Scene 3' , 'Scene 2', 'Scene 1'];

for dir_idx in range(0,len(dirs)):
    dir = dirs[dir_idx];
    mean_var_curve = [];
    for idx in range (0,3):
    
        expected_dir = dir + "/expectedImgs_" + str(idx);
        ssd_file = expected_dir + "/mean_var.txt"
        f = open(ssd_file, 'r');
        
        lines=[];
        lines = f.readlines();
  
        print lines
        
        mean_var_val = float(lines[0])
        print str(mean_var_val);
  
        mean_var_curve.append(mean_var_val);
        f.close();
        
    x = [28, 56, 84];
   
    plt.plot(x, mean_var_curve, label=labels[dir_idx]);
    plt.xlabel('Number of images used for modeling (only 28 distinct)',fontsize= 'large');

    plt.ylabel('Mean Depth Variance per Pixel',fontsize= 'large');  
    plt.hold(True);
      
plt.legend(loc='lower right');  
plt.show(); 
plt.hold(False);
