import serial, struct, os, math, pygame, time
from sweeppy import Sweep
from sweeppy import Scan
from sweeppy import Sample
from array import array
from pygame.locals import *

pygame.init()

#This sets up the colors and size of the pygame window
WHITE = (255,255,255)
BLACK = (0,0,0)
width = 800
height = 600

#This creates the pygame window and sets its background
screen = pygame.display.set_mode((width,height))
screen.fill(WHITE)
pygame.display.update()
pygame.display.set_caption('Sweep Visualizer')

#Initialize the sweep sensor
with Sweep('/dev/ttyUSB0') as sweep:

	#Set the sweep motor speeds and start scanning
	sweep.set_motor_speed(5)
	sweep.set_sample_rate(2)
	sweep.start_scanning()
	
	while True:
		#Refresh the screen after each scan
		screen.fill(WHITE)
		for scan in sweep.get_scans():
			#Store samples in scan array
			scans = scan.samples[:]
			
			#Loop for each sample
			for i in range(len(scans)):
				#Store direction property of each sample in angles array
				angles = str(scans[i][0])
				#Remove last three digits of angle
				if(len(angles[:]) == 6):
					angleArray = int(angles[:3])
				else: 
					angleArray = int(angles[:2])
				#Calculate x and y components of each sample based on basic trig
				if scans[i][2] > 100:
					x = int(0.75 * (scans[i][1] * math.cos(angleArray * math.pi / 180)))
					y = int(0.75 * (scans[i][1] * math.sin(angleArray * math.pi / 180)))
				
					#Draw circle on screen based on x and y components
					pygame.draw.circle(screen, BLACK, [x + 400,y + 300], 2)
				else:
					pygame.draw.circle(screen, WHITE, [x + 400,y + 300], 2)
			
			#Update screen with all the points from the sample
			pygame.display.update()
			screen.fill(WHITE)
