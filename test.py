#import Table
#fout = open('mytable.tex','w')
#t = Table.Table(3, justs='lrc', caption='Awesome results', label="tab:label")
#t.add_header_row(['obj', 'X', '$\\beta$'])
#col1 = [0.001,0.556,10.56]   # just numbers
#col2 = [0.001,0.556,10.56]   # just numbers
#col3 = [0.001,0.556,10.56]   # just numbers
#t.add_data([col1,col2,col3], 2)
#t.print_table(fout)
#fout.close()
#
#import numpy
#a=numpy.zeros((2,2))
#print " \\\\\n".join([" & ".join(map(str,line)) for line in a])
#
#print "DOne",
#"test"

import numpy
from mayavi.mlab import *

""" Demo the bar chart plot with a 2D array.
"""
s = numpy.abs(numpy.random.random((3, 3)))
barchart(s, mode='cube')
show()
print s
