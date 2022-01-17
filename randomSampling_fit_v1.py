# from io import StringIO
# from StringIO import StringIO
import ROOT
from ROOT import TTree, TBranch, TFile, TH1F
import numpy as np
import itertools
from root_numpy import random_sample, array2tree, array2root
import uproot
import sys 
#sys.exit()
min_ = int(sys.argv[1]) ##how many modules needs to be processed at a time and it is decided by min and max                                                                                               
max_ = int(sys.argv[2])

## reading module_info file
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

## reading luvts file and storing the information
#### reading param_file                                                                                                        
layer_n10=[]
u_n10=[]
v_n10=[]
typee_n10=[]
constant1_n10=[]
constant2_n10=[]
constant3_n10=[]
mean_G_n10=[]
sigma_G_n10=[]
mean_P_n10=[]
mean_L_n10=[]
sigma_L_n10=[]
shape_n10=[]
data_n10 = np.loadtxt("./fit_function_parameters_n10_updatedntuples_v2.txt")
for im in range(4851):

    layer_n10.append(int(data_n10[im][1]))
    u_n10.append(int(data_n10[im][2]))
    v_n10.append(int(data_n10[im][3]))
    typee_n10.append(int(data_n10[im][4]))
    constant1_n10.append(data_n10[im][5])
    mean_G_n10.append(data_n10[im][6])
    sigma_G_n10.append(data_n10[im][7])
    constant2_n10.append(data_n10[im][8])
    mean_P_n10.append(data_n10[im][9])
    constant3_n10.append(data_n10[im][10])
    mean_L_n10.append(data_n10[im][11])
    sigma_L_n10.append(data_n10[im][12])

layer_n20=[]
u_n20=[]
v_n20=[]
typee_n20=[]
constant1_n20=[]
constant2_n20=[]
constant3_n20=[]
mean_G_n20=[]
sigma_G_n20=[]
mean_P_n20=[]
mean_L_n20=[]
sigma_L_n20=[]
shape_n20=[]
data_n20 = np.loadtxt("./fit_function_parameters_n20_updatedntuples_v2.txt")
for im in range(4851):

    layer_n20.append(int(data_n20[im][1]))
    u_n20.append(int(data_n20[im][2]))
    v_n20.append(int(data_n20[im][3]))
    typee_n20.append(int(data_n20[im][4]))
    constant1_n20.append(data_n20[im][5])
    mean_G_n20.append(data_n20[im][6])
    sigma_G_n20.append(data_n20[im][7])
    constant2_n20.append(data_n20[im][8])
    mean_P_n20.append(data_n20[im][9])
    constant3_n20.append(data_n20[im][10])
    mean_L_n20.append(data_n20[im][11])
    sigma_L_n20.append(data_n20[im][12])

layer_n30=[]
u_n30=[]
v_n30=[]
typee_n30=[]
constant1_n30=[]
constant2_n30=[]
constant2_n30=[]
constant3_n30=[]
mean_G_n30=[]
sigma_G_n30=[]
mean_P_n30=[]
mean_L_n30=[]
sigma_L_n30=[]
shape_n30=[]
data_n30 = np.loadtxt("./fit_function_parameters_n30_updatedntuples_v2.txt")
for im in range(4851):

    layer_n30.append(int(data_n30[im][1]))
    u_n30.append(int(data_n30[im][2]))
    v_n30.append(int(data_n30[im][3]))
    typee_n30.append(int(data_n30[im][4]))
    constant1_n30.append(data_n30[im][5])
    mean_G_n30.append(data_n30[im][6])
    sigma_G_n30.append(data_n30[im][7])
    constant2_n30.append(data_n30[im][8])
    mean_P_n30.append(data_n30[im][9])
    constant3_n30.append(data_n30[im][10])
    mean_L_n30.append(data_n30[im][11])
    sigma_L_n30.append(data_n30[im][12])
    
out_fname = sys.argv[3] ## output file will contain similar 5k arrays saved after inverse qt                                                                                                              
fout = ROOT.TFile(out_fname, 'RECREATE')
# hist = ROOT.TH1F("hist","average n10 in CMSSW ntuple",500,0,500);

#fout = ROOT.TFile('RandomSample_from_fit_%dto%d_Latestntuples.root' %(min_,max_), 'RECREATE')
tree = ROOT.TTree('tree', 'tree')
M=4851
n=1000000
# nhits10=[]
# nhits20=[]
# nhits30=[]
### ## sampling random numbers from the fit
gRandom=ROOT.TRandom3()
for im in range(4851):
    name='%i_%i_%i_%i' %(layer_n10[im],typee_n10[im],u_n10[im],v_n10[im])
    print(name)#, layer_n30[im],typee_n30[im],u_n30[im],v_n30[im])
    print(constant1_n10[im],mean_G_n10[im],sigma_G_n10[im],constant2_n10[im],mean_P_n10[im],constant3_n10[im],mean_L_n10[im],sigma_L_n10[im])
    fit_func_n10= ROOT.TF1("fit_func_n10","[0]*TMath::Gaus(x,[1],[2])+[3]*TMath::Poisson(x,[4])+[5]*TMath::Landau(x,[6],[7])")
    fit_func_n10.FixParameter(0,constant1_n10[im])
    fit_func_n10.FixParameter(1,mean_G_n10[im])
    fit_func_n10.FixParameter(2,sigma_G_n10[im])
    fit_func_n10.FixParameter(3,constant2_n10[im])
    fit_func_n10.FixParameter(4,mean_P_n10[im])
    fit_func_n10.FixParameter(5,0)#constant3_n10[im])
    fit_func_n10.FixParameter(6,mean_L_n10[im])
    fit_func_n10.FixParameter(7,sigma_L_n10[im])
    f10=ROOT.TF1(fit_func_n10.Clone())
    #f10.SetRange(0,400)
    
    # nhitss_n10= np.array(random_sample(f10,n),dtype=[('n10_Module_%s' %name, np.float32)])
    # array2tree(nhitss_n10,tree=tree)

    fit_func_n20= ROOT.TF1("fit_func_n20","[0]*TMath::Gaus(x,[1],[2])+[3]*TMath::Poisson(x,[4])+[5]*TMath::Landau(x,[6],[7])")
    fit_func_n20.FixParameter(0,constant1_n20[im])
    fit_func_n20.FixParameter(1,mean_G_n20[im])
    fit_func_n20.FixParameter(2,sigma_G_n20[im])
    fit_func_n20.FixParameter(3,constant2_n20[im])
    fit_func_n20.FixParameter(4,mean_P_n20[im])
    fit_func_n20.FixParameter(5,constant3_n20[im])
    fit_func_n20.FixParameter(6,mean_L_n20[im])
    fit_func_n20.FixParameter(7,sigma_L_n20[im])
    f20=ROOT.TF1(fit_func_n20.Clone())
    #f20.SetRange(0,400)
    # nhitss_n20= np.array(random_sample(f20,n),dtype=[('n20_Module_%s' %name, np.float32)])
    # array2tree(nhitss_n20,tree=tree)

    fit_func_n30= ROOT.TF1("fit_func_n30","[0]*TMath::Gaus(x,[1],[2])+[3]*TMath::Poisson(x,[4])+[5]*TMath::Landau(x,[6],[7])")
    fit_func_n30.FixParameter(0,constant1_n30[im])
    fit_func_n30.FixParameter(1,mean_G_n30[im])
    fit_func_n30.FixParameter(2,sigma_G_n30[im])
    fit_func_n30.FixParameter(3,constant2_n30[im])
    fit_func_n30.FixParameter(4,mean_P_n30[im])
    fit_func_n30.FixParameter(5,constant3_n30[im])
    fit_func_n30.FixParameter(6,mean_L_n30[im])
    fit_func_n30.FixParameter(7,sigma_L_n30[im])
    f30=ROOT.TF1(fit_func_n30.Clone())
    # if(nCells[im]!=0):
    f10.SetRange(0,nCells[im]);
    f20.SetRange(0,nCells[im]);
    f30.SetRange(0,nCells[im]);
    # else:
    #     print(name)
    #     f10.SetRange(0,50);
    #     f20.SetRange(0,50);
    #     f30.SetRange(0,50);
    #print(name, layer_n30[im],typee_n30[im],u_n30[im],v_n30[im])
    #print(constant1_n30[im],mean_G_n30[im],sigma_G_n30[im],constant2_n30[im],mean_P_n30[im],constant3_n30[im],mean_L_n30[im],sigma_L_n30[im])
    nhits10=random_sample(f10,n,seed=0)
    nhits20=random_sample(f20,n,seed=0)
    nhits30=random_sample(f30,n,seed=0)
    # for i in range(min_,max_):
    #     #gRandom.SetSeed(i)
    #     nhits10.append(f10.GetRandom(0,nCells[im]))
    #     #hist.Fill(f10.GetRandom(0,nCells[im]))
    #     nhits20.append(f20.GetRandom(0,nCells[im]))
    #     nhits30.append(f30.GetRandom(0,nCells[im]))
    nhitss_n10= np.array(nhits10,dtype=[('n10_Module_%s' %name, np.float32)])
    # nhitss_n20= np.array(nhits20)
    # nhitss_n30= np.array(nhits30)
    #print(np.average(nhitss_n10))#, np.average(nhitss_n20),np.average(nhitss_n30),name)
    #print(nCells[im])
    
    array2tree(nhitss_n10,tree=tree)
    nhitss_n20= np.array(nhits20,dtype=[('n20_Module_%s' %name, np.float32)])
    array2tree(nhitss_n20,tree=tree)
    nhitss_n30= np.array(nhits30,dtype=[('n30_Module_%s' %name, np.float32)])
    array2tree(nhitss_n30,tree=tree)
    # nhits10=[]
    # nhits20=[]
    # nhits30=[]
    #f30.SetRange(0,400)
    # nhitss_n30= np.array(random_sample(f30,n),dtype=[('n30_Module_%s' %name, np.float32)])
    # array2tree(nhitss_n30,tree=tree)
    # for i in range(n):
    #     nhitss_n30 = 
    if(im%100==0):
        print(im)

fout.cd()
#hist.Write()
#f10.Write()
tree.Write() 
fout.Close()
