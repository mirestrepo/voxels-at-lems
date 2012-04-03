#!/usr/bin/env python
# encoding: utf-8
"""

Created by Preston Holmes on 2010-01-13.
preston@ptone.com
Copyright (c) 2010

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

"""
Usage: 
cd to target directory
path/to/pool-resize.py /path/to/src/images/*.jpg
"""


from multiprocessing import Pool

import sys
import os
import os.path
import Image
resize_factor = 0.5
dest = os.getcwd()

def resize(x):

        try:
            # Attempt to open an image file
            filepath = x
            image = Image.open(filepath)
        except IOError, e:
            # Report error, and then skip to the next argument
            print "Problem opening", filepath, ":", e
            return
        
        h,w = image.size
        h,w = (int(h * resize_factor), int(w * resize_factor))
        # Resize the image
        image = image.resize((h,w), Image.ANTIALIAS)
        fname = os.path.basename(filepath)
        
        # Split our original filename into name and extension
        (name, extension) = os.path.splitext(fname)
        
        # Save the thumbnail as "(original_name)_thumb.png"
        image.save(os.path.join(dest,name + '.jpg'),quality=80)
        image = None



if __name__ == '__main__':
    core_ct = os.sysconf('SC_NPROCESSORS_ONLN')
    pool = Pool(processes=core_ct)
    pool.map(resize,sys.argv[1:])
    pool.close()
    pool.join()