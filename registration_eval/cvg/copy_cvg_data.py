import glob, sys, os
import random
import shutil

flights = [2]
sites = [7]

for flight in flights:
    for site in sites:
        dir_in = "/Volumes/CVG_PVD_DATA/EO/flight" + str(flight) + "_sites/site_"+ str(site)
        dir_out = "/data/CVG_PVD_DATA/EO/flight" + str(flight) + "_sites/site_"+ str(site)

        if not os.path.isdir(dir_out +"/"):
            os.makedirs(dir_out +"/");

        files = glob.glob1(dir_in, '*.png')

        rnd_files = random.sample(files, 300)

        for this_file  in rnd_files:
            src = dir_in + '/' + this_file
            dst = dir_out + '/' +this_file
            print "Copying", src
            print "To", dst
            shutil.copy(src, dst);

print "Done"