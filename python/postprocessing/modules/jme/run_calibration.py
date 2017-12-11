#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jecUncertainties import *

from  jecEventWeights import * 
#p=PostProcessor(".",['root://cms-xrd-global.cern.ch//store/group/cmst3/group/nanoAOD/NanoTestProd006/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer17MiniAOD-92X-NanoCrabProd006/171006_155430/0000/nanolzma_1.root'],"Entry$ < 50000","keep_and_drop.txt",[jecUncert_cpp(),jecEventWeightCalib()],provenance=True)
#p=PostProcessor(".",['root://cms-xrd-global.cern.ch//store/group/cmst3/group/nanoAOD/NanoTestProd006/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer17MiniAOD-92X-NanoCrabProd006/171006_155430/0000/nanolzma_1.root',"root://cms-xrd-global.cern.ch//store/group/cmst3/group/nanoAOD/NanoTestProd006/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer17MiniAOD-92X-NanoCrabProd006/171006_155430/0000/nanolzma_2.root"],"","keep_and_drop.txt",[jecUncert_cpp(),jecEventWeightCalib()],provenance=True)
files=[
'root://cms-xrd-global.cern.ch//store/user/arizzi/NanoTestProd004/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/NanoCrabProd004/171002_115725/0000/lzma_100.root',
]
aaa=[
'root://cms-xrd-global.cern.ch//store/user/arizzi/NanoTestProd004/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/NanoCrabProd004/171002_115725/0000/lzma_101.root',
'root://cms-xrd-global.cern.ch//store/user/arizzi/NanoTestProd004/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/NanoCrabProd004/171002_115725/0000/lzma_102.root',
'root://cms-xrd-global.cern.ch//store/user/arizzi/NanoTestProd004/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/NanoCrabProd004/171002_115725/0000/lzma_103.root',
'root://cms-xrd-global.cern.ch//store/user/arizzi/NanoTestProd004/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/NanoCrabProd004/171002_115725/0000/lzma_104.root',
'root://cms-xrd-global.cern.ch//store/user/arizzi/NanoTestProd004/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/NanoCrabProd004/171002_115725/0000/lzma_105.root',
"root://cms-xrd-global.cern.ch//store/user/arizzi/NanoTestProd004/ZH_HToBB_ZToLL_M125_13TeV_amcatnloFXFX_madspin_pythia8/NanoCrabProd004/171002_120628/0000/lzma_1.root",
"root://cms-xrd-global.cern.ch//store/user/arizzi/NanoTestProd004/ZH_HToBB_ZToLL_M125_13TeV_amcatnloFXFX_madspin_pythia8/NanoCrabProd004/171002_120628/0000/lzma_2.root",
"root://cms-xrd-global.cern.ch//store/user/arizzi/NanoTestProd004/ZH_HToBB_ZToLL_M125_13TeV_amcatnloFXFX_madspin_pythia8/NanoCrabProd004/171002_120628/0000/lzma_3.root",
"root://cms-xrd-global.cern.ch//store/user/arizzi/NanoTestProd004/ZH_HToBB_ZToLL_M125_13TeV_amcatnloFXFX_madspin_pythia8/NanoCrabProd004/171002_120628/0000/lzma_4.root",
"root://cms-xrd-global.cern.ch//store/user/arizzi/NanoTestProd004/ZH_HToBB_ZToLL_M125_13TeV_amcatnloFXFX_madspin_pythia8/NanoCrabProd004/171002_120628/0000/lzma_5.root"


]
p=PostProcessor(".",files,"","keep_and_drop.txt",[jecUncert_cpp(),jecEventWeightCalib()],provenance=True,friend=True)
#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/user/arizzi/NanoTestProd004/ZH_HToBB_ZToLL_M125_13TeV_amcatnloFXFX_madspin_pythia8/NanoCrabProd004/171002_120628/0000/lzma_1.root"],"","keep_and_drop.txt",[jecUncert_cpp(),jecEventWeightCalib()],provenance=True)
p.run()
