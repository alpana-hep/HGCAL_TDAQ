#import numpy as np
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
from sklearn.preprocessing import QuantileTransformer
from numpy.random import seed
from numpy.random import randn
from rootpy.tree import Tree, TreeModel, FloatCol, IntCol, ULongCol
from rootpy import stl
min_ = int(sys.argv[1])
seed_=int(sys.argv[2])
out_fname=sys.argv[3]

fout = ROOT.TFile(out_fname, 'RECREATE')

tree = ROOT.TTree('tree', 'tree')

layer_M=[]
u_M=[]
v_M=[]
typee_M=[]
nCells=[]
nHalfHgcrocs=[]
nMaxWords=[]
nMinWords=[]
f = open("./module_info_updated_01032021.txt", "r")
 
for line in f:
    newline= line.replace("\t"," ")

    data=newline.split(" ")
 
    layer_M.append(int(data[1]))
    u_M.append(int(data[3]))
    v_M.append(int(data[4]))
    typee_M.append(int(data[2]))
    nCells.append(int(data[5]))
    nHalfHgcrocs.append(int(data[6]))
    nMaxWords.append(int(data[7]))
    nMinWords.append(int(data[8]))

random_number=[]
random_list=[]
n = 1000000
for im in range(5066):
     seed(im*seed_+im)
     random_number=randn(n)
     name='%i_%i_%i_%i' %(layer_M[im],typee_M[im],u_M[im],v_M[im])

     nhitss= np.array(random_number,dtype=[('Module_%s' %name, np.float32)])

     array2tree(nhitss,tree=tree)


fout.cd()
tree.Write()
fout.Close()

     #print(random_number)
     #random_list.append(random_number)
# print('mean',np.mean(random_list[1]))
# print('std',np.std(random_list[1]))

#print(len(random_number))                                                                                                      
#print(len(random_list))                                                                                                        
#random_list_np= np.array(random_list) 
