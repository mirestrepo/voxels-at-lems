#!/usr/bin/python
# Script to save the responses of pairs as Drishti raw files
# Author : Isabel Restrepo
#10-08-2009

import bvpl_batch
import time
import os

#time.sleep(30);
bvpl_batch.register_processes();
bvpl_batch.register_datatypes();

data_dir="/Users/isa/Experiments/CapitolSFM/smaller_capitol/ocp+app/corners";

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string

print("Load Pair Grid");
bvpl_batch.init_process("bvplLoadPairGridProcess");
bvpl_batch.set_input_string(0, data_dir +"/pair_centers.vox");
bvpl_batch.run_process();
(id, type)= bvpl_batch.commit_output(0);
pair_grid = dbvalue(id, type);

print("Extract Response");
bvpl_batch.init_process("bvplPairToFloatProcess");
bvpl_batch.set_input_from_db(0,pair_grid);
bvpl_batch.set_input_string(1, data_dir +"/pair_resp.vox");
bvpl_batch.run_process();
(id, type)= bvpl_batch.commit_output(0);
float_grid = dbvalue(id, type);

print("Writing Response Grid");
bvpl_batch.init_process("bvxmSaveGridRawProcess");
bvpl_batch.set_input_from_db(0,float_grid);
bvpl_batch.set_input_string(1,data_dir + "/pair_resp.raw");
bvpl_batch.run_process();

#print("Load Voxel Grid");
#bvpl_batch.init_process("bvxmLoadGridProcess");
#bvpl_batch.set_input_string(0,data_dir + "/corners_top_resp.vox");
#bvpl_batch.set_input_string(1,"float");
#bvpl_batch.run_process();
#(response_grid_id,response_grid_type)= bvpl_batch.commit_output(0);
#response_grid = dbvalue(response_grid_id,response_grid_type);
#
#print("Writing Response Grid");
#bvpl_batch.init_process("bvxmSaveGridRawProcess");
#bvpl_batch.set_input_from_db(0,response_grid);
#bvpl_batch.set_input_string(1,data_dir + "/corners_top_resp.raw");
#bvpl_batch.run_process();