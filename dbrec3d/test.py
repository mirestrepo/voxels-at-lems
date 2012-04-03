#!/usr/bin/python

#from generate_directions import dirs
#from math import pi
#
#d = dirs(pi,pi);
#
##print(d);
#
#filename = "dirs.txt"
#
#FILE = open(filename, "w");
#
#import pprint
#
#pp= pprint.PrettyPrinter(stream=FILE);
#
#pp.pprint(d);
#
#for i in range(len(d)):
#  print(i);


import dbrec3d_batch;
import os;
dbrec3d_batch.register_processes();
dbrec3d_batch.register_datatypes();

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string


min_x = -15;
max_x = 15;
min_y = -30;
max_y = 30;
min_z = -15;
max_z = 15;

axes_x=[-1.0,0.0,0.0];
axes_y=[0.0,-1.0,0.0];
axes_z=[0.0,0.0,-1.0];

angle =  0.0;


axis_x = axes_x[0];
axis_y = axes_y[0];
axis_z = axes_z[0];

print("Creating 3D edge kernel");
dbrec3d_batch.init_process("bvplCreateEdge3dKernelProcess");
dbrec3d_batch.set_input_int(0,min_x);
dbrec3d_batch.set_input_int(1,max_x);
dbrec3d_batch.set_input_int(2,min_y);
dbrec3d_batch.set_input_int(3,max_y);
dbrec3d_batch.set_input_int(4,min_z);
dbrec3d_batch.set_input_int(5,max_z);
dbrec3d_batch.set_input_float(6,axis_x);
dbrec3d_batch.set_input_float(7,axis_y);
dbrec3d_batch.set_input_float(8,axis_z);
dbrec3d_batch.set_input_float(9,angle);
dbrec3d_batch.run_process();
(kernel_id,kernel_type)= dbrec3d_batch.commit_output(0);
kernel = dbvalue(kernel_id,kernel_type);