import gc                                                                                 
import sys                                                                                 
import ROOT                                                                                
import scipy.linalg as la                                                                  
import numpy as np                                                                         
from random import seed                                                                    
from random import random                                                                  
from random import gauss                                                                   
import root_numpy                                                                          
from root_numpy import random_sample, array2tree, array2root                               
import uproot3
import covariance_module_v1
def readRandGaus(min_,max_):
    gc.enable()
    gc.collect()

    mycache1 = {}                                                                         
    L= covariance_module_v1.covariance_()                                                                      
    Rg_events = uproot3.open("./../condor_jobs/condor_output/temp_submit/random_numbers_Ndist_08_09.root")["tree"]                                                    
    events = uproot3.open("./luv_tree.root")["Eventtree"]                                 
    layer = events.array("layer")                                                         
    u=events.array("U")                                                                   
    v=events.array("V")                                                                   
    typee= events.array("type")                                                           
    RG_arrays=np.empty((5066,50000),dtype='int32')

    for ib in range(5066):                                                                   
        name='%i_%i_%i_%i' %(layer[ib],typee[ib],u[ib],v[ib])                           
        b=Rg_events.lazyarray("Module_%s" %name,cache=mycache1)                              
        RG_arrays[ib]=b[min_:max_]
    #np_RG_arrays = np.array(RG_arrays,dtype='float32')
    mycache1.clear()
    X=np.matmul(L,RG_arrays)
    return X
