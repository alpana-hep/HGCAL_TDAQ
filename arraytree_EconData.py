import ROOT
import plotting as plot
from array import array
import argparse
import tools
import json
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.TH1.AddDirectory(False)

# These lines make HGCHitProvider available via PyROOT
ROOT.gROOT.ProcessLine('#include "interface/HGCHitProvider.h"')
ROOT.gSystem.Load('lib/libHGCalBufferModel.so')
plot.ModTDRStyle()


def daqRawDataPacketWordsDec20(numberOfHalfHgcrocs,n10, n20, n30):
    nWords = 0
    subPacketVector = [0] * numberOfHalfHgcrocs

    nEach10 = int(n10) / int(numberOfHalfHgcrocs)
    nHigh10 = int(n10) % int(numberOfHalfHgcrocs)
    nEach20 = int(n20) / int(numberOfHalfHgcrocs)
    nHigh20 = int(n20) % int(numberOfHalfHgcrocs)
    nEach30 = int(n30) / int(numberOfHalfHgcrocs)
    nHigh30 = int(n30) % int(numberOfHalfHgcrocs)
    
    nCheck10 = 0
    nCheck20 = 0
    nCheck30 = 0
    
    for i in xrange(numberOfHalfHgcrocs):
        nSp10 = nEach10 + (1 if i < nHigh10 else 0)
        nSp20 = nEach20 + (1 if i < nHigh20 else 0)
        nSp30 = nEach30 + (1 if i < nHigh30 else 0)

        nCheck10 += nSp10
        nCheck20 += nSp20
        nCheck30 += nSp30

        if((nSp10 + nSp20 + nSp30) == 0): #empty
            # Header only
            subPacketVector[i] = 1
        else: # High occupancy
            #Header+ channels
            subPacketVector[i]=2+(16*nSp10+24*nSp20+32*nSp30+31)/32

        nWords += (2*subPacketVector[i])
        
    assert(nCheck10==n10)
    assert(nCheck20==n20)
    assert(nCheck30==n30)
    
    # Header + CRC
    nWords+= 2*3

    return nWords

parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', default='HGCalBEStudies.root', help='Input ROOT filename')
parser.add_argument('--output', '-o', default='hitData', help='Output ROOT filename')
parser.add_argument('--modifier', '-m', default='data/CMSSW/modifier_config_notransform.json', help='Modifier config json to convert hit numbers')
parser.add_argument('--mapping', '-a', default='data/FE/FeMappingV8.txt', help='Mapping file to define the modules')
parser.add_argument('--modules', default='data/FE/DaqModules.txt', help='File defining module properties')
parser.add_argument('--events', '-e', type=int, default=-1, help='Number of events to process (-1 for all events)')
args = parser.parse_args()

orig_geo = tools.ReadOrigGeoFile('data/FE/geomnew_corrected_withmult.txt')

modinfo = tools.ReadModuleFile(args.modules)
print modinfo

modifier = {}
with open(args.modifier) as jsonfile:
    modjson = json.load(jsonfile)
    for item in modjson:
        modifier[tuple(item['key'])] = dict(item)

hitprovider = ROOT.HGCHitProvider()
hitprovider.initialise(args.mapping, args.modifier)
hitprovider.setFile(args.input, 'beLinksNTuple/EventTree')

n_tot_evts = hitprovider.getEntries()
evts_to_proc = n_tot_evts if args.events == -1 else args.events

print '>> Using file %s and processing %i/%i pseudo events' % (args.input, evts_to_proc, n_tot_evts)

# hists_hits_orig = []
# hists_hits_orig_10 = []
# hists_hits_orig_20 = []
# hists_hits_orig_30 = []
# hists_hits_orig_BXM1 = []
# hists_hits_trans = []
# hists_hits_trans_10 = []
# hists_hits_trans_20 = []
# hists_hits_trans_30 = []
# hists_hits_trans_BXM1 = []
# hists_words_trans = []

# for im in xrange(hitprovider.modules().size()):
#     module = hitprovider.modules()[im]
#     # Produces TH1s with name [layer]_[type]_[U]_[V}]
#     name = '%i_%i_%i_%i' % (module.layer, module.type, module.u, module.v)
#     hists_hits_orig.append(ROOT.TH1F('orig_hits_%s' % name, '', 500, 0, 500))
#     hists_hits_orig_10.append(ROOT.TH1F('orig_hits_10_%s' % name, '', 500, 0, 500))
#     hists_hits_orig_20.append(ROOT.TH1F('orig_hits_20_%s' % name, '', 500, 0, 500))
#     hists_hits_orig_30.append(ROOT.TH1F('orig_hits_30_%s' % name, '', 500, 0, 500))
#     # hists_hits_orig_BXM1.append(ROOT.TH1F('orig_hits_BXM1_%s' % name, '', 500, 0, 500))
#     # hists_hits_trans.append(ROOT.TH1F('trans_hits_%s' % name, '', 500, 0, 500))
#     # hists_hits_trans_10.append(ROOT.TH1F('trans_hits_10_%s' % name, '', 500, 0, 500))
#     # hists_hits_trans_20.append(ROOT.TH1F('trans_hits_20_%s' % name, '', 500, 0, 500))
#     # hists_hits_trans_30.append(ROOT.TH1F('trans_hits_30_%s' % name, '', 500, 0, 500))
#     # hists_hits_trans_BXM1.append(ROOT.TH1F('trans_hits_BXM1_%s' % name, '', 500, 0, 500))
#     hists_words_trans.append(ROOT.TH1F('trans_words_%s' % name, '', 1000, 0, 1000))
fout = ROOT.TFile(args.output+'.root', 'RECREATE')
#fout.cd()
t = ROOT.TTree('EventTree', 'EventTree')

np_event_list_modules=np.empty((5066,1), dtype="int64")

for im in xrange(hitprovider.modules().size()):
    module = hitprovider.modules()[im]
    name='%i_%i_%i_%i' %(module.layer,module.type,module.u,module.v)
    # layer_number.append(module.layer)
    # U.append(module.u)
    # V.append(module.v)
    # typee.append(module.type)
    np_event_list_modules[im]=np.empty((1), dtype="int64")
    t.Branch('Module_%s' %name,np_event_list_modules[im],'Modules_%s/I'%name)


mods = hitprovider.modules()
nMods = len(mods)
modHalfRocs = [0] * nMods
for im in xrange(nMods):
    key = (mods[im].type, mods[im].s)
    if key not in modinfo:
        # print key
        modHalfRocs[im] = 1
    else:
        modHalfRocs[im] = modinfo[key]['n_calib_cells']
# print modHalfRocs

maxWords = 0
for ie in xrange(evts_to_proc):
    if ie % 1000 == 0:
        print '>> Processed %i pseudo events' % ie
    hitprovider.processEvent(ie)

    origHits10 = array('d', hitprovider.hits10(True))
    origHits20 = array('d', hitprovider.hits20(True))
    origHits30 = array('d', hitprovider.hits30(True))
    # origHitsBXM1 = array('d', hitprovider.hitsBXM1(True))
    transHits10 = array('d', hitprovider.hits10(False))
    transHits20 = array('d', hitprovider.hits20(False))
    transHits30 = array('d', hitprovider.hits30(False))
    # transHitsBXM1 = array('d', hitprovider.hitsBXM1(False))

    for im in xrange(nMods):
        nWords = daqRawDataPacketWordsDec20(modHalfRocs[im],origHits10[im], origHits20[im], origHits30[im])
        nWords_32 = nWords/2
        maxWords = max(maxWords, nWords)
        # hists_hits_orig[im].Fill(origHits10[im] + origHits20[im] + origHits30[im])
        # hists_hits_orig_10[im].Fill(origHits10[im])
        # hists_hits_orig_20[im].Fill(origHits20[im])
        # hists_hits_orig_30[im].Fill(origHits30[im])
        # hists_hits_orig_BXM1[im].Fill(origHitsBXM1[im])
        # hists_hits_trans[im].Fill(transHits10[im] + transHits20[im] + transHits30[im])
        # hists_hits_trans_10[im].Fill(transHits10[im])
        # hists_hits_trans_20[im].Fill(transHits20[im])
        # hists_hits_trans_30[im].Fill(transHits30[im])
        # hists_hits_trans_BXM1[im].Fill(transHitsBXM1[im])
        #hists_words_trans[im].Fill(nWords_32)
        np_event_list_modules[im][0]=nWords_32
    t.Fill()
fout.cd()
t.Write()
fout.Close()
# print '>> ' + str(maxWords)
# gr_20_x = []
# gr_20_y = []
# gr_30_x = []
# gr_30_y = []

# gr_scale_x = []
# gr_scale_y = []

# with open(args.output + '.txt', 'w') as out_file:
#     for im in xrange(hitprovider.modules().size()):
#         module = hitprovider.modules()[im]
#         av_rate = hists_hits_orig[im].GetMean()
#         av_rate_20 = hists_hits_orig_20[im].GetMean()
#         av_rate_30 = hists_hits_orig_30[im].GetMean()
#         key = (module.layer, module.u, module.v)
#         geo_av_rate = orig_geo.get(key, -1.0)
#         out_file.write('%i %i %i %f %f\n' % (key[0], key[1], key[2], av_rate, geo_av_rate))
#         # print '%-2i %-2i %-2i %10.2f %10.2f %10.2f' % (key[0], key[1], key[2], av_rate, geo_av_rate, av_rate / geo_av_rate if geo_av_rate > 0 else 0.0)
#         gr_20_x.append(av_rate_20)
#         gr_30_x.append(av_rate_30)

#         gr_scale_x.append(av_rate)
#         gr_scale_y.append(hists_hits_trans[im].GetMean())

# gr_scale = ROOT.TGraph(len(gr_scale_x), array('d', gr_scale_x), array('d', gr_scale_y))


# with open(args.output + '_occ_summary.txt', 'w') as out_file:
#     out_file.write('# l  u  v  type  shape  cells  cmssw_type  cmssw_shape  cmssw_cells  <nHitsTotal>  corrFactorTotal  <nHistsToA>  corrFactorToA  <nHitsBXM1>  corrFactorBXM1  <n32bWords>\n')
#     for im in xrange(hitprovider.modules().size()):
#         module = hitprovider.modules()[im]
#         if module.type >= 2:
#             continue
#         av_rate_orig = hists_hits_orig[im].GetMean()
#         av_rate_trans = hists_hits_trans[im].GetMean()
#         av_rate_ratio = av_rate_trans / av_rate_orig if av_rate_orig > 0 else 0.
#         av_rate_10_orig = hists_hits_orig_10[im].GetMean()
#         av_rate_10_trans = hists_hits_trans_10[im].GetMean()
#         av_rate_10_ratio = av_rate_10_trans / av_rate_10_orig if av_rate_10_orig > 0 else 0.
#         av_rate_20_orig = hists_hits_orig_20[im].GetMean()
#         av_rate_20_trans = hists_hits_trans_20[im].GetMean()
#         av_rate_20_ratio = av_rate_20_trans / av_rate_20_orig if av_rate_20_orig > 0 else 0.
#         av_rate_30_orig = hists_hits_orig_30[im].GetMean()
#         av_rate_30_trans = hists_hits_trans_30[im].GetMean()
#         av_rate_30_ratio = av_rate_30_trans / av_rate_30_orig if av_rate_30_orig > 0 else 0.
#         av_rate_BXM1_orig = hists_hits_orig_BXM1[im].GetMean()
#         av_rate_BXM1_trans = hists_hits_trans_BXM1[im].GetMean()
#         av_rate_BXM1_ratio = av_rate_BXM1_trans / av_rate_BXM1_orig if av_rate_BXM1_orig > 0 else 0.
#         av_words = hists_words_trans[im].GetMean()
#         modifier_info = modifier[(module.layer, module.u, module.v)]
#         target_shape = modifier_info['shape']
#         target_type = modifier_info['type']
#         if 'n_cells' in modifier_info:
#             target_cells = float(modifier_info['n_cells'])
#             cmssw_cells = float(modifier_info['cmssw_n_cells'])
#             cmssw_shape = modifier_info['cmssw_shape']
#             cmssw_type = modifier_info['cmssw_type']
#         else:
#             target_cells = 0
#             cmssw_cells = 1
#             cmssw_shape = '?'
#             cmssw_type = 0

#         out_file.write('%3i %3i %3i %3i %3s %3i %3i %3s %3i %10f %10f %10f %10f %10f %10f %10f\n' % (
#             module.layer, module.u, module.v,
#             target_type, target_shape, target_cells,
#             cmssw_type, cmssw_shape, cmssw_cells,
#             av_rate_orig, av_rate_ratio,
#             av_rate_30_orig, av_rate_30_ratio,
#             av_rate_BXM1_orig, av_rate_BXM1_ratio, av_words / 2.))



# canv = ROOT.TCanvas(args.output + '_trans_vs_orig')
# pads = plot.OnePad()

# gr_scale.Draw('AP')

# gr_scale.SetMarkerSize(0.5)

# axis = plot.GetAxisHist(pads[0])

# axis.GetXaxis().SetTitle('CMSSW hits')
# axis.GetYaxis().SetTitle('Corrected hits')
# hline = ROOT.TLine()
# plot.Set(hline, LineColor=16, LineStyle=2)
# hline.DrawLine(0, 0, 340, 340)

# canv.Print('.pdf')
# canv.Print('.png')


# fout = ROOT.TFile(args.output + '.root', 'RECREATE')
# fout.cd()
# for h in hists_hits_orig:
#     h.Write()
# for h in hists_hits_orig_10:
#     h.Write()
# for h in hists_hits_orig_20:
#     h.Write()
# for h in hists_hits_orig_30:
#     h.Write()
# for h in  hists_words_trans:
#     h.Write()
# for h in hists_hits_orig_BXM1:
#     h.Write()
# for h in hists_hits_trans:
#     h.Write()
# for h in hists_hits_trans_10:
#     h.Write()
# for h in hists_hits_trans_20:
#     h.Write()
# for h in hists_hits_trans_30:
#     h.Write()
# for h in hists_hits_trans_BXM1:
#     h.Write()
#fout.Close()
