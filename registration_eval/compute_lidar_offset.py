#!/usr/bin/env python
# encoding: utf-8
"""
compute_lidar_offset.py

Created by Maria Isabel Restrepo on 2012-09-20.
Copyright (c) 2012 . All rights reserved.
"""
import os
import sys
import argparse
from liblas import file
import numpy as np

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-i",       action="store",   type=str,
        dest="input",
        default="",
        help="Input file")

    args = parser.parse_args()
    print args


    f = file.File(args.input, mode='r')
    h = f.header


    offset = np.array(h.min) + 0.5*(np.array(h.max) - np.array(h.min))
    print "Offset origin to center "
    print "--offset" , -1*offset[0], -1*offset[1], 0.0

