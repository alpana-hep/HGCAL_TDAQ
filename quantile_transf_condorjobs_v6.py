import sys
import ROOT
import scipy.linalg as la
import numpy as np
from random import seed
from random import random
from random import gauss
from numpy import inf
import root_numpy
from root_numpy import random_sample, array2tree, array2root
import uproot3
from sklearn.preprocessing import QuantileTransformer
from numpy.random import seed
from numpy.random import randn
from rootpy.tree import Tree, TreeModel, FloatCol, IntCol, ULongCol
from rootpy import stl

M=4851 ## total number of modules                                                                                              
n= 1000000 ## maximum length of arrays                                                                                         
## input aruguments
infname1=sys.argv[1]
infname2=sys.argv[2]

out_fname = sys.argv[3] ## output file will contain similar 5k arrays saved after inverse qt                                        
fout = ROOT.TFile(out_fname, 'RECREATE')
## output tree ###                                                                                                             
tree = ROOT.TTree('tree', 'tree')
min_=int(sys.argv[4])
max_=int(sys.argv[5])
### saving layer, u,v information                                                                                              
# events = uproot3.open("./luv_tree.root")["Eventtree"]
# layer = events.array("layer")
# u=events.array("U")
# v=events.array("V")
# typee= events.array("type")
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
    
    temp10_v2=Events.lazyarray("n10_Module_%s" %name,cache=mycache)
    #temp10_v2=temp10_v1[min_:max_]
    Nhits_np_n10= np.array(temp10_v2)#[min_:max_])
    Nhits_np_n10=Nhits_np_n10.reshape(-1,1)
    #sys.exit()
    X_trans_qt_n10 = qt.fit(Nhits_np_n10).transform(Nhits_np_n10)
    count+=1                                                                                                                                                            
    a_n10=corrX_events.lazyarray("n10_Module_%s" %name,cache=mycache1)
    corrX_n10 =np.array(a_n10)#[min_:max_])
    corrX_n10=corrX_n10.reshape(-1,1)
    X_inv_gauss_qt_n10= qt.inverse_transform(corrX_n10)
    final_hits_n10=np.array(X_inv_gauss_qt_n10,dtype=[('n10_Module_%s' %name, np.int32)])
    array2tree(final_hits_n10,tree=tree)
    
    ##quantiletransformer on n20 hits                                                                                                             
    temp20_v2=Events.lazyarray("n20_Module_%s" %name,cache=mycache)
    Nhits_np_n20= np.array(temp20_v2)#[min_:max_])
    Nhits_np_n20[Nhits_np_n20 == -inf] = 0.1
    Nhits_np_n20[Nhits_np_n20 == inf] = 0.1
    Nhits_np_n20[~np.isfinite(Nhits_np_n20)]=0.1
    Nhits_np_n20=Nhits_np_n20.reshape(-1,1)                                                                                                                             
    X_trans_qt_n20 = qt.fit(Nhits_np_n20).transform(Nhits_np_n20)
    count+=1
    a_n20=corrX_events.lazyarray("n20_Module_%s" %name,cache=mycache1)
    corrX_n20 =np.array(a_n20)#[min_:max_])
    corrX_n20=corrX_n20.reshape(-1,1)
    X_inv_gauss_qt_n20= qt.inverse_transform(corrX_n20)
    final_hits_n20=np.array(X_inv_gauss_qt_n20,dtype=[('n20_Module_%s' %name, np.int32)])
    array2tree(final_hits_n20,tree=tree)

    #t# quantile transformation on n30                                                                                                                               
    temp30_v2=Events.lazyarray("n30_Module_%s" %name,cache=mycache)
    Nhits_np_n30= np.array(temp30_v2)#[min_:max_])
    Nhits_np_n30=Nhits_np_n30.reshape(-1,1)                                                                                                                             
    X_trans_qt_n30 = qt.fit(Nhits_np_n30).transform(Nhits_np_n30)
    count+=1
    a_n30=corrX_events.lazyarray("n30_Module_%s" %name,cache=mycache1)
    corrX_n30 =np.array(a_n30)#[min_:max_])
    corrX_n30=corrX_n30.reshape(-1,1)
    X_inv_gauss_qt_n30= qt.inverse_transform(corrX_n30)
    final_hits_n30=np.array(X_inv_gauss_qt_n30,dtype=[('n30_Module_%s' %name, np.int32)])
    array2tree(final_hits_n30,tree=tree)

    # b=Events.lazyarray("Module_%s" %name,cache=mycache)
    # Nhits_np= np.array(b)
    # Nhits_np=Nhits_np.reshape(-1,1)
    # X_trans_qt1 = qt.fit(Nhits_np).transform(Nhits_np)
    # count+=1
    # a=corrX_events.lazyarray("Module_%s" %name,cache=mycache1)
    # corrX =np.array(a)
    # corrX=corrX.reshape(-1,1)
    # X_inv_gauss_qt1= qt.inverse_transform(corrX)
    # X_inv_gauss_qt1 = X_inv_gauss_qt1.astype('int64')
    # final_hits=np.array(X_inv_gauss_qt1,dtype=[('Module_%s' %name, np.int64)])
    # array2tree(final_hits,tree=tree)
    if(im%100==0):
        print(im)
    #sys.exit()
print(count)


fout.cd()
tree.Write()
fout.Close()
