#!/usr/bin/python

import Queue 
import time
import os;
import optparse;
import shutil
from xml.etree.ElementTree import ElementTree

      
#function to parse and xml file containing the model directory and the xml_file_name (without the path)            
def parse_scenes_info(scenes_info_file, model_dirs, output_paths):
    
    print 'Parsing: ' + scenes_info_file
    
    #parse xml file
    bof_tree = ElementTree();
    bof_tree.parse(scenes_info_file);
    
    scenes_elm = bof_tree.getroot().findall('scene');
    
    if scenes_elm is None:
      print "Invalid bof info file: No scenes element"
      sys.exit(-1);
         
 
    #find scene paths
    for s in range(0, len(scenes_elm)):
        path = scenes_elm[s].get("path");
        output_dir = scenes_elm[s].get('output_dir');
        
        if path is None:
            print "Invalid info file: Error parsing scene path"
            sys.exit(-1);
            
        if output_dir is None:
            print "Invalid info file: Error parsing output dir "
            sys.exit(-1);
        
        model_dirs.append(path); 
        output_paths.append(output_dir);
        
def process_scene(scene_file, path):
        #parse xml file
    tree = ElementTree();
    tree.parse(scene_file);
    
    #find number of scenes
    paths_elm = tree.getroot().find('scene_paths');
    
    if paths_elm is None:
      print "Error parsing boxm scene: No paths_elm"
      sys.exit(-1);
      
    paths_elm.set('path', path);
    paths_elm.set('block_prefix', 'pmvs_scene');

    
    tree.write(path + '/pmvs_scene.xml');

#*********************The Main Algorithm ****************************#

if __name__=="__main__":
  #Parse inputs
  parser = optparse.OptionParser(description='Compute Expected Color Scene');

  parser.add_option('--scenes_info', action="store", dest="scenes_info", type="string", default="");
 
  options, args = parser.parse_args()

  scenes_info = options.scenes_info;
  
  model_dirs = [];
  output_paths = [];
  parse_scenes_info(scenes_info, model_dirs, output_paths);
  
  if(len(model_dirs)==len(output_paths)):
      for idx in range(0,len(model_dirs)):
          if not os.path.isdir(output_paths[idx] +"/"):
              os.mkdir(output_paths[idx] +"/");
              
          process_scene(model_dirs[idx], output_paths[idx])    
          
      
    

  



  
  
