import sys
import ROOT
import numpy as np
import root_numpy
from root_numpy import array2hist
import uproot3
M=102 ## total number of modules                                                                                               
n= 1000000 ## maximum length of arrays
### reading l,u,v type info ####
events = uproot3.open("./datapackets/luv_tree.root")["Eventtree"]
layer = events.array("layer")
u=events.array("U")
v=events.array("V")
typee= events.array("type")

### booking the histograms  #####
hist=[]
for i_hist in range(M):
    name1='with_luvt_as_%i_%i_%i_%i' %(layer[i_hist],u[i_hist],v[i_hist],typee[i_hist])
    hist.append(ROOT.TH1F('invQt_module_%s' % name1, '', 500, 0, 500))

Events=uproot3.open("./qt_invqt_temp_v1.root")["tree"]
mycache={}
invQTX_arrays=[] ##list to hold module wise arrays                                                                             
# for i in range(M):
#      name='%i_%i_%i_%i' %(layer[i],typee[i],u[i],v[i])
#      a=Events.array("Module_%s" %name, cache=mycache)
#      #resp1=ROOT.TH1F('invQt_module_%s' % name1, '', 500, 0, 500)
#      #array2hist(a, resp1)
#      invQTX_arrays.append(a)

print('...')
#np_invQTX_arrays=np.array(invQTX_arrays)
for im in range(M):
    name='%i_%i_%i_%i' %(layer[im],typee[im],u[im],v[im])
    a=Events.array("Module_%s" %name, cache=mycache)
    np_invQT_array=np.array(a)
    for xi in np_invQT_array:
        hist[im].Fill(xi)
    if(im%100==0):
        print(im)
fout= ROOT.TFile("hist_afterinvQT.root", 'RECREATE')
fout.cd()
for h in hist:
    h.Write()
fout.Close()

