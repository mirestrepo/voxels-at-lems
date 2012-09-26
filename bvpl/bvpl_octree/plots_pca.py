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

weights_10_file = "/Users/isa/Experiments/PCA/DowntownBOXM_3_3_1/10/weights.txt";


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

def plot_weights(w);
    x = np.arange(0, len(w), 1);
    weight_fig = plt.figure(1);
    plt.title('PCA Weights');
    
    y = plt.plot(x, w);
    plt.legend( ( y),
            ('weights 10%'),
            'upper right')
    plt.show();

def plot_cum_var(w)
    cum_sum=[];
    cum_sum = cum_error(w);
    var_fig = plt.figure(2);
    plt.title('Cumulative Variance');
    y = plt.plot(x, cum_sum);
    plt.legend( ( y),
            ('Variance 10%'),
            'upper right')
    plt.show();

def plot_error(w)
    training_error_=[];
    training_error = reconstruction_error(w);
    fig = plt.figure(3);
    plt.title('Training Error');
    y = plt.plot(x, training_error);
    plt.legend( ( y),
            ('Error 10%'),
            'upper right')
    plt.show();
#
#weights_10_file = "/Users/isa/Experiments/PCA/CapitolBOXM_1_1_1/10/weights.txt";
#weights_20_file = "/Users/isa/Experiments/PCA/CapitolBOXM_1_1_1/20/weights.txt"



weights_10_file = "/Users/isa/Experiments/PCA/DowntownBOXM_3_3_1/10/weights.txt";
weights_20_file = "/Users/isa/Experiments/PCA/DowntownBOXM_3_3_1/20/weights.txt";

f_10 = open(weights_10_file, 'r');
f_20 = open(weights_20_file, 'r');

w_10=[];

lines = f_10.readlines();
for i in lines:
    this_line = i.split(" ");
#    print (this_line)
#    print len(this_line)
    for j in this_line:
        w_10.append(float(j));
#        print j

w_20=[];

lines = f_20.readlines();
for i in lines:
    this_line = i.split(" ");
#    print (this_line)
#    print len(this_line)
    for j in this_line:
        w_20.append(float(j));
#        print j

x = np.arange(0, len(w_10), 1);
weight_fig = plt.figure(1);
plt.title('PCA Weights');

y_10 = plt.plot(x, w_10);
y_20 = plt.plot(x, w_20);
plt.legend( ( y_10, y_20),
        ('weights 10%', 'weights 20%'),
        'upper right')
plt.show();

#Calculate and plot cumulative variance
cum_sum_10=[];
cum_sum_10 = cum_error(w_10);
cum_sum_20=[];
cum_sum_20 = cum_error(w_20);
var_fig = plt.figure(2);
plt.title('Cumulative Variance');
y_10 = plt.plot(x, cum_sum_10);
y_20 = plt.plot(x, cum_sum_20);
plt.legend( ( y_10, y_20),
        ('Variance 10%', 'Variance 20%'),
        'upper right')
plt.show();

#Read test error
test_error_10_file = "/Users/isa/Experiments/PCA/CapitolBOXM_1_1_1/10/test_error.txt";
fte_10 = open(test_error_10_file, 'r');

t_error_10=[];

lines = fte_10.readlines();
for i in lines:
    this_line = i.split(" ");
    for j in this_line:
        t_error_10.append(float(j));

#Calculate and plot theoretical training error
training_error_10=[];
training_error_10 = reconstruction_error(w_10);
training_error_20=[];
training_error_20= reconstruction_error(w_20);
fig = plt.figure(3);
plt.title('Training Error');
y_10 = plt.plot(x, training_error_10);
y_20 = plt.plot(x, np.array(training_error_20)/2);
y_test_10 = plt.plot(x, np.array(t_error_10)/9.5);
plt.legend( ( y_10, y_20, y_test_10),
        ('Error 10%', 'Error 20%', 'Test Error 10%'),
        'upper right')
plt.show();



