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


def covariance_():
    gc.enable()
    gc.collect()

    Events=uproot3.open("./../datapackets/updatedNtupleTree_DataPacketDec20.root")["EventTree"]
    events = uproot3.open("./luv_tree.root")["Eventtree"]
    layer = events.array("layer")                                                         
    u=events.array("U")                                                                   
    v=events.array("V")                                                                   
    typee= events.array("type")                                                           
    mycache = {}                                                                          
    orig_modules_arrays=np.empty((5066,60000),dtype='int32')                                                         
    for ib in range(5066):                                                                   
        name='%i_%i_%i_%i' %(layer[ib],typee[ib],u[ib],v[ib])                            
        a=Events.lazyarray("Module_%s" %name,cache= mycache)                                
        orig_modules_arrays[ib]=a
    #np_orig_modules_arrays = np.array(orig_modules_arrays,dtype='int16')                  
    mycache.clear()                                                                       
    corr1=np.corrcoef(orig_modules_arrays)                                             
    L = la.cholesky(corr1, lower=True)                                                    
    return L                                                  
