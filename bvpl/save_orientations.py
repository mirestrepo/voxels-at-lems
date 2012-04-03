# Script to crop a voxel grid
# Author : Isabel Restrepo
# 6-14-2009

import bvpl_batch
import time
#time.sleep(60);
bvpl_batch.register_processes();
bvpl_batch.register_datatypes();


class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

data_dir = "/Volumes/Experiments/object_recognition/bvpl/CapitolSiteHigh/cropped_world"
param_dir = "/Projects/lemsvxl/src/contrib/isabel/params"
#first creat an empty world.
print("Load Voxel World");
bvpl_batch.init_process("bvxmLoadGridProcess");
bvpl_batch.set_input_string(0, data_dir + "/edge3d_alge_orientations.vox");
bvpl_batch.set_input_string(1,"vnl_vector_fixed_float_3");
bvpl_batch.run_process();
(grid_id,grid_type)= bvpl_batch.commit_output(0);
orientation_grid = dbvalue(grid_id,grid_type);

print("Load Voxel World");
bvpl_batch.init_process("bvxmLoadGridProcess");
bvpl_batch.set_input_string(0, data_dir + "/edge3d_alge.vox");
bvpl_batch.set_input_string(1,"float");
bvpl_batch.run_process();
(grid_id,grid_type)= bvpl_batch.commit_output(0);
grid = dbvalue(grid_id,grid_type);

print("Combine grids");
bvpl_batch.init_process("bvxmCombineGridsProcess");
bvpl_batch.set_input_from_db(0, orientation_grid );
bvpl_batch.set_input_from_db(1, grid );
bvpl_batch.set_input_string(2,data_dir + "/edge3d_combined.vox");
bvpl_batch.run_process();
(grid_id,grid_type)= bvpl_batch.commit_output(0);
combined_grid = dbvalue(grid_id,grid_type);

print("Creating 3D edge kernel");
bvpl_batch.init_process("bvplCreateEdge3dKernelVectorProcess");
bvpl_batch.set_input_unsigned(0, 5);  #width
bvpl_batch.set_input_unsigned(1, 5);  #height
bvpl_batch.set_input_unsigned(2, 5);  #length
bvpl_batch.run_process();
(kernel_id,kernel_type)= bvpl_batch.commit_output(0);
kernel_vector = dbvalue(kernel_id,kernel_type);

print("Convert to hsv space");
bvpl_batch.init_process("bvplConvertDirectionToHueProcess");
bvpl_batch.set_input_from_db(0,combined_grid );
bvpl_batch.set_input_from_db(1,kernel_vector);
bvpl_batch.set_input_string(2,data_dir+"/grid_hsv.vox");
bvpl_batch.run_process();
(id,type)= bvpl_batch.commit_output(0);
grid_hsv = dbvalue(id,type);


print("Writing Orientation Grid");
bvpl_batch.init_process("bvxmGridToImageStackProcess");
bvpl_batch.set_input_from_db(0,grid_hsv);
bvpl_batch.set_input_string(1,"vnl_vector_fixed_float_4");
bvpl_batch.set_input_string(2,data_dir + "/edge3d_orientations");
bvpl_batch.run_process();


