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
import covariance_module
import readRandGaus


gc.enable()
#gc.collect()
M=5066 ## total number of modules

events = uproot3.open("./luv_tree.root")["Eventtree"]
layer = events.array("layer")
u=events.array("U")
v=events.array("V")
typee= events.array("type")

## input aruguments
min_ = int(sys.argv[1]) ##how much length of the random gaussian array has to be taken is decided by min and max argu
max_ = int(sys.argv[2])
out_fname = sys.argv[3] ## output file will contain similar 5k arrays satisfying X = A.R

fout = ROOT.TFile(out_fname, 'RECREATE')
## output tree ###
tree = ROOT.TTree('tree', 'tree')

X = readRandGaus.readRandGaus(min_,max_)


for im in range(M):
     
     name='%i_%i_%i_%i' %(layer[im],typee[im],u[im],v[im])
     np_X = np.array(X[im],dtype =[('Module_%s' %name, np.float32)])
     
     array2tree(np_X,tree=tree)
#gc.enable()
gc.collect()

fout.cd()
tree.Write()
fout.Close()
