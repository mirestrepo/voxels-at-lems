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
import argparse


def compute_mean(file_in, lines2skip=16):
  fid = open(file_in, 'r')
  xyz = np.genfromtxt(fid, dtype=float, delimiter=' ',
                       skip_header=lines2skip,
                       usecols={0, 1, 2});
  fid.close()

  centroid = np.mean(xyz, axis=0)

  return centroid



if __name__ == "__main__":

  #######################################################
  # handle inputs                                       #
  #######################################################
  parser = argparse.ArgumentParser(description="Get INFO on PLY")
  parser.add_argument("-i", action="store", type=str, dest="file_in",   default="", help=".PLY for info")
  parser.add_argument("-s", action="store", type=int, dest="lines2skip",   default=16, help="number of headerlines to skip")

  args = parser.parse_args()

  c = compute_mean(args.file_in, args.lines2skip)

  print c
