from optparse import OptionParser
import numpy as np
from sklearn import preprocessing, neighbors, svm
from sklearn.naive_bayes import MultinomialNB 
from sklearn.metrics import *
import matplotlib.pyplot as plt
import matplotlib.cm as cmt


#*******************The Main Algorithm ************************#
if __name__=="__main__":

  parser = OptionParser()
  parser.add_option("-r", "--radius", action="store", type="int", dest="radius", help="radius (multiple of resolution)");
  parser.add_option("-p", "--percent", action="store", type="int", dest="percentile", help="percentile of original samples");
  parser.add_option("-d", "--descriptor", action="store", type="string", dest="descriptor_type", help="name of the descriptor i.e FPFH");
  parser.add_option("-k", "--nmeans", action="store", type="int", dest="K", help="number of means");
  parser.add_option("-c", "--clf_name", action="store", type="string", dest="clf_name", help="classifier name");

  (opts, args) = parser.parse_args()
  print opts
  print args

  ft=opts.descriptor_type;
  radius=opts.radius;
  percentile=opts.percentile;
  K=opts.K;
  clf_name = opts.clf_name;
  trials = (0,3,4)
#  trials = (0,1, 2, 3,4)
#  trials = (0,1, 2, 3)



#*************************************************************************
# Read all labels and get average confusion matrix and average report
#*************************************************************************
  feature_name = ft + "_" + str(radius);
   
  #Where results will be saved
  avg_classification_dir = "/Users/isa/Experiments/bof_bmvc12/" + "/average/" + feature_name   + "/percentile_" + str(percentile) 
  avg_classification_dir = avg_classification_dir + "/classification_" + str(K);
 
  descriptor_dir = "/Users/isa/Experiments/bof_bmvc12/" + "/trial_" + str(0) + "/" + feature_name   + "/percentile_" + str(percentile) 
  classification_dir = descriptor_dir + "/classification_" + str(K)
  prfs_file = classification_dir +'/' + clf_name + "_prf1s.txt"
  fis = open(prfs_file, 'r');
  prf1s = np.genfromtxt(fis)
  recall = prf1s[:,1];
  support = prf1s[:,3];
  fis.close();


  for trial in trials:
    descriptor_dir = "/Users/isa/Experiments/bof_bmvc12/" + "/trial_" + str(trial) + "/" + feature_name   + "/percentile_" + str(percentile) 
    classification_dir = descriptor_dir + "/classification_" + str(K);
    prfs_file = classification_dir +'/' + clf_name + "_prf1s.txt"
    fis = open(prfs_file, 'r');
    prf1s = np.genfromtxt(fis)
    recall = np.vstack((recall, prf1s[:,1]));
    support = np.vstack((support, prf1s[:,3]));
    fis.close();
    
  #save the recall file
  print "Saving Recall to:" + avg_classification_dir
  recall_file = avg_classification_dir +'/' + clf_name + "_recall.txt"
  fos = open(recall_file, 'w');
  np.savetxt(fos,recall);
  fos.close();
  support_file = avg_classification_dir +'/' + clf_name + "_support.txt"
  fos = open(support_file, 'w');
  np.savetxt(fos,support);
  fos.close();