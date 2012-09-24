#!/usr/bin/env python
# encoding: utf-8
"""
vpcl_ply2pcd.py
Convert a /ply file to .pcd
Created by Maria Isabel Restrepo on 2012-09-20.
Copyright (c) 2012 . All rights reserved.
"""
import os
import sys
import logging
import argparse
from vpcl_adaptor import *

LOG = None

def process_command_line(argv):
    """
    Return a 2-tuple: (settings object, args list).
    `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
    """
    global LOG
    if argv is None:
        argv = sys.argv[1:]
    
    # initialize the parser object:
    parser = argparse.ArgumentParser(description="Export PLY to PCD file")
    
    # define options here:
    parser.add_argument("-i", "--input_file",   action='store',    type = str,   dest="input_file",    help=".ply file")
    parser.add_argument("-o", "--output_file",  action='store',    type = str,   dest="output_file",   help=".pcd file")
    parser.add_argument("-t", "--point_type",   action='store',    type = str,   dest="point_type",    default="PointNormal",    help="Type of data")
    parser.add_argument("-v", "--verbose",      action='store',    type = bool,   dest="verbose",       default=True,  help="Write debug log to log_file")
    parser.add_argument("-L", "--log", dest="logfile", help="write debug log to log_file")
 
    args = parser.parse_args(argv)
    
    # set up logging
    if args.verbose:
        LOG = setlogging(args.logfile)
        
    if not args.input_file or not args.output_file :
        pass
        LOG.error("Input or Output filename not specified")
        parser.error("You must supply an input file")
    
    return args

def main(argv=None):
    args = process_command_line(argv)
    return ply2pcd(args.input_file, args.output_file, args.point_type, 1)

def setlogging(logfile=None):
    consolelevel = logging.DEBUG
    logger = logging.getLogger(__name__)
    logger.setLevel(consolelevel)
    # create formatter and add it to the handlers
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(consolelevel)
    ch.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    
    # create file handler which logs error messages
    if logfile:
        filelevel = logging.ERROR
        fh = logging.FileHandler(logfile)
        fh.setLevel(filelevel)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    
    #test logging
    # logger.debug("debug message")
    # logger.info("info message")
    # logger.warn("warn message")
    # logger.error("error message")
    # logger.critical("critical message")
    
    return logger

if __name__ == '__main__':
    status = main()
    sys.exit(status)
