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
from numpy import inf
from numpy.random import seed
from numpy.random import randn
                                                                                                                                                                         
layer=[]
u=[]
v=[]
typee=[]
nCells=[]
nHalfHgcrocs=[]
nMaxWords=[]
data = np.loadtxt("./fit_function_parameters_n10_updatedntuples_v2.txt") ## to get the luvtype information for each modules
for im in range(4851):
    layer.append(int(data[im][1]))
    u.append(int(data[im][2]))
    v.append(int(data[im][3]))
    typee.append(int(data[im][4]))
    nCells.append(int(data[im][5]))
    nHalfHgcrocs.append(int(data[im][6]))
    nMaxWords.append(int(data[im][7]))

# reading input array files
Events1=uproot3.open("./Arraytotree_n10_unmaksed_newtuple.root")["EventTree"]
Events2=uproot3.open("./Arraytotree_n20_unmaksed_newtuple.root")["EventTree"]
Events3=uproot3.open("./Arraytotree_n10_unmaksed_newtuple.root")["EventTree"]

mycache = {}
orig_modules_arrays=np.empty((14553,119700),dtype='int32')
count=0
count1=0
count2=0
count3=0
count4=0
for ib in range(0,14553,3):
        name='%i_%i_%i_%i' %(layer[count],typee[count],u[count],v[count])
        a=Events1.lazyarray("Module_%s" %name,cache= mycache)
        count+=1
            
        b=Events2.lazyarray("Module_%s" %name,cache= mycache)
        if(np.std(np.array(b))==0):
            print(name)
            b=randn(119700)

        c=Events3.lazyarray("Module_%s" %name,cache= mycache)
        orig_modules_arrays[ib]=a
        orig_modules_arrays[ib+1]=b
        orig_modules_arrays[ib+2]=c
        
print(count1)
corr1 = np.cov(orig_modules_arrays)
print(np.linalg.eig(corr1))
# corr1[corr1 == -inf] = 0.1
# corr1[corr1<=0]= 0.01
# corr1[~np.isfinite(corr1)] = 0.1

#corr1[np.linalg.eig(corr1)<0]=abs(np.linalg.eig(corr1))
#L= np.linalg.cholesky(
#L=la.cholesky(corr1, lower=True)

# print(corr1)
# print(L)
np.savetxt("v1_correlationMatrix_15kby15k_LatestNtuples.txt",L)
