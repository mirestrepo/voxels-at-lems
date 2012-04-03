# THIS IS /helicopter_providence/middletown_3_29_11/site2_planes/boxm2_1/boxm2_update_and_refine_scene.py
import os,re, random;
import sys;
import optparse;
import numpy;

#Parse inputs
parser = optparse.OptionParser(description='tavsan');

parser.add_option('--boxm2_dir', action="store", dest="boxm2_dir");
parser.add_option('--imgdir', action="store", dest="imgdir", type="string");
parser.add_option('--chunks', action="store", dest="chunks",type="int");

options, args = parser.parse_args()

boxm2_dir = options.boxm2_dir;
imgdir = options.imgdir;
chunks = options.chunks;

if not os.path.isdir(imgdir):
    print "Invalid Image Dir"
    sys.exit(-1);
    
imgs = len(os.listdir(imgdir))

list = range(0,imgs,1);
random.shuffle(list);

avg = imgs/ float(chunks);
out = []
last = 0.0;
while last < imgs:
    out.append(list[int(last):int(last + avg)])
    last += avg

f = open(boxm2_dir+"/list.txt", 'w')

for list in out:
    print len(list)
    for item in list:
        f.write("%d " % item)
    f.write("\n")
