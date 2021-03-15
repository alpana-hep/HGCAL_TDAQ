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
gc.enable()
gc.collect()
M=50 ## total number of modules
#n= 1000000 ## maximum length of arrays
## input aruguments
min_ = int(sys.argv[1]) ##how much length of the random gaussian array has to be taken is decided by min and max argu
max_ = int(sys.argv[2])
# luv_fname=sys.argv[3] ## root file that contains layer, type u and v information
# RG_fname=sys.argv[4] ## root file containing arraysof random gaussian numbers  as branches of tree
# Orig_hits_fname=sys.argv[5] ## MC simulated root file to calculate covariance matrix'A'
out_fname = sys.argv[3] ## output file will contain similar 5k arrays satisfying X = A.R

fout = ROOT.TFile(out_fname, 'RECREATE')
## output tree ###
tree = ROOT.TTree('tree', 'tree')

### saving layer, u,v information                                                                                              
events = uproot3.open("./luv_tree.root")["Eventtree"]
layer = events.array("layer")
u=events.array("U")
v=events.array("V")
typee= events.array("type")
##reading montecarlo simulated file
print('readin MC file')
Events=uproot3.open("./../datapackets/updatedNtupleTree_DataPacketDec20.root")["EventTree"]
Rg_events = uproot3.open("./../condor_jobs/condor_output/temp_submit/random_numbers_Ndist_00_01.root")["tree"]
#events.show()
orig_modules_arrays=[] ##list to hold module wise arrays
RG_arrays=[]
mycache = {}
mycache1 = {}
for ib in range(M):
     #a=np.empty(60000,1)
     name='%i_%i_%i_%i' %(layer[ib],typee[ib],u[ib],v[ib])
     a=Events.array("Module_%s" %name,cache= mycache)
     print(a.dtype)
     orig_modules_arrays.append(a)
     b=Rg_events.array("Module_%s" %name,cache=mycache1)
     RG_arrays.append(b[min_:max_])
mycache.clear()
mycache1.clear()

np_orig_modules_arrays = np.array(orig_modules_arrays, dtype=int16)
print(np_orig_modules_arrays.nbytes)
corr1=np.corrcoef(np_orig_modules_arrays)
np_RG_arrays = np.array(RG_arrays,dtype=float32)
print(np_orig_modules_arrays.nbytes)
#print(corr1.type)
#sys.exit()
#del np_orig_modules_arrays

L = la.cholesky(corr1, lower=True)
#corr1=0
#del corr1
## matrix multiplications                                                                                                                                                             
X=np.matmul(L,np_RG_arrays)
#L=0
#del L
#print(gc.garbage)
for im in range(M):
     name='%i_%i_%i_%i' %(layer[im],typee[im],u[im],v[im])
     np_X = np.array(X[im],dtype =[('Module_%s' %name, np.float32)])
     
     array2tree(np_X,tree=tree)

fout.cd()
tree.Write()
fout.Close()
# ### reading random gaussian arrays ####
# Rg_events = uproot3.open("./../condor_jobs/condor_output/temp_submit/random_numbers_Ndist_00_01.root")["tree"]
# #events.show()
# print('reading RG file')
# RG_arrays=[]
# for ib in range(M):
#      name='%i_%i_%i_%i' %(layer[ib],typee[ib],u[ib],v[ib])
#      b=Rg_events.array("Module_%s" %name)
#      RG_arrays.append(b[min_:max_])
#      #print(len(b[min_:max_]))
# ## selecting only sub-length of RG_arrays defined by min and max
# np_RG_arrays = np.array(RG_arrays)
# # np_RG_arrays_sub = np_RG_arrays[:,min_:max_]

##calculate correlation matrix
#corr1=np.corrcoef(np_orig_modules_arrays)
###lower decomposition part of correlation matrix                                                                              
