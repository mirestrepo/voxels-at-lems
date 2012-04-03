# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 11:10:18 2011

@author:Isabel Restrepo

Sets of functions to plot statictics about principal components
"""
import numpy as np
import matplotlib.pyplot as plt
import math

def cum_error(w_list):
    sum = 0;
    cum_sum=[];
    total_sum = math.fsum(w_list);
    for i in range(0, len(w_list), 1):
        sum = sum + w_list[i];
        cum_sum.append(sum/total_sum);

    return cum_sum;


#//computes theoretical reconstruction error
def reconstruction_error(weights):

    error= [];

    for i in range(0, len(weights), 1):
        error.append(sum(weights[i+1:len(weights)]));


    return error;


def read_weights(weights_file):
    f = open(weights_file, 'r');
    
    w =[];
    
    lines = f.readlines();
    for i in lines:
        this_line = i.split(" ");
    #    print (this_line)
    #    print len(this_line)
        for j in this_line:
            w.append(float(j));
    #        print j
    return w
    
def read_vector(vector_file):
    f = open(vector_file, 'r');
    
    w =[];
    
    lines = f.readlines();
    for i in lines:
        this_line = i.split(" ");
    #    print (this_line)
    #    print len(this_line)
        for j in this_line:
            w.append(float(j));
    #        print j
    return w

def plot_weights(w):
    weight_fig = plt.figure(1);
    plt.title('PCA Weights');
    x = np.arange(0, len(w), 1);
    y = plt.plot(x, w);
    plt.legend( (y),
            ('weights 10%'),
            'upper right')
    plt.show();

def plot_cum_var(w):
    cum_sum=[];
    cum_sum = cum_error(w);
    var_fig = plt.figure(2);
    plt.title('Cumulative Variance');
    x = np.arange(0, len(w), 1);
    y = plt.plot(x, cum_sum);
    plt.legend( ( y),
            ('Variance 10%'),
            'upper right')
    plt.show();

def plot_error(w):
    training_error_=[];
    training_error = reconstruction_error(w);
    fig = plt.figure(3);
    plt.title('Training Error');
    x = np.arange(0, len(w), 1);
    y = plt.plot(x, training_error);
    plt.legend( ( y),
            ('Error 10%'),
            'upper right')
    plt.show();
    
def plot_error_per_sample(w, nsamples):
    training_error_=[];
    training_error = reconstruction_error(w);
    fig = plt.figure(4);
    plt.title('Training Error per Sample');
    x = np.arange(0, len(w), 1);
    y = plt.plot(x, np.array(training_error)/nsamples);
    plt.legend( ( y),
            ('Error 10%'),
            'upper right')
    plt.show();
    

def plot_results(weights_file, nsamples):
    w = [];
    w = read_weights(weights_file);
    plot_weights(w);
    plot_cum_var(w);
    plot_error(w);
    plot_error_per_sample(w,nsamples);

def read_test_error(pca_dir, dim):
    error=[];
    for i in range(0,dim+1,5):
        error_file = pca_dir + "/error_" + str(i) +"/error.txt";
        
        #read the first line of the fi
        f = open(error_file, 'r');     
        e = float(f.readline());
        #print e;
        if (e>50):
            e=0.0;
        error.append(e);
        
    return error
        
def plot_error(e):
    e_fig = plt.figure(1);
    plt.title('Reconstruction Error');
    x = np.arange(0, len(e), 1);
    y = plt.plot(x, e);
    plt.legend( (y),
            ('Error'),
            'upper left')
    plt.show();


if __name__=="__main__":
    weights_file = "/Users/isa/Experiments/PCA/DowntownBOXM_3_3_1/10/weights.txt";
    
    
    #weights_file = "/Users/isa/Experiments/PCA/CapitolBOXMSmall/10/weights.txt";
    
    #nsamples = 3492300;
    #plot_results(weights_file,nsamples);
    
    pca_dir = "/Users/isa/Experiments/PCA/CapitolBOXM_6_4_4/10";
    errors = read_test_error(pca_dir, 125);
    plot_error(errors);
