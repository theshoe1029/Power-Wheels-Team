import serial, struct, os, math, pygame, time
from sweeppy import Sweep
from sweeppy import Scan
from sweeppy import Sample
from array import array
from pygame.locals import *

#Initialize the sweep sensor
with Sweep('COM5') as sweep:

    #Set the sweep motor speeds and start scanning
    sweep.set_motor_speed(5)
    sweep.set_sample_rate(2)
    sweep.start_scanning()
    
    while True:
        for scan in sweep.get_scans():
            scans = scan.samples[:]
            
            for i in range(len(scans)):
                angles = str(scans[i][0])
            if(len(angles[:]) == 6):
                adjustedAngles = int(angles[:3])
            else: 
                adjustedAngles = int(angles[:2])
                
            print(adjustedAngles)
