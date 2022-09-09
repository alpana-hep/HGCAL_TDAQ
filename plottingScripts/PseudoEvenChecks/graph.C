#include <stdio.h>
#include<fstream>
#include <vector>
#include <string>
#include <map>
#include<iostream>
using namespace std;


void graph(string root_file_name)
{
char* title= new char[200]; char* path = new char[2000];
  char* full_path = new char[2000];
  char* path1 = new char[2000];
  char* full_path1 = new char[2000];
  char* path2 = new char[2000];
char* full_path2 = new char[2000];
 char* hname = new char[2000];
  char* hname1 = new char[2000];
  char* hname0 = new char[2000];
char* name = new char[2000];
  char* hist_name = new char[200];
  char* hist_name1 = new char[200];
  char* hist_name2 = new char[200];
  char* hist_name3 = new char[200];

  sprintf(hname,"%s",root_file_name.c_str());
  sprintf(path2,"Results/1d_plots");
    TFile * inputfile = new TFile(hname,"READ");
    sprintf(hist_name,"gr_ave_cmssw_pred_n30");
    TGraph* gr = (TGraph*)inputfile->Get(hist_name);
    TCanvas *Canvas_n2 = new TCanvas(hist_name, hist_name,900,700);//65,725,725);
    Canvas_n2->Range(-60.25,-0.625,562.25,0.625);
    Canvas_n2->SetFillColor(0);
    Canvas_n2->SetBorderMode(0);
    Canvas_n2->SetBorderSize(2);
    //gStyle->SetOptFit(111111);
    sprintf(full_path2,"./Results/gr_ave_cmssw_pred_n30.pdf");
    gr->GetXaxis()->SetTitle("Average n30 occupancy -CMSSW");
    gr->GetYaxis()->SetTitle("Average n30 occupancy -Pseudo");
    gr->GetXaxis()->SetTitleSize(0.035);
    gr->GetXaxis()->SetTitleOffset(0.99);
    gr->GetYaxis()->SetTitleSize(0.035);
    gr->GetYaxis()->SetTitleOffset(1.15);
    gr->SetLineStyle(1);
    gr->SetLineWidth(2);
    gr->SetMarkerColorAlpha(kBlue, 0.95);
    gr->SetMarkerSize(1.5);
    gr->SetMarkerStyle(8);

    gr->Draw("AP");
    Canvas_n2->Modified();
    Canvas_n2->cd();
    Canvas_n2->SetSelected(Canvas_n2);
    Canvas_n2->SaveAs(full_path2);
}

  
