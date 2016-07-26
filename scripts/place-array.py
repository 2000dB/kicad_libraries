import sys
import re
import math

from pcbnew import *

# Settings
# units are mm
master = ['U1', 'R1', 'R2', 'R3']
xNum = 4
xSpacing = 100
scale = 1000000. # mm



def moveArray(part, master):
    basePosition = None
    interval = 0
    
    for p in master:
        if p.startswith(part.rstrip('0123456789')[0]):
            interval += 1

    #Get base position
    for m in modules:
        reference = m.GetReference()
        if reference == part:
            basePosition = tuple(x/scale for x in m.GetPosition())
            baseOrientation = m.GetOrientation()
            break

    print "----------------------"
    print part
    print 'interval: ' + str(interval)
    print 'base pos: ',
    print basePosition,
    print ', base rot: ',
    print baseOrientation

    moveClones(part, interval, basePosition, baseOrientation)


def moveClones(part, interval, basePosition, baseOrientation):
    refCount = 0

    for i in range(xNum):
        for m in modules:
            reference = m.GetReference()
            cloneRef = part.rstrip('0123456789')[0] + str(int(part[len(part.rstrip('0123456789')[0])]) + interval * (refCount+1))

            if not reference == cloneRef:
                continue


            refCount += 1
            
            position = tuple(x/scale for x in m.GetPosition())
        
            newPosition = (basePosition[0] + xSpacing * refCount, basePosition[1])
            newPosition = tuple(x * scale for x in newPosition)
            point = wxPoint(newPosition[0], newPosition[1])
            
            print reference
            print point
            m.SetPosition(point)
            m.SetOrientation(baseOrientation)
            
        

pcb = GetBoard()
modules = pcb.GetModules()

for p in master:
    moveArray(p, master)
    
    
pcb.Save('/Users/vdb/Desktop/a.kicad_pcb')
