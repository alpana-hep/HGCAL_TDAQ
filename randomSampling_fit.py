#from io import StringIO
#from StringIO import StringIO
import ROOT
from ROOT import TTree, TBranch, TFile, TH1F
import numpy as np
import itertools
from root_numpy import random_sample, array2tree, array2root
#import uproot
import sys 
#sys.exit()
## reading luvts file and storing the information
## reading module_info file
min_ = int(sys.argv[1])
seed_=int(sys.argv[2])
out_fname=sys.argv[3]
layer_M=[]
u_M=[]
v_M=[]
typee_M=[]
nCells=[]
nHalfHgcrocs=[]
nMaxWords=[]
nMinWords=[]
f = open("./module_info_updated_01032021.txt", "r")
#data = np.loadtxt("./module_info_updated_01032021.txt")
#for im in range(5066):
for line in f:
    newline= line.replace("\t"," ")
    
    data=newline.split(" ")
    #data0=data.split(" ")
    #   print(data[8])
    layer_M.append(int(data[1]))
    u_M.append(int(data[3]))
    v_M.append(int(data[4]))
    typee_M.append(int(data[2]))
    nCells.append(int(data[5]))
    nHalfHgcrocs.append(int(data[6]))
    nMaxWords.append(int(data[7]))
    nMinWords.append(int(data[8]))
#### reading param_file                                                                                                        
layer=[]
u=[]
v=[]
typee=[]
constant1=[]
constant2=[]
constant3=[]
mean_G=[]
sigma_G=[]
mean_P=[]
mean_L=[]
sigma_L=[]
shape=[]
#data = np.loadtxt("./fit_function_parameters_01March2021.txt")
f1= open("./fit_function_parameters_01March2021.txt")

#for im in range(5066):
for line in f1:
    newline= line.replace("\t"," ")

    data1=newline.split(" ")

    #data1= line.split(" ")
    layer.append(int(data1[1]))
    u.append(int(data1[2]))
    v.append(int(data1[3]))
    typee.append(int(data1[4]))
    constant1.append(float(data1[5]))
    mean_G.append(float(data1[6]))
    sigma_G.append(float(data1[7]))
    constant2.append(float(data1[8]))
    mean_P.append(float(data1[9]))
    constant3.append(float(data1[10]))
    mean_L.append(float(data1[11]))
    sigma_L.append(float(data1[12]))


#fout = ROOT.TFile('DataPackets_after_fit_1M_%i.root' %min_, 'RECREATE')
fout = ROOT.TFile(out_fname, 'RECREATE')

tree = ROOT.TTree('tree', 'tree')
#M=202
print(len(layer))
#sys.exit()
M=2
n1=1550
n=1000000
count=0
count1=0
count2=0
### ## sampling random numbers from the fit
for im in  range(M):
    name='%i_%i_%i_%i' %(layer[im],typee[im],u[im],v[im])
    if((u[im]>=5 and u[im]<=8 and v[im]>=5and v[im]<=8 )and (layer[im]<=50 and layer[im]>=37)):
        fit_func= ROOT.TF1("fit_func","[0]*TMath::Gaus(x,[1],[2])+[3]*TMath::Poisson(x,[4])+[5]*exp([6]*x+[7])")
    else:
        fit_func= ROOT.TF1("fit_func","[0]*TMath::Gaus(x,[1],[2])+[3]*TMath::Poisson(x,[4])+[5]*TMath::Landau(x,[6],[7])")
    count+=1
    fit_func.FixParameter(0,constant1[im])
    fit_func.FixParameter(1,mean_G[im])
    fit_func.FixParameter(2,sigma_G[im])
    fit_func.FixParameter(3,constant2[im])
    fit_func.FixParameter(4,mean_P[im])
    fit_func.FixParameter(5,constant3[im])
    fit_func.FixParameter(6,mean_L[im])
    fit_func.FixParameter(7,sigma_L[im])
    f2=ROOT.TF1(fit_func.Clone())
    #f2.SetRange(,400)
    max_= nMaxWords[im]
    min_=nMinWords[im]
    print(min_)
    max_Words = max_/2
    min_words= min_/2
    if(max_Words==min_words):
        count1+=1
        nhitss=np.array(np.full((n,1),4),dtype=[('Module_%s' %name, np.float32)])
        array2tree(nhitss,tree=tree)

        # f2.SetRange(0,400
        # temp0 = random_sample(f2,n)
        # temp1= np.array(temp0[min_words<=temp0])
        # temp2=np.array(temp1[0:1000000])
        # temp2=temp2.reshape(-1,1)
    else:    
        # Integral = f2.Integral(min_words,max_Words)
        # if(Integral==0):
        #     print("...intergal", name)
        #     f2.SetRange(min_words, 2000)
        # else:
        f2.SetRange(min_words,max_Words)
        seed0=seed_+im
        temp0 = random_sample(f2,n1,seed=seed0)
        print(temp0)
        temp1= np.array(temp0[(min_words<=temp0) & (temp0<=max_Words)])
        temp2=np.array(temp1[0:n])
        temp2=temp2.reshape(-1,1)
        # print(len(temp1))
        # print(len(temp2))
        
        # if(len(temp2)!=1000000):
        #     nhitss=np.array(np.full((1000000,1),8),dtype=[('Module_%s' %name, np.float32)])
        #     #nhitss= np.array(temp0[0:1000000],dtype=[('Module_%s' %name, np.float32)])
        #     count2+=1
        #     print("problem")
        #     print(len(temp2))
        # else:
        nhitss= np.array(temp2,dtype=[('Module_%s' %name, np.float32)])
        
        array2tree(nhitss,tree=tree)
    if(im%100==0):
        print('im',im)
print(count)
print('c',count1)
print('c -problem',count2)
fout.cd()
tree.Write() 
fout.Close()
