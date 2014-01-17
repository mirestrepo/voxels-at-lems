#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Maria Isabel Restrepo
# @Date:   2014-01-14 15:08:05
# @Last Modified by:   Maria Isabel Restrepo
# @Last Modified time: 2014-01-14 15:40:44
# Set up the paths to import c++ vpcl_adaptor

import sys


def setUpPaths(**kwargs):
    configuration         = kwargs.get('configuration', 'Debug')

    print "Setting include paths of the VPCL c++ Library"
    for key in kwargs:
        print "Arguments: %s: %s" % (key, kwargs[key])

    VPCL_BIN_PATH="/Users/isa/Dropbox/Projects/binaries/vpcl/vpcl_xcode_project/bin/" + configuration
    VPCL_LIB_PATH= "/Users/isa/Dropbox/Projects/binaries/vpcl/vpcl_xcode_project/lib/" + configuration
    VPCL_INCLUDE = "/Users/isa/Dropbox/Projects/vpcl/pyscripts";

    sys.path.append(VPCL_BIN_PATH)
    sys.path.append(VPCL_LIB_PATH)
    sys.path.append(VPCL_INCLUDE)

