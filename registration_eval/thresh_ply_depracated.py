#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo
Script to threshold a .ply file based on percentiles.
CAUTION! - This method is very memory inefficient
This file has been moved as part of vpcl
"""
import os
import sys
import numpy as np
from scipy import stats
from optparse import OptionParser


def write_ply(file_out, data):
  #Create header
  rows, cols = data.shape
  header = ('ply\n' +
  'format ascii 1.0\n' +
  'element vertex ' + str(rows) + '\n' +
  'property float x\nproperty float y\nproperty float z\n' +
  'property float nx\nproperty float ny\nproperty float nz\n' +
  'property float prob\nproperty float vis\nproperty float nmag\n' +
  'property uchar diffuse_red\nproperty uchar diffuse_green\nproperty uchar diffuse_blue\n'+
  'end_header\n');

  fid = open( file_out , 'w' )
  fid.write( header )
  np.savetxt( fid , data , fmt='%.5f %.5f %.5f %.5f %.5f %.5f %.5f %.5f %.5f %d %d %d', delimiter=' ')
  fid.close()

if __name__ == "__main__":

  #######################################################
  # handle inputs                                       #
  #######################################################
  parser = OptionParser()
  parser.add_option("-s", "--sceneroot", action="store", type="string", dest="sceneroot", help="root folder for this scene")
  parser.add_option("-i", action="store", type="string", dest="file_in",   default="", help=".PLY file to threshold")
  parser.add_option("-o", action="store", type="string", dest="out_basename",   default="", help="Output files are saved as out_basename_%.ply")
  (opts, args) = parser.parse_args()

  file_in = opts.file_in;
  fid = open(file_in, 'r')
  data = np.genfromtxt(fid, dtype=float, delimiter=' ', skip_header=16);
  fid.close()

  #normalize visibility
  data[:,7] = data[:,7]/(data[:,7].max());
  #normalize nmag
  data[:,8] = data[:,8]/(data[:,8].max());

  percentile=[90, 92, 95, 98, 99];

  data_measure = data[:,6] *data[:,7] *data[:,8]


for p in percentile :

    print 'Percentile: ' , p

    file_out = opts.out_basename + '_' + str(p) + ".ply"

    indices = (data_measure > stats.scoreatpercentile(data_measure, p));
    filtered_data = data[indices, :];
    write_ply(file_out, filtered_data)
