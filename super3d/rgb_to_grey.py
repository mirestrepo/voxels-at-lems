import boxm_batch;
import sys;
import optparse;
import os;
import glob;

#import matplotlib.pyplot as plt;
boxm_batch.register_processes();
boxm_batch.register_datatypes();

class dbvalue:
  def __init__(self, index, type):
    self.id = index    # unsigned integer
    self.type = type   # string
    
import random

#Parse inputs
parser = optparse.OptionParser(description='Conver rbg images to grey');

parser.add_option('--rgb_dir', action="store", dest="rgb_dir");
parser.add_option('--grey_dir', action="store", dest="grey_dir");


options, args = parser.parse_args()

rgb_dir = options.rgb_dir;
grey_dir = options.grey_dir;


if not os.path.isdir(rgb_dir + '/'):
    print "Invalid RGB Dir"
    sys.exit(-1);
    
if not os.path.isdir(grey_dir + '/'):
    os.mkdir(grey_dir + '/');
    
    
rgb_imgs = glob.glob1(rgb_dir, '*.png');

for img in rgb_imgs:

    #tif_img_name = os.path.splitext(img)[0] + '.tif';
    
    boxm_batch.init_process("vilLoadImageViewProcess");
    boxm_batch.set_input_string(0,rgb_dir + '/' + img);
    boxm_batch.run_process();
    (id,type) = boxm_batch.commit_output(0);
    rgb_img = dbvalue(id,type);

    
    boxm_batch.init_process("vilRGBToGreyProcess");
    boxm_batch.set_input_from_db(0,rgb_img);
    boxm_batch.run_process();
    (id,type) = boxm_batch.commit_output(0);
    grey_img = dbvalue(id,type);

    boxm_batch.init_process("vilSaveImageViewProcess");
    boxm_batch.set_input_from_db(0,grey_img);
    boxm_batch.set_input_string(1,grey_dir + '/' + img);
    boxm_batch.run_process();

    boxm_batch.remove_data(rgb_img.id)
    boxm_batch.remove_data(grey_img.id)