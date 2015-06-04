# Author: Erin C. McKiernan
# Last modified: 1 June 2015


# import packages
from __future__ import division
import csv
import scipy as sc
import scipy.stats
import scipy.interpolate
import numpy as np
import pylab as gr
import string

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 20}


# Select csv files for analysis.  
# Note: It is assumed that wildtype and EKI burst times are stored in
# separate csv files.
csvFiles={'EKI':'MN1-Ib_EKI.csv','WT':'MN1-Ib_WT.csv'}


# Extract data from the csv files 
def getCSVData(CSVfile,nHeaderLines=1):
    data = list()
    with open(CSVfile,'rb') as csvf:
        csvdata = csv.reader(csvf,delimiter=',', quotechar='|')
        nrows =0
        # Count the rows and get all the data into a numeric array.
        for row in csvdata:
            # Take care of the header row. If there are more header
            # rows, change the 1 to the number of header rows.
            if nrows>=nHeaderLines:
                data.append(map(float,string.split(string.join(row[1:]))))
            nrows = nrows+1
    return data


# Test if the averages of CDFs are monotonically increasing.
# Note: CDFs should always be increasing - this is used for debugging.
def testMonotonicIncrease(aRRay):
    if len(gr.find(gr.diff(aRRay)<0))>0:
        print 'The array is NOT monotonic.'
        x=0
    else: 
        print 'The array is non-decreasing.'
        x=1
    return x
    

# Calculate the burst measures from one data set. The input argument
# is a list whose elements are realizations of a bursting process
# containing the beginning and end of each burst as they occurred.
def calcBurstMeasures(data):
    """
    Example:
    dataEKI=getCSVData(csvFiles['EKI'])
    bMeasures= calcBurstMeasures(dataEKI)
    """
    measures=dict()
    nrows = len(data)
    burstStarts=list()
    burstStops=list()
    burstDurs=list()
    cycleDurs=list()
    burstFreqs=list()
    dutyCycles=list()
    qIs=list()


    # Burst duration - time elapsed from start to end of one burst
    # Cycle duration - time elapsed from start of one burst to start of next 
    # Duty cycle - burst duration divided by cycle duration 
    # Quiescence interval - time elapsed from end of burst to start of next
    for n in range(0,nrows):
        nBursts = len(data[n])
        burstStarts.append(sc.array(data[n][0::2]))
        burstStops.append(sc.array(data[n][1::2]))
        burstDurs.append(burstStops[n]-burstStarts[n])
        cycleDurs.append(sc.diff(burstStarts[n]))
        burstFreqs.append(1/cycleDurs[n][:-1])
        dutyCycles.append(burstDurs[n][:-1]/cycleDurs[n])
        qIs.append(burstStarts[n][1:]-burstStops[n][:-1])
        if 0:
            print 'Burst durations:' 
            print burstDurs[n]
            print 'Cycle durations:' 
            print cycleDurs[n]
            print 'Duty cycles:' 
            print dutyCycles[n]
            print 'Quiescence intervals:' 
            print qIs[n]
            print '\n'
        
    measures={'burstDur':burstDurs,
              'cycleDur':cycleDurs,
              'dutyCycle':dutyCycles,
              'qI':qIs}
    return measures


# Set intervals and get bins for each measure. 
def calcBins(): 
    minburstdur=1.; maxburstdur = 50.; burstdur_bin=1.0;
    mincycledur=1.; maxcycledur = 50.; cycledur_bin=1.0;
    minduty = 0; maxduty=1.0; dutycycle_bin=0.04;
    minqi = 0; maxqi=50.0; qi_bin=1.0;
    bins = dict()
    #
    bins['burstDur']=sc.arange(minburstdur,maxburstdur,burstdur_bin);
    bins['cycleDur']=sc.arange(mincycledur,maxcycledur,cycledur_bin);
    bins['dutyCycle']=sc.arange(minduty,maxduty,dutycycle_bin)
    bins['qI']=sc.arange(minqi, maxqi, qi_bin)
    #
    #return bins, burstdur_bin, cycledur_bin, dutycycle_bin, qi_bin
    return bins

# Calculate cumulative distribution functions (CDFs).
def calcCDFs(sampleList,binEdges):
    """
    Example:
    dataEKI = getCSVData(csvFiles['EKI'])
    bMeasures = calcBurstMeasures(dataEKI)
    cdfs =calcCDFs(sampleList=bMeasures['burstDur'],binEdges=bins['burstDur'])
    """
    nSamples=len(sampleList)
    nBinPts = len(binEdges)
    cdfs=list()
    for n in range(nSamples):
        nPts=sc.float64(len(sampleList[n]))
        cdfs.append(sc.zeros(nBinPts))
        for m in range(0,nBinPts):
            samp=sampleList[n]
            cdfs[n][m] = len(sc.where(samp<=binEdges[m])[0])/nPts 
    return sc.array(cdfs)


# Plot cumulative distribution functions (CDFs).
def graphCDFsOneSample(cdfs,binEdges,ax,grpColor='r',indivMark=':',strLabel='avg'):
    """
    fig=gr.figure(num=figNum,figsize=(9,10))
    gr.ioff();
    ax1= fig.add_subplot(111)
    cdfs =calcCDFs(sampleList=bMeasures['burstDur'],binEdges=bins['burstDur'])
    graphCDFsOneSample(cdfs,binEdges=bE,ax=ax1,grpColor='r',indivMark=':',strLabel='avg')
    gr.ion()
    gr.draw()
    """
    nSamples=len(cdfs)
    cdfAvg=cdfs.mean(0)
    #
    for n in range(nSamples):
        ax.plot(binEdges,cdfs[n],grpColor+indivMark,lw=1)        
    ax.plot(binEdges,cdfAvg,grpColor,alpha=0.6,lw=3,label=strLabel)
    ax.legend(loc='lower right')    
    return ax


# Multipanel figure showing different comparisons between cdfs. 
# Assumes you get 4 lists of pairs of cdfs, 1 for each measure.
def graphMultiCDF(bins,bMeasures):
    colors={'EKI':'r','WT':'b'}
    measureNames= bMeasures['WT'].keys()
    measureNames.sort()
    wholeNames=['Burst duration', 'Cycle duration', 'Duty cycle', 'Quiescence interval']
    cdfs={'EKI': dict(), 'WT':dict() }
    for k1 in cdfs.keys():
        for k2 in measureNames:
            cdfs[k1][k2]=calcCDFs(sampleList=bMeasures[k1][k2],binEdges=bins[k2])

    f4= gr.figure(figsize=(15,15))
    gr.ioff()
    r=2; c=2; ax1=list()
    for mm in range(r*c):
        ax1.append(f4.add_subplot(r,c,mm+1))
        for k1 in cdfs.keys():
            str0=k1
            myCDF= cdfs[k1][measureNames[mm]]
            myBins=bins[measureNames[mm]]
            graphCDFsOneSample(cdfs=myCDF, binEdges=myBins, ax=ax1[mm],grpColor=colors[k1], strLabel=str0)
            ax1[mm].set_title(wholeNames[mm])
            if measureNames[mm]!='dutyCycle':
                ax1[mm].set_xlabel('secs')
                ax1[mm].set_xlim(0,30)

    gr.ion(); gr.draw()
    return 


# Calculate average relative frequencies
def calcAvgRelFreq(Xbins, Xmeasures):
    p = dict()
    nMeasures = len(Xmeasures)
    nBins = len(Xbins)
    rf = sc.zeros((nMeasures, nBins-1),float)
    for n in range(0,nMeasures):
        N = len(Xmeasures[n])
        rf[n,:] =sc.histogram(Xmeasures[n],bins=Xbins)[0]/float(N)

    p['relFreqs']=rf
    p['avgRelFreq'] = sc.mean(rf,0)
    return p


# Set intervals and get bins to calculate relative frequencies. 
def getRelFreqs(bins): 
    burstMeasures=dict();
    burstRFs=dict();
    for x in csvFiles.items():
        print x[1]
        burstMeasures[x[0]] = calcBurstMeasures(getCSVData(x[1],1))
        burstRFs[x[0]] = dict()
        burstRFs[x[0]]['burstDur']=calcAvgRelFreq(bins['burstDur'],burstMeasures[x[0]]['burstDur']);
        burstRFs[x[0]]['cycleDur']=calcAvgRelFreq(bins['cycleDur'],burstMeasures[x[0]]['cycleDur']);
        burstRFs[x[0]]['dutyCycle']=calcAvgRelFreq(bins['dutyCycle'],burstMeasures[x[0]]['dutyCycle']);
        burstRFs[x[0]]['qI']=calcAvgRelFreq(bins['qI'],burstMeasures[x[0]]['qI']);
    return burstRFs


# Plots histograms for group comparisons.
def pdfComparison(label1='WT',label2='EKI',maxRF=0.33,alpha1=1,alpha2=1,skinfactor=0.3):

    burstdur_bin=1.0; cycledur_bin=1.0; dutycycle_bin=0.04; qi_bin=1.0;
    bins=calcBins()
    burstRFs=getRelFreqs(bins)
    rows=2; cols =2;
    ax=list()
    f0=gr.figure(figsize=(13,13))
    gr.ioff()
    for n in range(0,rows*cols):
        ax.append(f0.add_subplot(rows,cols,n+1))
        
    maxTime=30.0
    # burst duration
    binw=burstdur_bin
    shift=binw*(1-skinfactor)/2.0
    ax[0].bar(bins['burstDur'][:-1],burstRFs[label1]['burstDur']['avgRelFreq'],width=binw,color='w' ,alpha=alpha1,label=label1)
    ax[0].bar(bins['burstDur'][:-1]+shift,burstRFs[label2]['burstDur']['avgRelFreq'],width=binw*skinfactor,color='k' ,alpha=alpha2,label=label2)
    ax[0].legend(shadow=True, fancybox=True, ncol=1, prop={'size':16})
    ax[0].set_xlim(0,maxTime)
    ax[0].set_ylim(0,maxRF)
    ax[0].set_xlabel('Burst duration (secs)')
    ax[0].set_ylabel('Relative frequency')
    # cycle duration
    binw=cycledur_bin
    shift=binw*(1-skinfactor)/2.0
    ax[1].bar(bins['cycleDur'][:-1],burstRFs[label1]['cycleDur']['avgRelFreq'], width=binw,color='w' ,alpha=alpha1,label=label1)
    ax[1].bar(bins['cycleDur'][:-1]+shift,burstRFs[label2]['cycleDur']['avgRelFreq'], width=binw*skinfactor,color='k' ,alpha=alpha2,label=label2)
    ax[1].legend(shadow=True, fancybox=True, ncol=1, prop={'size':16})
    ax[1].set_xlim(0,maxTime)
    ax[1].set_ylim(0,maxRF)
    ax[1].set_xlabel('Cycle duration (secs)')
    # duty cycle 
    binw=dutycycle_bin
    shift=binw*(1- skinfactor)/2.0
    ax[2].bar(bins['dutyCycle'][:-1],burstRFs[label1]['dutyCycle']['avgRelFreq'], width=binw,color='w' ,alpha=alpha1,label=label1)
    ax[2].bar(bins['dutyCycle'][:-1]+shift, burstRFs[label2]['dutyCycle']['avgRelFreq'], width=binw*skinfactor,color='k' ,alpha=alpha2,label=label2)
    ax[2].legend(shadow=True, fancybox=True, ncol=1, prop={'size':16})
    ax[2].set_xlim(0,1)
    ax[2].set_ylim(0,maxRF)
    ax[2].set_xlabel('Duty cycle')
    ax[2].set_ylabel('Relative frequency')
    # quiescence interval
    binw=qi_bin
    shift=binw*(1-skinfactor)/2.0
    ax[3].bar(bins['qI'][:-1],burstRFs[label1]['qI']['avgRelFreq'],width=binw,color='w' ,alpha=alpha1,label=label1)
    ax[3].bar(bins['qI'][:-1]+shift,burstRFs[label2]['qI']['avgRelFreq'], width=binw*skinfactor,color='k' ,alpha=alpha2,label=label2)
    ax[3].legend(shadow=True, fancybox=True, ncol=1, prop={'size':16})
    ax[3].set_xlim(0,maxTime)
    ax[3].set_ylim(0,maxRF)
    ax[3].set_xlabel('Quiescence interval (secs)')
    f0.text(0.055,0.95,'A',size=20)
    f0.text(0.52,0.95,'B',size=20)
    f0.text(0.05,0.5,'C',size=20)
    f0.text(0.52,0.5,'D',size=20)

    f0.subplots_adjust(left=0.12, bottom=0.1, right=0.95, top=0.95, wspace=0.2, hspace=0.2)

    gr.ion(); gr.draw()
    gr.ion(); gr.draw()
    return 




