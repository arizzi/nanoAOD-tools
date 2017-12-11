import ROOT
import os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True
from math import *
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class jecEventWeights(Module):
    def __init__(self,uncerts=["Total"],calibrate=False,collapseDeltaR=False):
	self.calibrate=calibrate
	self.uncerts=uncerts
	self.collapseDeltaR=collapseDeltaR
	if self.calibrate:
	    self.deltaRbins = [0.5,0.8,1.2,1.5,2.0]
#	    self.deltaRbins = [0,0.45,0.48,0.52,0.55,0.6] #actually area
	    self.calibHistos={}
	    self.hf=ROOT.TFile("calib.root","recreate")
	    for u in ["central"]+self.uncerts :
	     for fl in [0,4,5] :
   	      for b in self.deltaRbins :
		#self.calibHistos["%s_%s"%(u,b)]=ROOT.TH3F("%s_deltaR%s"%(u,b),"%s_deltaR%s"%(u,b),40,0.7,1.5,40,20,400,10,0,5)
		self.calibHistos["%s_%s_%s"%(u,b,fl)]=ROOT.TH3F("%s_deltaR%s_flav%s"%(u,b,fl),"%s_deltaR%s_flav%s"%(u,b,fl),40,0.5,2,15,3,6,20,0,5)
	else :
            self.f=ROOT.TFile.Open("calib.root")
            self.deltaRbins = [0.5,0.8,1.2,1.5,2.0]
#	    self.deltaRbins = [0.2,0.5,0.8,0.95,0.98]   #btag
#	    self.deltaRbins = [0,0.45,0.48,0.52,0.55,0.6] #area
            self.calibHistos={}
            for u in ["central"]+self.uncerts :
             for fl in [0,4,5] :
              for b in self.deltaRbins :
		 self.calibHistos["%s_%s_%s"%(u,b,fl)]=self.f.Get("%s_deltaR%s_flav%s"%(u,b,fl))
		 print "%s_%s_%s"%(u,b,fl), self.calibHistos["%s_%s_%s"%(u,b,fl)].GetEntries()
		
              if self.collapseDeltaR :
 		self.calibHistos["%s_%s"%(u,fl)]=ROOT.TH3F("%s_flav%s"%(u,fl),"%s_flav%s"%(u,fl),20,0.7,1.5,10,3,6,8,0,5)
		for b in self.deltaRbins :
		  self.calibHistos["%s_%s"%(u,fl)].Add(self.calibHistos["%s_%s_%s"%(u,b,fl)])
		for b in self.deltaRbins :
		  self.calibHistos["%s_%s_%s"%(u,b,fl)]=self.calibHistos["%s_%s"%(u,fl)]
		  print "%s_%s_%s"%(u,b,fl), self.calibHistos["%s_%s_%s"%(u,b,fl)].GetEntries(),self.calibHistos["%s_%s"%(u,fl)].GetEntries()

    def beginJob(self):
	self.misstarget=0
	self.missnominal=0
	self.miss=0
	pass

    def endJob(self):
	print self.misstarget,self.missnominal, self.miss

	if hasattr(self,"hf") :
		self.hf.Write()

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for u in self.uncerts :
                self.out.branch("EventWeight_jecUncert%s"%u, "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = Collection(event, "Jet")
        genjets = Collection(event, "GenJet")
	if self.calibrate :
          for j in jets:
           if j.genJetIdx!=-1 and j.genJetIdx<len(genjets) and genjets[j.genJetIdx].pt>20 and j.jetId >0 and j.puId > 0:
	    fl = j.hadronFlavour
	    minDeltaR=min([deltaR(j,j1) for j1 in jets if j1!=j and j1.pt > 15 and j1.puId > 0 and j1.jetId > 0] or  [999]) 
#	    minDeltaR=j.area
	    b=next((b for b in self.deltaRbins if b>minDeltaR),self.deltaRbins[-1])
	    genpt=genjets[j.genJetIdx].pt #if j.genJetIdx!=-1 and j.genJetIdx<len(genjets) else 0
	    if genpt > 0 :
		for u in ["central"]+self.uncerts :
			jpt=j.pt
			if u!="central" :
				jpt*=(1.+getattr(j,"jecUncert%s"%u))
			self.calibHistos["%s_%s_%s"%(u,b,fl)].Fill(jpt/genpt,log(genpt),abs(genjets[j.genJetIdx].eta))
#			print "filled", getattr(j,"jecUncert%s"%u),jpt/genpt,j.pt,abs(j.eta)
	else :
          for u in self.uncerts :
	    jetUn=1.
            for j in jets:
	     if j.genJetIdx!=-1 and j.genJetIdx<len(genjets) and genjets[j.genJetIdx].pt>20 and j.jetId >0 and j.puId > 0:
	      fl = j.hadronFlavour
  	      minDeltaR=min([deltaR(j,j1) for j1 in jets if j1!=j and j1.pt > 15 and j1.puId > 0 and j1.jetId > 0] or  [999]) 
#	      minDeltaR=j.area
	      b=next((b for b in self.deltaRbins if b>minDeltaR),self.deltaRbins[-1])
	      genpt=genjets[j.genJetIdx].pt #f j.genJetIdx!=-1 and j.genJetIdx<len(genjets) else 0
	      jpt=j.pt
	      if genpt > 0 :
#		 print self.calibHistos["%s_%s"%(u,b)]
#		 print jpt/genpt,j.pt,abs(j.eta)
		 bb=self.calibHistos["%s_%s_%s"%(u,b,fl)].FindBin(jpt/genpt,log(genpt),abs(genjets[j.genJetIdx].eta))
		 target=self.calibHistos["%s_%s_%s"%(u,b,fl)].GetBinContent(bb)
		 nominal=self.calibHistos["central_%s_%s"%(b,fl)].GetBinContent(bb)	
		 if nominal > 2 and target > 2:
			 jetUn*=target/nominal
		 else :
		    print "stat is not sufficient (nominal, target,jpt,genpt,minDeltaR,b,j.eta,fl)" , nominal, target,jpt,genpt,minDeltaR,b,j.eta,fl
		    self.misstarget+=target
		    self.missnominal+=nominal
		    self.miss+=1
            self.out.fillBranch("EventWeight_jecUncert%s"%u, jetUn)

        return True
allUncerts=["Total"]
allUncerts2=[
        "AbsoluteStat",
        "AbsoluteScale",
        "AbsoluteFlavMap",
        "AbsoluteMPFBias",
        "Fragmentation",
        "SinglePionECAL",
        "SinglePionHCAL",
        "FlavorQCD",
        "TimePtEta",
        "RelativeJEREC1",
        "RelativeJEREC2",
        "RelativeJERHF",
        "RelativePtBB",
        "RelativePtEC1",
        "RelativePtEC2",
        "RelativePtHF",
        "RelativeBal",
        "RelativeFSR",
        "RelativeStatFSR",
        "RelativeStatEC",
        "RelativeStatHF",
        "PileUpDataMC",
        "PileUpPtRef",
        "PileUpPtBB",
        "PileUpPtEC1",
        "PileUpPtEC2",
        "PileUpPtHF",
        "PileUpMuZero",
        "PileUpEnvelope",
        "SubTotalPileUp",
        "SubTotalRelative",
        "SubTotalPt",
        "SubTotalScale",
        "SubTotalAbsolute",
        "SubTotalMC",
        "Total",
        "TotalNoFlavor",
        "TotalNoTime",
        "TotalNoFlavorNoTime",
        "FlavorZJet",
        "FlavorPhotonJet",
        "FlavorPureGluon",
        "FlavorPureQuark",
        "FlavorPureCharm",
        "FlavorPureBottom",
        "TimeRunBCD",
        "TimeRunEF",
        "TimeRunG",
        "TimeRunH",
        "CorrelationGroupMPFInSitu",
        "CorrelationGroupIntercalibration",
        "CorrelationGroupbJES",
        "CorrelationGroupFlavor",
        "CorrelationGroupUncorrelated",
]

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

# python looper
# you can re-use the uncertainty values in modules running after this one in the same event loop
jecEventWeightCalib = lambda : jecEventWeights(uncerts=allUncerts,calibrate=True )
jecEventWeight = lambda : jecEventWeights(uncerts=allUncerts,calibrate=False )
#jecEventWeightUncertAll = lambda : jecEventWeights( "Summer16_23Sep2016V4_MC",allUncerts)

