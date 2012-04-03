'''
Created on Nov 1, 2010

@author: octi
'''
import dbbgm_batch
import math
class dbvalue:
    def __init__(self, index, type):
        self.id = index    # unsigned integer
        self.type = type   # string


import math

def frameSuffixWrite(index,maxFrame):
    if (index==0):
        digits=1;
    else:
        digits=int(math.log10(index))+1;
    max_digits=int(math.log10(maxFrame))+1;
    diff=max_digits-digits;
    prefix="";
    for i in range(diff):
        prefix+="0";
    return prefix+str(index)
def frameSuffix(index,max_digits): 
    if (index==0):
        digits=1;
    else:    
        digits=int(math.log10(index))+1;
    diff=max_digits-digits;
    prefix="";
    for i in range(diff):
        prefix+="0";
    return prefix+str(index)       
def GUI(model,inv_model,fwd_model,pMap):
    dbbgm_batch.init_process("bbgmInvokeGUIProcess");
    dbbgm_batch.set_input_from_db(0,model);
    dbbgm_batch.set_input_from_db(1,inv_model);
    dbbgm_batch.set_input_from_db(2,fwd_model);
    dbbgm_batch.set_input_from_db(3,pMap);
    print dbbgm_batch.run_process();
    return []

def displayImg(model,type,component,scale):
    Image=dbvalue(0,"");
    dbbgm_batch.init_process("bbgmDisplayDistImageProcess")
    dbbgm_batch.set_input_from_db(0,model);
    dbbgm_batch.set_input_string(1,type);
    dbbgm_batch.set_input_int(2,component);
    dbbgm_batch.set_input_bool(3,scale);
    print   dbbgm_batch.run_process();
    (Image.id,Image.type)=dbbgm_batch.commit_output(0);
    return Image

def saveImg(image,path):
    dbbgm_batch.init_process("vilSaveImageViewProcess");
    dbbgm_batch.set_input_from_db(0,image);
    dbbgm_batch.set_input_string(1,path);
    dbbgm_batch.run_process();
    return []

def wvXform(image_string,image,wv_type,level,nplanes):
    Wavelet=dbvalue(0,"");
    dbbgm_batch.init_process("bbgmWaveletXformProcess");
    dbbgm_batch.set_input_string(0,image_string);
    dbbgm_batch.set_input_int(1,wv_type);
    dbbgm_batch.set_input_int(2,level);
    dbbgm_batch.set_input_from_db(3,image);
    dbbgm_batch.set_input_int(4,nplanes);
    print   dbbgm_batch.run_process();
    (Wavelet.id,Wavelet.type)=dbbgm_batch.commit_output(0);
    return Wavelet


def getSubband(image_string,nplanes,subband_type,depth,wavelet):
    subband=dbvalue(0,"");
    dbbgm_batch.init_process("bbgmWaveletUtilsProcess");
    dbbgm_batch.set_input_string(0,image_string);
    dbbgm_batch.set_input_int(1,nplanes);
    dbbgm_batch.set_input_string(2,subband_type);
    dbbgm_batch.set_input_int(3,depth);
    dbbgm_batch.set_input_from_db(4,wavelet);
    print   dbbgm_batch.run_process();
    (subband.id,subband.type)=dbbgm_batch.commit_output(0);    
    return subband

def updateImageStream(path,w_size,init_var,minimum_stdev,start_frame,end_frame):
    dbbgm_batch.init_process("vidlOpenIstreamProcess")
    print dbbgm_batch.set_input_string(0, path+"*.tiff");
    print dbbgm_batch.run_process();
    stream = dbvalue(0,"");
    model = dbvalue(0,"");
    (stream.id, stream.type) = dbbgm_batch.commit_output(0);
    dbbgm_batch.init_process("bbgmUpdateDistImageStreamProcess")
    print dbbgm_batch.set_input_from_db(1, stream); # input stream
    print dbbgm_batch.set_input_int(2, 3); # number of mixture components
    print dbbgm_batch.set_input_int(3, w_size); # window size
    print dbbgm_batch.set_input_float(4, init_var); # initial variance
    print dbbgm_batch.set_input_float(5, 3.0); # g_thresh
    print dbbgm_batch.set_input_float(6, minimum_stdev);# minimum standard deviation
    print dbbgm_batch.set_input_int(7, start_frame);# start frame
    print dbbgm_batch.set_input_int(8, end_frame);# end frame -1 == do all
    print dbbgm_batch.process_init();
    print dbbgm_batch.run_process();
    (model.id, model.type) = dbbgm_batch.commit_output(0);
    print dbbgm_batch.remove_data(stream.id);
    return model

def saveModel(path,model):
    dbbgm_batch.init_process("bbgmSaveImageOfProcess");
    dbbgm_batch.set_input_string(0,path);
    dbbgm_batch.set_input_from_db(1, model);
    print dbbgm_batch.run_process();
    return[]
    
def saveWavelet(path,wavelet):
    dbbgm_batch.init_process("bbgmSaveWaveletProcess");
    dbbgm_batch.set_input_string(0,path);
    dbbgm_batch.set_input_from_db(1, wavelet);
    print dbbgm_batch.run_process();
    return[]
    
def loadModel(path):
    model = dbvalue(0,"");
    dbbgm_batch.init_process("bbgmLoadImageOfProcess");
    dbbgm_batch.set_input_string(0,path);
    print dbbgm_batch.run_process();
    (model.id, model.type) = dbbgm_batch.commit_output(0);
    return model

def openImage(path):
    image=dbvalue(0,"");
    dbbgm_batch.init_process("vilLoadImageViewProcess");
    dbbgm_batch.set_input_string(0,path);
    dbbgm_batch.run_process();
    (image.id, image.type) = dbbgm_batch.commit_output(0);
    ni=dbbgm_batch.commit_output(1);
    nj=dbbgm_batch.commit_output(2);
    return [image,ni,nj]

def openImageAtTarget(path,index):
    image=dbvalue(0,"");
    dbbgm_batch.init_process("vilLoadImageViewProcess");
    dbbgm_batch.set_input_string(0,path);
    dbbgm_batch.run_process();
    (image.id, image.type) = dbbgm_batch.commit_output(0,index);
    ni=dbbgm_batch.commit_output(1);
    nj=dbbgm_batch.commit_output(2);
    return [image,ni,nj]

def openImageWithDb(path,manager):
    image=dbvalue(0,"");
    dbbgm_batch.init_process_with_db("vilLoadImageViewProcess",manager);
    dbbgm_batch.set_input_string(0,path);
    dbbgm_batch.run_process();
    (image.id, image.type) = dbbgm_batch.commit_output(0);
    ni=dbbgm_batch.commit_output(1);
    nj=dbbgm_batch.commit_output(2);
    return [image,ni,nj]

def loadWavelet(path):
    wavelet=dbvalue(0,"");
    dbbgm_batch.init_process("bbgmLoadWaveletProcess");
    dbbgm_batch.set_input_string(0,path);
    print dbbgm_batch.run_process();
    (wavelet.id, wavelet.type) = dbbgm_batch.commit_output(0);
    return wavelet

def measureWvLookup(wavelet,test_image,attribute,tolerance,interp_functor,data_path):
    image=dbvalue(0,"");
    dbbgm_batch.init_process("bbgmMeasureWvLookupProcess");
    dbbgm_batch.set_input_from_db(0,wavelet);
    dbbgm_batch.set_input_from_db(1,test_image);
    dbbgm_batch.set_input_string(2,attribute);
    dbbgm_batch.set_input_float(3,tolerance);
    dbbgm_batch.set_input_string(4,interp_functor);
    dbbgm_batch.set_input_string(5,data_path);
    print dbbgm_batch.run_process();
    (image.id,image.type)=dbbgm_batch.commit_output(0); 
    return image

