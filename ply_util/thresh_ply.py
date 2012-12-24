#!/usr/bin/env python
# encoding: utf-8
"""
Author: Isabel Restrepo
Script to threshold a .ply file based on percentiles.
CAUTION! - This method is very memory inefficient
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

#Threshold using pvn and bounding box
def thresh_bbox(file_in, file_out,
                min_pt, max_pt):
  fid = open(file_in, 'r')
  data_full = np.genfromtxt(fid, dtype=float, delimiter=' ', skip_header=16);
  fid.close()

  data = data_full[(data_full[:,0] > min_pt[0]), :]
  data = data[(data[:,0] < max_pt[0]), :]
  data = data[(data[:,1] > min_pt[1]), :]
  data = data[(data[:,1] < max_pt[1]), :]
  data = data[(data[:,2] > min_pt[2]), :]
  data = data[(data[:,2] < max_pt[2]), :]
  write_ply(file_out, data)

#Threshold using a bounding sphere
def thresh_bsphere(file_in, file_out,
                   centroid, max_pt):
  fid = open(file_in, 'r')
  data_full = np.genfromtxt(fid, dtype=float, delimiter=' ', skip_header=16);
  fid.close()

  rad = (max_pt - centroid) * (max_pt - centroid);
  radXY = rad[0] + rad[1]
  radZ = rad[2]

  dx = (data_full[:,0] - centroid[0])*(data_full[:,0] - centroid[0])
  dy = (data_full[:,1] - centroid[1])*(data_full[:,1] - centroid[1])
  indeces =  (dx + dy) < radXY
  data = data_full[indeces, :]
  dz = (data[:,2] - centroid[2])*(data[:,2] - centroid[2])
  data = data[ dz < radZ, :]

  write_ply(file_out, data)

def thresh_pvn( file_in, out_basename):
  fid = open(file_in, 'r')
  data = np.genfromtxt(fid, dtype=float, delimiter=' ', skip_header=16);
  fid.close()

  #normalize visibility
  data[:,7] = data[:,7]/(data[:,7].max());
  #normalize nmag
  data[:,8] = data[:,8]/(data[:,8].max());

  percentile = [90, 95, 99];

  data_measure = data[:,6] *data[:,7] *data[:,8]


  for p in percentile:

      print 'Percentile: ' , p

      file_out = out_basename + '_' + str(p) + ".ply"

      indices = (data_measure > stats.scoreatpercentile(data_measure, p));
      filtered_data = data[indices, :];
      write_ply(file_out, filtered_data)


if __name__ == "__main__":

  #######################################################
  # handle inputs                                       #
  #######################################################
  parser = OptionParser()
  parser.add_option("-i", action="store", type="string", dest="file_in",   default="", help=".PLY file to threshold")
  parser.add_option("-o", action="store", type="string", dest="out_basename",   default="", help="Output files are saved as out_basename_%.ply")
  (opts, args) = parser.parse_args()

  thresh_pvn(opts.file_in,opts.out_basename)
