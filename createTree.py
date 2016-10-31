

import ROOT
import array 
import numpy
import matplotlib.pyplot as pyplot
import os
#import scipy
import peakutils

from scipy.ndimage.filters import maximum_filter
filter_win_size = 15
peak_intensity_threshold = 4
#peak_intensity_threshold = 2

import sys
import time

#set the files numbers 
#13,14,15 - 1mV ch2, 1mV ch3 , timePeakPosTail2 = 452 
#18,19,20 - 15mV ch2, 1mV ch3,timePeakPosTail2 = 470
runs = {18,19,20}
N=9999

#loop over the files 
for run in runs:
  inFile = ("run%s.txt" % run)
  outFile = ("run%s.root" % run)
  print "reading file: %s" % inFile
  os.system("mkdir plots_run%s" % run)

  ### must be read from scope settings
  #ALLOcate:WAVEform:REF<x>
  HorizDivis = 500#add to file data file 
  voltageScaleTrig = 200.*5./128 #[mV]
  vScale2 = 1 #1 [mV]
  voltageScale2 = 1.*5./128
  timePeakPosTail2 = 452 
  
  voltageScale3 = 1.*5./128
  timeScale = 1000/500 #[ns]
  
  
  
  if(run == 18 or run == 19 or run == 20):
    vScale2 = 15 #[mv]
    voltageScale2 = 15.*5./128
    timePeakPosTail2 = 470
  
  rootFile = ROOT.TFile( outFile, 'recreate' )
  rootTree = ROOT.TTree( 'tree', 'tree for scope signals analysis' )
  eventNr = array.array( 'i', [ 0 ] )
  isTrig = array.array( 'i', [ 0 ] )
  isCh2 = array.array( 'i', [ 0 ] )
  isCh3 = array.array( 'i', [ 0 ] )
  t1 = array.array( 'f', [ 0 ] )
  t2 = array.array( 'f', [ 0 ] )
  t3 = array.array( 'f', [ 0 ] )
  avg1 = array.array( 'f', [ 0 ] )
  avg2 = array.array( 'f', [ 0 ] )
  avg3 = array.array( 'f', [ 0 ] )
  signal2 = array.array( 'f', [ 0 ] )
  signal3 = array.array( 'f', [ 0 ] )
  dtT2 = array.array( 'f', 10*[ 0. ] )
  rootTree.Branch('eventNr', eventNr, 'eventNr/I')
  rootTree.Branch('isTrig',isTrig,'isTrig/I')
  rootTree.Branch('isCh2',isCh2,'isCh2/I')
  rootTree.Branch('isCh3',isCh3,'isCh3/I')  
  rootTree.Branch('t1',t1,'t1/F')
  rootTree.Branch('t2',t2,'t2/F')
  rootTree.Branch('t3',t3,'t3/F')
  rootTree.Branch('avg1',avg1,'avg1/F')
  rootTree.Branch('avg2',avg2,'avg2/F')
  rootTree.Branch('avg3',avg3,'avg3/F')
  rootTree.Branch('signal2',signal2,'signal2/F')
  rootTree.Branch('signal3',signal3,'signal3/F')
  
  #t.Branch( 'myval', d, 'myval[mynum]/F' )
  
  #book histograms
  h_pass2 = ROOT.TH1F("h_pass2","eff. vs thr. for ch2;thr., mV;eff.",100,0,6*vScale2)
  h_total2 = ROOT.TH1F("h_total2","eff. vs thr. for ch2;thr., mV;eff.",100,0,6*vScale2)
  h_signal2 = ROOT.TH1F("h_signal2","signal amplitude from ch2;Amplitude, mV;Entries",200,0,6*vScale2)
  h_t2 = ROOT.TH1F("h_t2","signal scope time from ch2;ns;Entries",500,0,1000)
  
  nTriggers = 0
  #loop over the lines
  source = open(inFile,'r')
  for line in source: #get line by line from txt file 
    lineArray = line.replace(',',' ').split()#split line to array
    lineIndicator = lineArray[0]
    
    lineArray.pop(0)
    if nTriggers>N:break
    
    if lineIndicator == ":CURV":
      
      isCh2[0] = -999
      isCh3[0] = -999
      t1[0] = -999
      t2[0] = -999
      t3[0] = -999
      signal2[0] = -999
      signal3[0] = -999
      
      
      eventNr[0] += 1
      print "\neventNr: ", eventNr[0]
      lineArray = map(int, lineArray) # convert string to int
      ch1 = lineArray[:HorizDivis]
      ch2 = lineArray[HorizDivis:2*HorizDivis]
      ch3 = lineArray[2*HorizDivis:3*HorizDivis]
      
      #set offset
      avg1[0] = numpy.mean(ch1[:150])
      avg2[0] = numpy.mean(ch2[:150])+0.3
      avg3[0] = numpy.mean(ch3[:150])+0.3
      
      for i in range(len(ch1)):ch1[i] -= avg1[0]
      for i in range(len(ch2)):ch2[i] -= avg2[0]
      for i in range(len(ch3)):ch3[i] -= avg3[0]
      
      
      diff_ch1 = numpy.diff(ch1)
      diff_ch1[diff_ch1>0]=0
      diff_ch1=abs(diff_ch1)
      indexes1 = peakutils.indexes(diff_ch1, thres=0.5, min_dist=10)
      
      if max(map(abs, ch1)) < 10 or len(indexes1)==0:
       isTrig[0] = 0
       rootTree.Fill()
       continue
      else: 
       isTrig[0] = 1
       nTriggers += 1
      
      t1[0] = indexes1[0]*timeScale
      
      
      if(max(map(abs, ch2)) <= peak_intensity_threshold): isCh2[0] = 0
      else: isCh2[0] = 1
      if(max(map(abs, ch3)) <= peak_intensity_threshold): isCh3[0] = 0
      else: isCh3[0] = 1
      
      ##plots
      #pyplot.clf()
      #pyplot.plot(ch1)
      #pyplot.plot(ch2)
      ##pyplot.plot(ch3)
      
      diff_ch1 = numpy.diff(ch1)
      diff_ch1[diff_ch1>0]=0
      diff_ch1=abs(diff_ch1)
      indexes1 = peakutils.indexes(diff_ch1, thres=0.5, min_dist=10)
      t1[0] = indexes1[0]*timeScale
      
      if isCh2[0]:
	data2 = numpy.array(-(numpy.array(ch2)))
	max_data2 = maximum_filter(data2, filter_win_size)
	min_data2 = -maximum_filter(-data2, filter_win_size)
	# select places where we detect maximum but not minimum -> we dont want long plateaus
	peak_mask2 = numpy.logical_and(max_data2 == data2, min_data2 != data2)
	# select peaks where we have enough elevation
	peak_mask2 = numpy.logical_and(peak_mask2, max_data2 - min_data2 > peak_intensity_threshold)
	# a trick to convert True to 1, False to -1
	peak_mask2 = peak_mask2 * 2 - 1
	# select only the up edges to eliminate multiple maximas in a single peak
	peak_mask2 = numpy.correlate(peak_mask2, [-1, 1], mode='same') == 2
	max_places2 = numpy.where(peak_mask2)[0]
	if(len(max_places2)>0):
	  signal2[0] = data2[max_places2[0]]
          startPos2 = max_places2[0]
	  startVal2 = signal2[0]
	  while startVal2 >= 0.3*signal2[0]:
	    startPos2 -= 1
	    startVal2 = data2[startPos2]
	  t2[0] = startPos2*timeScale
	  signal2[0] = data2[max_places2[0]]*voltageScale2
      
      #plots
      #r = range(data2.shape[0])
      #pyplot.plot(r, data2, 'k')
      #pyplot.plot(max_places2, data2[max_places2], 'xr')
      #pyplot.plot(startPos2,startVal2,marker = '*')
      #pyplot.grid()
      #pyplot.savefig(("plots_run%s/ch_plot%s.png" % (run , eventNr[0])))
      #pyplot.clf() # clear plot
      
      rootTree.Fill()
      
      if(isTrig[0]==1 and isCh2[0]==1 and t2[0]>0): h_t2.Fill(t2[0])
      if(isTrig[0]==1 and isCh2[0]==1 and t2[0]>0 and t2[0]<timePeakPosTail2): h_signal2.Fill(signal2[0])
      for i in range(h_pass2.GetNbinsX()):
        thr =  h_pass2.GetBinLowEdge(i+1)#+h_pass2.GetBinWidth(i+1)
        binCenter = h_pass2.GetBinCenter(i+1)
        thr = binCenter
        if(isTrig[0]==1):h_total2.Fill(binCenter)
        if(isTrig[0]==1 and isCh2[0]==1 and t2[0]>0 and t2[0]<timePeakPosTail2 and signal2[0]>thr):h_pass2.Fill(binCenter)
        
      
  if(ROOT.TEfficiency.CheckConsistency(h_pass2,h_total2)):h_eff2 = ROOT.TEfficiency(h_pass2,h_total2)
  h_eff2.SetName("h_eff2")
  h_eff2.SetTitle("eff. vs thr. for ch2;thr., mV;eff.")
  rootTree.Write()
  h_total2.Write()
  h_pass2.Write()
  h_eff2.Write()
  h_signal2.Write()
  h_t2.Write()
  
  
  rootFile.Close()

