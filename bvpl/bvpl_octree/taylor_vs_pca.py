# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 16:41:25 2011

@author: -
"""

import os;
import time;
import sys;
import plot_pca_functions;
import numpy as np
import matplotlib.pyplot as plt
import math

taylor_error_capitol= 0.608546356589;
pca_error_9_capitol = 0.614236131016;  #at 10% sample-training

taylor_error_downtown= 0.248427497809; #this is for downtown12_12_4!
pca_error_9_downtown = 0.193806624247; #this is for downtown3_3_1!

fig = plt.figure();
