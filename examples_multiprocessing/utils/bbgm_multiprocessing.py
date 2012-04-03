'''
Created on Nov 15, 2010

@author: octi
'''
import dbbgm_batch
import multiprocessing
import Queue 
from bbgm_utils import saveImg,dbvalue,openImage,frameSuffix,frameSuffixWrite
        
class GUIInvoker(multiprocessing.Process):
    def __init__(self,model,inv_model,fwd_model,pMap):
        self.mdl=model
        self.invmdl=inv_model
        self.fwd=fwd_model
        self.pmap=pMap
        multiprocessing.Process.__init__(self)
    def run(self):
        dbbgm_batch.init_process("bbgmInvokeGUIProcess");
        dbbgm_batch.set_input_from_db(0,self.mdl);
        dbbgm_batch.set_input_from_db(1,self.invmdl);
        dbbgm_batch.set_input_from_db(2,self.fwd);
        dbbgm_batch.set_input_from_db(3,self.pmap);
        print   dbbgm_batch.run_process();
        return []   

def executeJobs(jobs, num_procs=5):
    work_queue=multiprocessing.Queue();
    result_queue=multiprocessing.Queue();
    for job in jobs:
        work_queue.put(job)
    
    for i in range(num_procs):
        worker= measureProbWorker(work_queue,result_queue)
        worker.start();
        print("worker with name ",worker.name," started!")
    
    
    
class bbgmJob():
    def __init__(self,wavelet,attribute,tolerance,interp_functor,data_path,input_path,output_path):
        self.wavelet=wavelet;
        self.test_image_path=input_path;
        self.attribute=attribute;
        self.tolerance=tolerance;
        self.interp_functor=interp_functor;
        self.data_path=data_path;
        self.output_path=output_path;
        
              
class measureProbWorker(multiprocessing.Process):
 
    def __init__(self,work_queue,result_queue):
        # base class initialization
        multiprocessing.Process.__init__(self)
        # job management stuff
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.kill_received = False
    
    def run(self):
        while not self.kill_received:
 
            # get a task
            try:
                job = self.work_queue.get_nowait()
            except Queue.Empty:
                break
            # store the result
            [test_image,ni,nj]=openImage(job.test_image_path);
            dbbgm_batch.init_process("bbgmMeasureWvLookupProcess");
            dbbgm_batch.set_input_from_db(0,job.wavelet);
            dbbgm_batch.set_input_from_db(1,test_image);
            dbbgm_batch.set_input_string(2,job.attribute);
            dbbgm_batch.set_input_float(3,job.tolerance);
            dbbgm_batch.set_input_string(4,job.interp_functor);
            dbbgm_batch.set_input_string(5,job.data_path);
            print dbbgm_batch.run_process();
            out_image=dbvalue(0,"")
            (out_image.id,out_image.type)=dbbgm_batch.commit_output(0);
            saveImg(out_image,job.output_path)   

class measureProbQueue(multiprocessing.Process):  
    def __init__(self,wavelet,attribute,tolerance,interp_functor,data_path,input_path,output_path,input_queue):
        multiprocessing.Process.__init__(self)
        self.wavelet=wavelet;
        self.input_path=input_path
        self.attribute=attribute;
        self.tolerance=tolerance;
        self.interp_functor=interp_functor;
        self.data_path=data_path;
        self.input_queue=input_queue;
        self.output_path=output_path;
        self.kill_received=False
   
    def run(self):
        while not self.kill_received:
            try:
                index = self.input_queue.get_nowait()
                
            except Queue.Empty:
                break
            # store the result
            [test_image,ni,nj]=openImage(self.input_path+frameSuffix(index,5)+".tiff");
            dbbgm_batch.init_process("bbgmMeasureWvLookupProcess");
            dbbgm_batch.set_input_from_db(0,self.wavelet);
            dbbgm_batch.set_input_from_db(1,test_image);
            dbbgm_batch.set_input_string(2,self.attribute);
            dbbgm_batch.set_input_float(3,self.tolerance);
            dbbgm_batch.set_input_string(4,self.interp_functor);
            dbbgm_batch.set_input_string(5,self.data_path);
            print dbbgm_batch.run_process();
            out_image=dbvalue(0,"")
            (out_image.id,out_image.type)=dbbgm_batch.commit_output(0)
            saveImg(out_image,self.output_path+frameSuffix(index,3)+".tiff")   

class measureProb(multiprocessing.Process):  
    def __init__(self,wavelet,test_image,attribute,tolerance,interp_functor,data_path,output_path,index):
        multiprocessing.Process.__init__(self)
        self.wavelet=wavelet;
        self.test_image=test_image;
        self.attribute=attribute;
        self.tolerance=tolerance;
        self.interp_functor=interp_functor;
        self.data_path=data_path;
        self.output_path=output_path;
        self.index=index
        self.done=0;
   
    def run(self):
        dbbgm_batch.init_process("bbgmMeasureWvLookupProcess");
        dbbgm_batch.set_input_from_db(0,self.wavelet);
        dbbgm_batch.set_input_from_db(1,self.test_image);
        dbbgm_batch.set_input_string(2,self.attribute);
        dbbgm_batch.set_input_float(3,self.tolerance);
        dbbgm_batch.set_input_string(4,self.interp_functor);
        dbbgm_batch.set_input_string(5,self.data_path);
        print dbbgm_batch.run_process();
        out_image=dbvalue(0,"")
        (out_image.id,out_image.type)=dbbgm_batch.commit_output(0)
        saveImg(out_image,self.output_path+frameSuffixWrite(self.index,300)+".tiff") 
        
