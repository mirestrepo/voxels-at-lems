from utils.bbgm_utils import *
from utils.bbgm_multiprocessing import measureProb,measureProbQueue,bbgmJob,executeJobs,GUIInvoker
from multiprocessing import Queue
import time
import multiprocessing

dbbgm_batch.register_processes();
dbbgm_batch.register_datatypes();

path="C:/Users/octi/Documents/Mundy Group/imagedata/tree_sequence/";

#model=updateImageStream(path,300,0.1,0.02,0,-1);
#saveModel(path+"/out_wv/model.mdl",model);
model=loadModel(path+"/out_wv/model.mdl");

#myWavelet=wvXform("bbgm_image_sptr",model,2,2,3);
#saveWavelet(path+"out_wv/wavelet.wv",myWavelet);
myWavelet=loadWavelet(path+"out_wv/wavelet.wv");
mySubband=getSubband("bbgm_image_sptr",3,"LL",2,myWavelet);
inverse=getSubband("bbgm_image_sptr",3,"LL",0,myWavelet);
waveletDomain=getSubband("bbgm_image_sptr",3,"forward",0,myWavelet);
[test_image,ni,nj]=openImage(path+"00001.tiff");
#dbbgm_batch.print_db();
Mean=displayImg(model,"mean",0,1);
#Mean2=displayImg(model,"mean",1,1);
#saveImg(Mean,path+"/out_stats/mean.jpg");
#saveImg(Mean2,path+"/out_stats/mean2.jpg");
prob_map=measureWvLookup(myWavelet,test_image,"probability",0.15,"bil",path+"/out_stats/");


frame_num=20;
ImageList=[];
job_list=[];
t1=time.time();
work_queue=Queue();
num_cores=5;
for x in range(1,frame_num):
    [current_im,cur_ni,cur_nj]=openImage(path+frameSuffix(x,5)+".tiff");
    ImageList.append(current_im);
 
if __name__=="__main__": #you really need this if you want to do multiprocessing. Otherwise unthinkable, evil things will occur on your machine 
    #There should be only one example running at a time. Uncomment the block to run it.
    
######===============================================================================================================================######    
    #Example 1: The easy way to do multiprocessing; Each thread contains the same parameters of the 
    #experiment and only the frame index varies. We first enqueue all the frame indeces in a queue
    #initialize each process with the experiment parameters, and start it
   
   
#    for i in range(1,frame_num):
#        work_queue.put(i)
#    
#    for i in range(num_cores):
#        current_process=measureProbQueue(myWavelet,"probability",0.15,"bil",path+"/out_stats/",path,path+"/out_pmap/",work_queue)
#        current_process.start()

######===============================================================================================================================###### 
    
    #Example 2: The more general/Object-Oriented way to do multiprocessing; Each thread contains an input and an output Queue. The input Queue contains Job objects that have the experiment
    #parameters. We create the Job objects, Enqueue them in the input queue and then start each process. The output Queue is empty for this particular example.   
    
    for i in range(1,frame_num):
        current_job=bbgmJob(myWavelet,"probability",0.15,"bil",path+"/out_stats/",path+frameSuffix(i,5)+".tiff",path+"/out_pmap/"+frameSuffix(i,3)+".tiff") 
        job_list.append(current_job)
    executeJobs(job_list,num_cores)  

######===============================================================================================================================###### 
    
    #Example 3: Load three different GUI windows (possibly with different tableau's in each one)
#    GUIInvoker(model,mySubband,waveletDomain,prob_map).start();  
#    GUIInvoker(model,inverse,waveletDomain,0).start(); 
#    GUIInvoker(model,0,waveletDomain,0).start();   
   
#    dbbgm_batch.print_db(); 
#print dbbgm_batch.remove_data(model.id);
 
