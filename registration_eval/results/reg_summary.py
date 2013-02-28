import numpy as np
from mayavi.mlab import *
import vtk


errorFPFH = np.array([[3.0/18.0, 0, 1.0/18.0, 0, 0, 0],
    [0,0,20.0/54.0,0,0,0],
    [1.0/3.0,0,4.0/12.0,0,0,3.0/6.0],
    [3.0/3.0,10.0/12.0,2.0/3.0,0,0,2.0/3.0],
    [30.0/30.0,0,30.0/30.0,18.0/30.0,0,0],
    [10.0/10.0,3.0/10.0,9.0/10.0,4.0/10.0,6.0/10.0,0]])

errorSHOT = np.array([[4.0/18.0, 0, 1.0/18.0, 0, 0, 0],
    [0,0,17.0/54.0,0,0,0],
    [1.0/3.0,0,4.0/12.0,0,0,4.0/6.0],
    [3.0/3.0,10.0/12.0,3.0/3.0,0,0,2.0/3.0],
    [30.0/30.0,0,30.0/30.0,19.0/30.0,0,0],
    [10.0/10.0,9.0/10.0,10.0/10.0,9.0/10.0,9.0/10.0,0]])

barchart(errorFPFH, opacity=0.9)
#surf(error, warp_scale='auto')
#outline()
#axes()
show()

# ex = vtk.vtkGL2PSExporter()
# # defaults
# ex.SetFilePrefix(f_prefix)
# ex.SetFileFormatToPDF()
# ex.SetSortToBSP()
# # configure the exporter.
# c = vtkPipeline.ConfigVtkObj.ConfigVtkObj(self.renwin)
# c.configure(self.frame, ex, get=[], auto_update=1,
#             one_frame=1, run_command=0)
# self.frame.update()
# c.root.transient(self.frame)
# self.frame.wait_window(c.root)

# self.lift()
# ex.SetRenderWindow(self.renwin)
# Common.state.busy()
# ex.Write()
# Common.state.idle()