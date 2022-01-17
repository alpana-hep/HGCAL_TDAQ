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
#import covariance_module_v1
import readRandGaus


gc.enable()
#gc.collect()
M=15198 ## total number of modules

layer=[]
u=[]
v=[]
typee=[]
nCells=[]
nHalfHgcrocs=[]
nMaxWords=[]

data = np.loadtxt("./module_info_updated_01032021.txt")
for im in range(4851):
    layer.append(int(data[im][1]))
    u.append(int(data[im][3]))
    v.append(int(data[im][4]))
    typee.append(int(data[im][2]))
    nCells.append(int(data[im][5]))
    nHalfHgcrocs.append(int(data[im][6]))
    nMaxWords.append(int(data[im][7]))


## input aruguments
min_ = int(sys.argv[1]) ##how much length of the random gaussian array has to be taken is decided by min and max argu
max_ = int(sys.argv[2])
out_fname = sys.argv[4] ## output file will contain similar 5k arrays satisfying X = A.R
fin = sys.argv[3]
fout = ROOT.TFile(out_fname, 'RECREATE')
## output tree ###
tree = ROOT.TTree('tree', 'tree')

X = readRandGaus.readRandGaus(min_,max_,fin)
#print(X)
count1=0
for im in range(0,14553,3):
    #if(im<5066):
    name='%i_%i_%i_%i' %(layer[count1],typee[count1],u[count1],v[count1])
    np_X_n10 = np.array(X[im],dtype =[('n10_Module_%s' %name, np.float32)])
    np_X_n20 = np.array(X[im+1],dtype =[('n20_Module_%s' %name, np.float32)])
    np_X_n30 = np.array(X[im+2],dtype =[('n30_Module_%s' %name, np.float32)])
    array2tree(np_X_n10,tree=tree)
    array2tree(np_X_n20,tree=tree)
    array2tree(np_X_n30,tree=tree)
    if(im%100==0):
        print(im)
    count1+=1
#gc.enable()
gc.collect()

fout.cd()
tree.Write()
fout.Close()
