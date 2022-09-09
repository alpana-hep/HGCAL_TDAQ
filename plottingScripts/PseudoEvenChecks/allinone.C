#define allinone_cxx
#include "allinone.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

void allinone::Loop()
{
//   In a ROOT session, you can do:
//      root> .L allinone.C
//      root> allinone t
//      root> t.GetEntry(12); // Fill t data members with entry number 12
//      root> t.Show();       // Show values of entry 12
//      root> t.Show(16);     // Read and show values of entry 16
//      root> t.Loop();       // Loop on all entries
//

//     This is the loop skeleton where:
//    jentry is the global entry number in the chain
//    ientry is the entry number in the current Tree
//  Note that the argument to GetEntry must be:
//    jentry for TChain::GetEntry
//    ientry for TTree::GetEntry and TBranch::GetEntry
//
//       To read only selected branches, Insert statements like:
// METHOD1:
//    fChain->SetBranchStatus("*",0);  // disable all branches
//    fChain->SetBranchStatus("branchname",1);  // activate branchname
// METHOD2: replace line
//    fChain->GetEntry(jentry);       //read all branches
//by  b_branchname->GetEntry(ientry); //read only this branch
   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();

   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      cout<<( *layer).size()<<endl;
      for (int i=0; i<( *layer).size();i++)
	{
	  if(( *layer)[i]==11 && (*wafer_u)[i] ==1 && (*wafer_v)[i] ==5 )
	    {
	      //if((*nhits10_defined)[i]+(*nhits20_defined)[i]+(*nhits30_defined)[i]>192)
		cout<<(*nhits10_defined)[i]<<"\t"<<(*nhits20_defined)[i]<<"\t"<<(*nhits30_defined)[i]<<endl;
	    }
	}
      // if (Cut(ientry) < 0) continue;
   }
}
