import bvxm_batch
bvxm_batch.register_processes();
bvxm_batch.register_datatypes();

#Delay for debugging
import time


class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

input_dir = "/Users/isa/Experiments/CapitolSFM/capitol_rotated"
output_dir = "/Users/isa/Experiments/CapitolSFM/smaller_capitol"


print("Load Grid World");
bvxm_batch.init_process("bvxmLoadGridProcess");
bvxm_batch.set_input_string(0,input_dir + "/KL_gaussf1.vox");
bvxm_batch.set_input_string(1,"bsta_gauss_f1");
bvxm_batch.run_process();
(world_id,world_type)= bvxm_batch.commit_output(0);
world = dbvalue(world_id,world_type);

print("Crop Voxel World");
bvxm_batch.init_process("bvxmCropGridProcess");
bvxm_batch.set_params_process(output_dir +"/crop_grid_params.xml");
bvxm_batch.set_input_from_db(0,world);
bvxm_batch.set_input_string(1, output_dir +"/KL_gaussf1.vox");
bvxm_batch.run_process();
(crop_world_id,crop_world_type)= bvxm_batch.commit_output(0);
crop_world = dbvalue(crop_world_id,crop_world_type);

print("Writing World");
bvxm_batch.init_process("bvxmSaveGridRawProcess");
bvxm_batch.set_input_from_db(0,crop_world);
bvxm_batch.set_input_string(1,output_dir + "/KL_gaussf1.raw");
bvxm_batch.run_process();

print("Load Grid World");
bvxm_batch.init_process("bvxmLoadGridProcess");
bvxm_batch.set_input_string(0,input_dir + "/MPM_gaussf1.vox");
bvxm_batch.set_input_string(1,"bsta_gauss_f1");
bvxm_batch.run_process();
(world_id,world_type)= bvxm_batch.commit_output(0);
world = dbvalue(world_id,world_type);

print("Crop Voxel World");
bvxm_batch.init_process("bvxmCropGridProcess");
bvxm_batch.set_params_process(output_dir +"/crop_grid_params.xml");
bvxm_batch.set_input_from_db(0,world);
bvxm_batch.set_input_string(1,output_dir +"/MPM_gaussf1.vox");
bvxm_batch.run_process();
(crop_world_id,crop_world_type)= bvxm_batch.commit_output(0);
crop_world = dbvalue(crop_world_id,crop_world_type);

print("Writing World");
bvxm_batch.init_process("bvxmSaveGridRawProcess");
bvxm_batch.set_input_from_db(0,crop_world);
bvxm_batch.set_input_string(1,output_dir + "/MPM_gaussf1.raw");
bvxm_batch.run_process();


print("Load Grid World");
bvxm_batch.init_process("bvxmLoadGridProcess");
bvxm_batch.set_input_string(0,input_dir + "/ocp.vox");
bvxm_batch.set_input_string(1,"float");
bvxm_batch.run_process();
(world_id,world_type)= bvxm_batch.commit_output(0);
world = dbvalue(world_id,world_type);

print("Crop Voxel World");
bvxm_batch.init_process("bvxmCropGridProcess");
bvxm_batch.set_params_process(output_dir + "/crop_grid_params.xml");
bvxm_batch.set_input_from_db(0,world);
bvxm_batch.set_input_string(1, output_dir + "/ocp.vox");
bvxm_batch.run_process();
(crop_world_id,crop_world_type)= bvxm_batch.commit_output(0);
crop_world = dbvalue(crop_world_id,crop_world_type);

print("Writing World");
bvxm_batch.init_process("bvxmSaveGridRawProcess");
bvxm_batch.set_input_from_db(0,crop_world);
bvxm_batch.set_input_string(1,output_dir + "/ocp.raw");
bvxm_batch.run_process();
