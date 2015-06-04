# Author: Erin C. McKiernan
# Code adapted from Neo IO documentation https://pythonhosted.org/neo/io.html 
# Last modified: June 3, 2015

# import packages
from matplotlib import pyplot as plt
from neo import io
import os

# specify directory name
dirname = '/home/erin/manuscripts/inprep/EKI-REVISION/repo'


# reading and plotting recordings in ABF (Axon) format
def readABF(recname = 'ABF-files/09721000.abf'):	
    filename= os.path.join(dirname,recname)
    r = io.AxonIO(filename)
    bl = r.read_block(lazy=False,cascade=True)
    print bl.segments
    print bl.segments[0].analogsignals
    print bl.segments[0].eventarrays
    
    for seg in bl.segments:
        siglist=seg.analogsignals
        timepoints=siglist[0].times

        plt.figure()
        plt.plot(timepoints,siglist[0])
        plt.plot(timepoints,siglist[1])
        plt.xlim(160,280)
        plt.xlabel('Time (seconds)')
        plt.ylabel('Voltage (mV)')

        plt.show()
        
    return

# reading and plotting recordings in SMR (Spike2) format
def readSMR(recname = 'SMR-files/09706000.SMR', xmin=163, xmax=276, ymin=-70, ymax=0):		
    filename= os.path.join(dirname,recname)
    r = io.Spike2IO(filename)
    bl = r.read(lazy=False,cascade=True)[0]
    #print bl.segments
    #print bl.segments[0].analogsignals
    # print bl.segments[0].eventarrays
    
    for seg in bl.segments:
        siglist=seg.analogsignals
        timepoints=siglist[0].times

        plt.figure(figsize=(18,5))
        plt.plot(timepoints,siglist[0])
        plt.plot(timepoints,siglist[1])
        plt.xlim(xmin,xmax)
        plt.ylim(ymin,ymax)
        plt.xlabel('Time (seconds)')
        plt.ylabel('Voltage (mV)')

        plt.show()
        
    return
