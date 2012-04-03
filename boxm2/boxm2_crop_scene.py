# A file to crop blocks from a boxm2 scene
# Takes boxm2_dir as input and assumes scene.xml file is present at that location
# Writes the cropped parameters to scene-cropped.xml

import optparse;
from xml.etree.ElementTree import ElementTree

#Parse inputs
parser = optparse.OptionParser(description='Update BOXM2 Scene without refinement 0');

parser.add_option('--boxm2_dir', action="store", dest="boxm2_dir");
parser.add_option('--min_i', action="store", dest="min_i", type="int");
parser.add_option('--min_j', action="store", dest="min_j", type="int");
parser.add_option('--min_k', action="store", dest="min_k", type="int");
parser.add_option('--max_i', action="store", dest="max_i", type="int");
parser.add_option('--max_j', action="store", dest="max_j", type="int");
parser.add_option('--max_k', action="store", dest="max_k", type="int");
options, args = parser.parse_args()

boxm2_dir = options.boxm2_dir;
min_i = options.min_i;
min_j = options.min_j;
min_k = options.min_k;
max_i = options.max_i;
max_j = options.max_j;
max_k = options.max_k;


scene_input_file = boxm2_dir + '/scene.xml';
scene_output_file = boxm2_dir + '/scene_cropped.xml';

print 'Parsing: ' 
print scene_input_file

#parse xml file
tree_in = ElementTree();
tree_in.parse(scene_input_file);

tree_out = ElementTree();


#find all blocks removing those outside the limits
blocks = tree_in.getroot().findall('block');

for block in blocks:
    if block is None:
       print "Invalid info file: No resolution"
       sys.exit(-1);
       
    i = float(block.get('id_i'));
    j = float(block.get('id_j'));
    k = float(block.get('id_k'));
    
    if  (not (i in range(min_i, max_i))) or (not (j in range(min_j, max_j))) or (not (k in range(min_k, max_k))):
        tree_in.getroot().remove(block)
    
tree_in.write(scene_output_file);