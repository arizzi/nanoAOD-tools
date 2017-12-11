import ROOT
import os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True
from math import *
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class jecEventWeightsValidation(Module):
    def __init__(self,uncerts=["Total"]):
	self.uncerts=uncerts
        self.hf=ROOT.TFile("valid.root","recreate")
	self.h1=ROOT.TH1F("mass","mass",100,0,250)
	self.h2=ROOT.TH1F("mass_highpt","mass for pt > 150",100,0,250)
	self.h3=ROOT.TH1F("pt","mass for pt > 150",100,0,250)
	self.h1e=ROOT.TH1F("e_mass","mass (evt weight)",100,0,250)
	self.h2e=ROOT.TH1F("e_mass_highpt","mass for pt > 150 (evt weight)",100,0,250)
	self.h3e=ROOT.TH1F("e_pt","mass for pt > 150 (evt weight)",100,0,250)
        self.h1u=ROOT.TH1F("u_mass","mass (uncorr)",100,0,250)
        self.h2u=ROOT.TH1F("u_mass_highpt","mass for pt > 150 (uncorr)",100,0,250)
        self.h3u=ROOT.TH1F("u)pt","mass for pt > 150 (uncorr)",100,0,250)
	self.hgr=ROOT.TH1F("genreco","recoge",100,0,3)


    def beginJob(self):
	self.count=0.
	self.sumw=0.
	pass

    def endJob(self):
	print "Normalization", self.count/self.sumw
	self.h1e.Scale(self.count/self.sumw)
	self.h2e.Scale(self.count/self.sumw)
	self.h3e.Scale(self.count/self.sumw)
	c1=ROOT.TCanvas()
	self.h1.Draw()
	self.h1e.Draw("sames")
	self.h1u.SetLineColor(3)	
	self.h1u.Draw("sames")
	c1.SaveAs("~/scratch0/web/c1.png")
	c2=ROOT.TCanvas()
	self.h2.Draw()
	self.h2e.Draw("sames")
	self.h2u.SetLineColor(3)	
	self.h2u.Draw("sames")
	c2.SaveAs("~/scratch0/web/c2.png")
	c3=ROOT.TCanvas()
	self.h3.Draw()
	self.h3e.Draw("sames")
	self.h3u.SetLineColor(3)	
	self.h3u.Draw("sames")
	c3.SaveAs("~/scratch0/web/c3.png")
	c5=ROOT.TCanvas()
	self.hgr.Draw()
	c5.SaveAs("~/scratch0/web/c5.png")
	
	if hasattr(self,"hf") :
		self.hf.Write()

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
	pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = Collection(event, "Jet")
        weights = Object(event, "EventWeight")
        genjets = Collection(event, "GenJet")
	selJets = [ j for j in jets if j.pt > 25 and j.puId > 0 and j.jetId > 0 and abs(j.eta) < 2.4 ]
	selJets.sort(key= lambda x : x.btagCMVA)
	self.count+=1
	self.sumw+=weights.jecUncertTotal
	if len(selJets) >= 2 :
	     if selJets[0].genJetIdx >=0 and selJets[0].genJetIdx < len(genjets):
		     self.hgr.Fill(selJets[0].pt/genjets[selJets[0].genJetIdx].pt)
	     if selJets[1].genJetIdx >=0 and selJets[1].genJetIdx < len(genjets):
		     self.hgr.Fill(selJets[1].pt/genjets[selJets[1].genJetIdx].pt)
	     j1=ROOT.TLorentzVector()
	     j2=ROOT.TLorentzVector()
	     j1.SetPtEtaPhiM(selJets[0].pt,selJets[0].eta,selJets[0].phi,selJets[0].mass)
	     j2.SetPtEtaPhiM(selJets[1].pt,selJets[1].eta,selJets[1].phi,selJets[1].mass)
	     h=j1+j2

	     self.h1u.Fill(h.M())
	     self.h1e.Fill(h.M(),weights.jecUncertTotal)
	     self.h3u.Fill(h.Pt())
	     self.h3e.Fill(h.Pt(),weights.jecUncertTotal)
	     if h.Pt() > 150 :
		     self.h2e.Fill(h.M(),weights.jecUncertTotal)
		     self.h2u.Fill(h.M())

	selJets = [ j for j in jets if (j.pt*(1.+j.jecUncertTotal)) > 25 and j.puId > 0 and j.jetId > 0 and abs(j.eta) < 2.4 ]
	selJets.sort(key= lambda x : x.btagCMVA)
	if len(selJets) >= 2 :
             j1c=ROOT.TLorentzVector()
             j2c=ROOT.TLorentzVector()
             j1c.SetPtEtaPhiM(selJets[0].pt*(1.+selJets[0].jecUncertTotal),selJets[0].eta,selJets[0].phi,selJets[0].mass)
             j2c.SetPtEtaPhiM(selJets[1].pt*(1.+selJets[1].jecUncertTotal),selJets[1].eta,selJets[1].phi,selJets[1].mass)
             hc=j1c+j2c

	     self.h1.Fill(hc.M())
	     self.h3.Fill(hc.Pt())
	     if hc.Pt() > 150 :
		     self.h2.Fill(hc.M())

	     

	     
	    	
        return True


allUncerts=["Total"]
jecEventWeightValidation = lambda : jecEventWeightsValidation(uncerts=allUncerts )

