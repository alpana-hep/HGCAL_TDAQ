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

M=5066 ## total number of modules                                                                                              
n= 1000000 ## maximum length of arrays                                                                                         
## input aruguments
infname1=sys.argv[1]
infname2=sys.argv[2]

out_fname = sys.argv[3] ## output file will contain similar 5k arrays saved after inverse qt                                        
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
print('readin after fit hits file')
Events=uproot3.open(infname1)["tree"]
corrX_events = uproot3.open(infname2)["tree"]
# Events=uproot3.open("./../condor_jobs/condor_output/temp_submit/datapackets_afterfit_1M_00_01.root")["tree"]
# corrX_events = uproot3.open("./../condor_jobs/condor_output/temp_submit/run01/matmulti_0to1M.root")["tree"]

#sys.exit()
mycache={}
mycache1={}
## perform qt on afit arrays and inv qt on corrX arrays
qt= QuantileTransformer(n_quantiles=100000, output_distribution='normal', random_state=0,subsample = 1000000)
count=0
for im in range(M):

     name='%i_%i_%i_%i' %(layer[im],typee[im],u[im],v[im])
     b=Events.lazyarray("Module_%s" %name,cache=mycache)
     Nhits_np= np.array(b)
     Nhits_np=Nhits_np.reshape(-1,1)
     X_trans_qt1 = qt.fit(Nhits_np).transform(Nhits_np)
     count+=1
     a=corrX_events.lazyarray("Module_%s" %name,cache=mycache1)
     corrX =np.array(a)
     corrX=corrX.reshape(-1,1)
     X_inv_gauss_qt1= qt.inverse_transform(corrX)
     X_inv_gauss_qt1 = X_inv_gauss_qt1.astype('int64')
     final_hits=np.array(X_inv_gauss_qt1,dtype=[('Module_%s' %name, np.int64)])
     array2tree(final_hits,tree=tree)
     if(im%100==0):
          print(im)
print(count)


fout.cd()
tree.Write()
fout.Close()
