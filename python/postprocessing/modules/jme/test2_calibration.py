#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jecUncertainties import *

from  jecEventWeights import *
p=PostProcessor(".",['root://cms-xrd-global.cern.ch//store/user/arizzi/NanoTestProd004/ZH_HToBB_ZToLL_M125_13TeV_amcatnloFXFX_madspin_pythia8/NanoCrabProd004/171002_120628/0000/lzma_1.root'],"Entry$ < 300000","keep_and_drop.txt",[jecUncert_cpp(),jecEventWeight()],provenance=True)
p.run()
