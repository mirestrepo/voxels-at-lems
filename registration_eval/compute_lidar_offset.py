#!/usr/bin/env python
# encoding: utf-8
"""
compute_lidar_offset.py

Created by Maria Isabel Restrepo on 2012-09-20.
Copyright (c) 2012 . All rights reserved.
"""
import os
import sys
import logging
import optparse

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
    parser = optparse.OptionParser(
        formatter=optparse.TitledHelpFormatter(width=78),
        add_help_option=None)
    
    # define options here:
    parser.add_option("-f", "--file", dest="filename",
                      help="read data from FILENAME")
    parser.add_option("-v", "--verbose", dest="verbose", default=False,
                      action='store_true', help="write debug log to FILENAME")
    parser.add_option("-L", "--log", dest="logfile", help="write debug log to FILENAME")
    parser.add_option(      # customized description; put --help last
        '-h', '--help', action='help',
        help='Show this help message and exit.')
    
    options, args = parser.parse_args(argv)
    
    # check number of arguments, verify values, etc.:

    # set up logging
    if options.verbose:
        LOG = setlogging(options.logfile)
        
    if not options.filename:
        pass
        #LOG.error("Input filename not specified")
        #parser.error("You must supply an input file")
    # further process settings & args if necessary
    
    return options, args

def main(argv=None):
    settings, args = process_command_line(argv)
    
    # application code here, like:
    # run(settings, args)
    return 0        # success

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
    logger.debug("debug message")
    logger.info("info message")
    logger.warn("warn message")
    logger.error("error message")
    logger.critical("critical message")
    
    return logger

if __name__ == '__main__':
    status = main()
    sys.exit(status)
