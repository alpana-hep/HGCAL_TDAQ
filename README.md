# HGCAL_TDAQ
DAQ and TPG Studies
this branch contains the step by step instructions to get the CMSSW based pseudo event generation with correct modeling of correlation.

Link to the slides showing the work flow of pseudo event generation
https://indico.cern.ch/event/1014822/ (See update from Alpana)

## Step-0.0  Preparing input files needed (a) occupancy histograms for all the modules , (b) occpuancy arrays in all three formats (c) mapping files

cmsrel CMSSW_11_1_0_pre3
cd CMSSW_11_1_0_pre3/src
cmsenv
git init
git clone ssh://git@gitlab.cern.ch:7999/agilbert/HGCalBufferModel.git .
python scripts/generateHitData.py  -i <input root ntuple> --output hitData_${TYPE} -e 500 --modifier data/CMSSW/modifier_config_${TYPE}.json 2>&1 | tee hit_averages_EOL_${TYPE}.txt; done
where {Type} = for TYPE in notransform fixdensity pessimistic optimistic

You will get a root file named hitData_${TYPE}.root which will have all the 1-d occupancy distributions for all modules

(b) cp https://gitlab.cern.ch/kalpana/HGCalBufferModel/-/blob/Datapackets/arraytree_EconData.py .
 python  arraytree_EconData.py  -i <input root ntuple> --output hitData_${TYPE} -e 500 --modifier data/CMSSW/modifier_config_${TYPE}.json

(Repeat for three times and get three root files containing one branch for each module)

This step needs to be done once for same input file

## Step 1.0: Fit the occupancy distributions & save the fit functions parameters in a txt file (different file for different occupancy format [n10,n20,n30]

You can do this locally in your computer or you can use the CMSSW_11_1_0_pre3 version
git clone -b PseudoEvents git@github.com:alpana-hep/HGCAL_TDAQ.git
cd Fits
root -b 'n*_fitting.C("occupancy_histogram_file","mapping file (FeMapping)")'  // where * = 10,20,30

#### This scripts fits the occupancy distributions and saves the plots and write the parameters in the txt files. Check for bad fits & accordingly change the initial values of the parameters in the code

## Step 1.1: Calculating the covariance matrix[15k X 115k] and storing it into a txt file

python3 calCorrMatrix.py

This will save the correlation matrix into a txt file

## Step2: Generating random gaussian numbers [n = 1M or whatever value you want] and save these to a root file so that these can be correlated after multiplying it with the correlation matrix

Python3 genRandon.py
{generates root file containing uncorrelated random number with gaussian distribution [0:1], mind the random seed}

To correlate these random numbers
Python3 matrix_multiplication_v1.py $min_ $max_ $out_fname $fin // see the code to understand the argument meaning

this will generate a root file containing one branch for each module

## Step3: Sampling random numbers from the fit function and save them in a root file
python3 randomSampling_fit_v1.py $min_ $max_


## Step4: This step is to read correlated random numbers and random sampled numbers from the fit function and use quantile tranformation to transfer correlated numbers to fitted random sampled space
python3 quantile_transf_condorjobs_v6.py $infile_fitrandomSamples $infile_correlatedrandomNumber $outfile $min_ $max_

This will give us a root file which will contain one branch containing pseudo correlated events for each module.


## Step5: The final step is to convert the output from step4 to a ntuple compatible to the emulator code.

Two ways to do this:
Either use MakeClass method for root files : 
(a) root -l <outfrom step4>
tree->MakeClass("allinone")

(b) root -l
    .L tree_try5k_v1.C
    allinone M
    m.Loop()

You will get the final ntuple compatible with emulator code

Or use the Analyzer in finalNtuple/
cp tree_try5k_v1.C WriteBENtupleFinal.cc
And make slight changes according to need





