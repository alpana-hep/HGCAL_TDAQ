#ifndef WRITEBENTUPLEFINAL_H
#define WRITEBENTUPLEFINAL_H

#include <iostream>
#include <fstream>
#include <cmath>
#include <vector>
#include "NtupleVariables.h"
#include "TTree.h"

class WriteBENtupleFinal : public NtupleVariables{

 public:
  WriteBENtupleFinal(const TString &inputFileList="foo.txt", const char *outFileName="histo.root",const char *dataset="data");
  ~WriteBENtupleFinal();
  Bool_t   FillChain(TChain *chain, const TString &inputFileList);
  Long64_t LoadTree(Long64_t entry);
  void     EventLoop(const char *);
  void     BookHistogram(const char *,const char*);

  //define module indentifier map (l, u, v etc.)
  struct modulemap {
    unsigned int  layer, u, v, type;
    char shape;
    int  nDaqElinks1, nDaqElinks2;
    int  idxDaqLpgbt1, idxDaqLpgbt2;
    unsigned nDaqLpgbt,nTpgLpgbt;
    int idxTpgLpgbt1, nTpgElinks1, idxTpgLpgbt2, nTpgElinks2;
  };
  std::vector <modulemap> map_vec;
  std::vector<int> map_layer;
  std::vector<int> map_wafer_u;
  std::vector<int> map_wafer_v;
  std::vector<int> map_type;
  std::vector<int> dummy_zeros;
  
  // output tree
  TFile *oFile;
  TTree *tnew;
  // define tree variables
  std::vector<int> layer;
  std::vector<int> wafer_u;
  std::vector<int> wafer_v;
  std::vector<int> type;
  std::vector<int> nhits10;
  std::vector<int> nhits30;
  std::vector<int> nhits20;
  std::vector<int> nhitsBXM1;
  std::vector<int> nhits30_defined;
  std::vector<int> nhits20_defined;
  std::vector<int> nhits10_defined;
  std::vector<int> nhitsBXM1_defined;
  std::vector<int> nhits10_unmasked;
  std::vector<int> nhits20_unmasked;
  std::vector<int> nhits30_unmasked;
  std::vector<int> nhitsBXM1_unmasked;
   UInt_t          lumi;
  UInt_t          run;
  Int_t           pseudo_event;

  std::vector<int>data_packets;
  ULong64_t event;

};
#endif

#ifdef WRITEBENTUPLEFINAL_cxx

void WriteBENtupleFinal::BookHistogram(const char *outFileName,const char *dataset) {
  
  oFile = new TFile(outFileName, "recreate");
  oFile->mkdir("beLinksNTuple");
  oFile->cd("beLinksNTuple");

  tnew = new TTree("EventTree", "my event tree");

  //  tnew->Branch("event",   &event, "event/l");
  tnew->Branch("event",   &event);
  tnew->Branch("layer",   &layer);
  tnew->Branch("wafer_v", &wafer_v);
  tnew->Branch("wafer_u", &wafer_u);
  tnew->Branch("type",    &type);
  tnew->Branch("nhits20_defined",   &nhits20_defined);
  tnew->Branch("nhits30_defined",   &nhits30_defined);
  tnew->Branch("nhitsBXM1_defined", &nhitsBXM1_defined);
  tnew->Branch("data_packets",&data_packets);

}


WriteBENtupleFinal::WriteBENtupleFinal(const TString &inputFileList, const char *outFileName, const char* dataset) {

  TChain *tree = new TChain("tree");

  if( ! FillChain(tree, inputFileList) ) {
    std::cerr << "Cannot get the tree " << std::endl;
  } else {
    std::cout << "Initiating analysis of dataset " << dataset << std::endl;
  }

  NtupleVariables::Init(tree);

  // read mapping file and populate mapping vector
  std::ifstream mapping_file;
  mapping_file.open("module_info_27022021.txt",ios::in);
  struct modulemap {
     int  layer, u, v, type;
    int nCells, nHalfHgcrocs, nMaxWords, nMinWords;
};
  std::vector <modulemap> map_vec;
  std::vector<int> map_layer;
  std::vector<int> map_wafer_u;
  std::vector<int> map_wafer_v;
  std::vector<int> map_type;
  std::vector<int> dummy_zeros;

  if(!mapping_file.is_open())
    {
      std::cout << " file not opened" << std::endl;
    }
  else
    {
      map_vec.clear();
      map_layer.clear();
      map_wafer_u.clear();
      map_wafer_v.clear();
      map_type.clear();
      dummy_zeros.clear();

      while (true) {
        unsigned int  index,layer, u, v, type;
        char shape;
        int  idxDaqLpgbt1, idxDaqLpgbt2;
        int nDaqElinks1, nDaqElinks2;
        int   idxTpgLpgbt1, nTpgElinks1, idxTpgLpgbt2, nTpgElinks2;
        int nDaqLpgbt, nTpgLpgbt;
        // int nDaqLpgbt, nTpgLpgbt;                                                                                                                                      
        mapping_file >> index>>layer>>type >> u >> v
                     >> nDaqLpgbt >> nTpgLpgbt
                     >> idxDaqLpgbt1 >> nDaqElinks1;   if (mapping_file.eof()) break;
        map_layer.push_back(layer);
        map_wafer_u.push_back(u);
        map_wafer_v.push_back(v);
        map_type.push_back(type);
        dummy_zeros.push_back(0);

      }
      mapping_file.close();
    }


  //std::cout << "In WriteBENtupleFinal() map_vec size is : " << map_vec.size() << std::endl;
  std::cout << "In WriteBENtupleFinal() map_layer size is " << map_layer.size() << " " 
	    << map_wafer_u.size() << " " << map_wafer_v.size() <<" " << map_type.size() 
	    << std::endl;

  BookHistogram(outFileName,dataset);


}

Bool_t WriteBENtupleFinal::FillChain(TChain *chain, const TString &inputFileList) {

  ifstream infile(inputFileList, ifstream::in);
  std::string buffer;

  if(!infile.is_open()) {
    std::cerr << "** ERROR: Can't open '" << inputFileList << "' for input" << std::endl;
    return kFALSE;
  }

  std::cout << "TreeUtilities : FillChain " << std::endl;
  while(1) {
    infile >> buffer;
    if(!infile.good()) break;
    //    std::cout << "Adding tree from " << buffer.c_str() << std::endl;                                                              
    chain->Add(buffer.c_str());
  }
  std::cout << "No. of Entries in this tree : " << chain->GetEntries() << std::endl;
  return kTRUE;
}

Long64_t WriteBENtupleFinal::LoadTree(Long64_t entry) {
  // Set the environment to read one entry                                                                                          
  if (!fChain) return -5;
  Long64_t centry = fChain->LoadTree(entry);
  if (centry < 0) return centry;
  if (!fChain->InheritsFrom(TChain::Class()))  return centry;
  TChain *chain = (TChain*)fChain;
  if (chain->GetTreeNumber() != fCurrent) {
    fCurrent = chain->GetTreeNumber();
    //    Notify();
  }
  return centry;
}

WriteBENtupleFinal::~WriteBENtupleFinal() { 

  if (!fChain) return;
  delete fChain->GetCurrentFile();
  oFile->cd();
  oFile->Write();
  oFile->Close();

}

#endif

