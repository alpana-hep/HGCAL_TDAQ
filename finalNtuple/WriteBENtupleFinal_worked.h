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

  TFile *oFile;

  TTree *tnew;
  // define tree variables
  std::vector<int> nhits20_defined;
  // declaring branches for l, u, v, type, bx .... 

  // vector to be read from l u v text file ... v_vread ... 


};
#endif

#ifdef WRITEBENTUPLEFINAL_cxx

void WriteBENtupleFinal::BookHistogram(const char *outFileName,const char *dataset) {
  
  oFile = new TFile(outFileName, "recreate");
  tnew = new TTree("Eventtree", "my event tree");
  tnew->Branch("nhits20_defined",&nhits20_defined);
  // define branches for l, u, v, type, bx ...
}


WriteBENtupleFinal::WriteBENtupleFinal(const TString &inputFileList, const char *outFileName, const char* dataset) {

  TChain *tree = new TChain("tree");

  if( ! FillChain(tree, inputFileList) ) {
    std::cerr << "Cannot get the tree " << std::endl;
  } else {
    std::cout << "Initiating analysis of dataset " << dataset << std::endl;
  }

  NtupleVariables::Init(tree);

  // read v_read here

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

