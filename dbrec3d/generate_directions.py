#!/usr/bin/python

from math import pi, cos, sin;

# generate_derections.py
# This function returns a list of 4-d vectors. 
# The first 3 numbers correspond to the direction, the 4th number corresponds to the angle of rotation around the axis
# Angle convention of spherical system is from math not from physics. i.e theta = azimuthal, phi = polar
def dirs_edges(angle_res, theta_res):

  directions=[];

  # when zenith is is 
  theta = 0.0;# azimuthal
  phi = 0.0; #polar/zenith
  angle = 0.0;

  # rotations from and beyon pi are equivalent to opposite one
  while angle < pi - 1e-5:
    dir = 0.0, 0.0, 1.0, angle;
    directions.append(dir);
    angle+=angle_res;

  
  #when zenith is pi/2 we only traverse the entire hemisphere. Notice that the response to opposite kernels is the same but opposite sign
  phi = pi/2;
  while theta < 2*pi - 1e-5:
    angle = 0.0;
    while angle < pi - 1e-5:
      dir = cos(theta) * sin(phi), sin(theta) * sin(phi), cos(phi), angle;
      directions.append(dir);
      angle+=angle_res;
    theta+=theta_res;
    
  return directions
