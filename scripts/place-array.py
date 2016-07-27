import sys
import re
import math

from pcbnew import *

# Settings
# units are mm
master = ['LED1', 'C1', 'C2', 'C3', 'C4', 'U1', 'D1', 'D2', 'R1', 'L1']
xNum = 8
yNum = 8
xSpacing = 57.14
ySpacing = 57.14
scale = 1000000. # mm


def moveArray(part, master):
    basePosition = None
    interval = 0
    
    for p in master:
        if p.rstrip('0123456789') == part.rstrip('0123456789'):
            interval += 1

    #Get base position
    for m in modules:
        reference = m.GetReference()
        if reference == part:
            basePosition = tuple(x/scale for x in m.GetPosition())
            baseOrientation = m.GetOrientation()
            break

    lastItem = int(part[len(part.rstrip('0123456789'))]) + interval * xNum * yNum - interval

    print "----------------------"
    print part
    print 'interval: ' + str(interval),
    print 'last item: ' + str(lastItem)
    print 'base pos: ',
    print basePosition,
    print ', base rot: ',
    print baseOrientation


    moveClones(part, interval, basePosition, baseOrientation, lastItem)


def moveClones(part, interval, basePosition, baseOrientation, lastItem):
    refCount = 0

    
    for m in modules:
        reference = m.GetReference()
        cloneRef = part.rstrip('0123456789') + str(int(part[len(part.rstrip('0123456789'))]) + interval * min(refCount, lastItem))
        
        if reference == cloneRef:
            position = tuple(x/scale for x in m.GetPosition())

            xPos = refCount / yNum
            yPos = refCount % yNum
            
            newPosition = (basePosition[0] + xSpacing * xPos, basePosition[1] + ySpacing * yPos)
            newPosition = tuple(x * scale for x in newPosition)
            point = wxPoint(newPosition[0], newPosition[1])

            print refCount,
            print "(" + str(xPos) + "," + str(yPos) + ")",
            print cloneRef,
            print reference,
            print point

            m.SetPosition(point)
            m.SetOrientation(baseOrientation)

            refCount += 1
            
        

pcb = GetBoard()
modules = pcb.GetModules()

for p in master:
    moveArray(p, master)
    
    
pcb.Save('/Users/vdb/Desktop/a.kicad_pcb')
