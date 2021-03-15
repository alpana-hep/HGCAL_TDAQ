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

M=2 ## total number of modules                                                                                              
n= 1000000 ## maximum length of arrays                                                                                         
## input aruguments                                                                                                            
min_ = int(sys.argv[1]) ##how many modules needs to be processed at a time and it is decided by min and max         
max_ = int(sys.argv[2])
# luv_fname=sys.argv[3] ## root file that contains layer, type u and v information                                              
# corrX_fname=sys.argv[4] ## root file containing arrays of correlated random gaussian numbers  as branches of tree                             
# Afit_hits_fname=sys.argv[5] ## arrays for 5k modules generated after fitting a function ot original correlated modules
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
Events=uproot3.open("./../condor_jobs/condor_output/temp_submit/datapackets_afterfit_1M_00_01.root")["tree"]
# Afit_modules_arrays=[] ##list to hold module wise arrays                                                                       
# for ib in range(M):
#      name='%i_%i_%i_%i' %(layer[ib],typee[ib],u[ib],v[ib])
#      a=Events.array("Module_%s" %name)
#      Afit_modules_arrays.append(a)

# np_Afit_arrays=np.array(Afit_modules_arrays)
corrX_events = uproot3.open("./../condor_jobs/condor_output/temp_submit/run01/matmulti_0to1M.root")["tree"]
#print('reading corrX file')
# corrX_arrays=[]
# for ib in range(M):
#      name='%i_%i_%i_%i' %(layer[ib],typee[ib],u[ib],v[ib])
#      b=corrX_events.array("Module_%s" %name)
#      corrX_arrays.append(b)

# np_corrX_arrays=np.array(corrX_arrays)

#sys.exit()
mycache={}
mycache1={}
## perform qt on afit arrays and inv qt on corrX arrays
qt= QuantileTransformer(n_quantiles=100000, output_distribution='normal', random_state=0,subsample = 1000000)
count=0
for im in range(M):

     name='%i_%i_%i_%i' %(layer[im],typee[im],u[im],v[im])
     b=Events.lazyarray("Module_%s" %name,cache=mycache)
     Nhits_np= np.array(b[min_:max_])
     # if(typee[im]==0):
     #      Nhits_np=Nhits_np[Nhits_np<=432]
     #      Nhits_np=Nhits_np.reshape(-1,1)
     #      X_trans_qt1 = qt.fit(Nhits_np).transform(Nhits_np)
     #      count+=1
     # elif(typee[im]==1):
     #      Nhits_np=Nhits_np[Nhits_np<=192]
     #      Nhits_np=Nhits_np.reshape(-1,1)
     #      X_trans_qt1 = qt.fit(Nhits_np).transform(Nhits_np)
     #      count+=1
     # else:
          
     #print(len(Nhits_np))
     Nhits_np=Nhits_np.reshape(-1,1)
     X_trans_qt1 = qt.fit(Nhits_np).transform(Nhits_np)
     count+=1
     a=corrX_events.lazyarray("Module_%s" %name,cache=mycache1)
     corrX =np.array(a[min_:max_])
     corrX=corrX.reshape(-1,1)
     X_inv_gauss_qt1= qt.inverse_transform(corrX)
     final_hits=np.array(X_inv_gauss_qt1,dtype=[('Module_%s' %name, np.int64)])
     array2tree(final_hits,tree=tree)
     if(im%100==0):
          print(im)
print(count)


fout.cd()
tree.Write()
fout.Close()
