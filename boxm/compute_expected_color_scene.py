#!/usr/bin/python

import boxm_batch;
import optparse;
import os;
import sys;

if __name__=="__main__":
  boxm_batch.register_processes();
  boxm_batch.register_datatypes();

  class dbvalue:
    def __init__(self, index, type):
      self.id = index    # unsigned integer
      self.type = type   # string


  #Parse inputs
  parser = optparse.OptionParser(description='Compute Expected Color Scene');

  parser.add_option('--model_dir', action="store", dest="model_dir", type="string", default="");
  parser.add_option('--model_name', action="store", dest="model_name", type="string",default="");
  parser.add_option('--grey_offset', action="store", dest="grey_offset", type="float", default=0);

  options, args = parser.parse_args()

  model_dir = options.model_dir;
  model_name = options.model_name;
  grey_offset = options.grey_offset;

  if len(model_dir) == 0:
    print "Missing Model Dir"
    sys.exit(-1);
      
  if len(model_name) == 0:
    print "Missing Model Name"
    sys.exit(-1);
      
  if not os.path.isdir(model_dir +"/"):
    print "Invalid Model Dir"
    sys.exit(-1);


  print("Creating a Scene");
  boxm_batch.init_process("boxmCreateSceneProcess");
  boxm_batch.set_input_string(0,  model_dir + "/" + model_name + ".xml");
  boxm_batch.run_process();
  (scene_id, scene_type) = boxm_batch.commit_output(0);
  scene= dbvalue(scene_id, scene_type);

  #print("*************************************");
  #print("Save Scene");
  #boxm_batch.init_process("boxmSaveOccupancyRawProcess");
  #boxm_batch.set_input_from_db(0,scene);
  #boxm_batch.set_input_string(1,model_dir + "/" + model_name);
  #boxm_batch.set_input_unsigned(2,0);
  #boxm_batch.set_input_unsigned(3,1);
  #boxm_batch.run_process();

  print("*************************************");
  print("Computing Excpected Color Scene");
  boxm_batch.init_process("boxmComputeExpectedColorSceneProcess");
  boxm_batch.set_input_from_db(0, scene);
  boxm_batch.set_input_float(1, grey_offset);
  boxm_batch.run_process();
  (scene_id, scene_type) = boxm_batch.commit_output(0);
  expected_color_scene = dbvalue(scene_id, scene_type);

  print("*************************************");
  print("Save Scene");
  boxm_batch.init_process("boxmSaveOccupancyRawProcess");
  boxm_batch.set_input_from_db(0,expected_color_scene);
  boxm_batch.set_input_string(1, model_dir + "/mean_color_scene");
  boxm_batch.set_input_unsigned(2,0);
  boxm_batch.set_input_unsigned(3,1);
  boxm_batch.run_process();

