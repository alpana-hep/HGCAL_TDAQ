# HGCAL_TDAQ
DAQ and TPG Studies
this branch contains the step by step instructions to get the CMSSW based pseudo event generation with correct modeling of correlation.

##Step-0.0  We start with individual occupancy histograms for all the modules.

cmsrel CMSSW_11_1_0_pre3
cd CMSSW_11_1_0_pre3/src
cmsenv
git init
git clone ssh://git@gitlab.cern.ch:7999/agilbert/HGCalBufferModel.git .
python scripts/generateHitData.py  -i <input root ntuple> --output hitData_${TYPE} -e 500 --modifier data/CMSSW/modifier_config_${TYPE}.json 2>&1 | tee hit_averages_EOL_${TYPE}.txt; done
where {Type} = for TYPE in notransform fixdensity pessimistic optimistic

You will get a root file named hitData_${TYPE}.root which will have all the 1-d occupancy distributions for all modules

##Step 1: Fit the occupancy distributions & save the fit functions parameters in a txt file (different file for different occupancy format [n10,n20,n30]
You can do this locally in your computer or you can use the CMSSW_11_1_0_pre3 version
git clone -b quantile_transformation git@github.com:alpana-hep/HGCAL_TDAQ.git

