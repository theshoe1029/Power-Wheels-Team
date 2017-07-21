import serial, struct, os, math, pygame, time, sys
import Tkinter as tk
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
pygame.display.set_caption('Follow Wall')

arduino = serial.Serial('COM9')
print(arduino.name)

def turnRobot(direction):
        global turn
        turn = turn + (1 * direction)
        arduino.write("t")
        arduino.write(turn)
        arduino.write("\n")

def keyboard():
        for event in pygame.event.get():
            
            # determin if X was clicked, or Ctrl+W or Alt+F4 was used 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                        arduino.write("m10\n")
                        print("Throttle on")
                elif event.key == pygame.K_s:
                        arduino.write("m-10\n")
                        print("Throttle back")
                elif event.key == pygame.K_e:
                        arduino.write("m0\n")
                        print("Throttle off")

                if event.key == pygame.K_a:
                        print("Turning left")
                elif event.key == pygame.K_d:
                        arduino.write("Turning right")

                if event.key == pygame.K_q:
                        arduino.close()
                        pygame.quit()
                        sys.exit()

#Initialize the sweep sensor
with Sweep('COM4')as sweep:
        #Set the sweep motor speeds and start scanning
        sweep.set_motor_speed(5)
        sweep.set_sample_rate(500)
        sweep.start_scanning()

        speed = 0
        target = 0
        summation = 0
        angleAvg = 0
        numAngles = 0
        
        while True:
                pygame.font.init()
                
                #Refresh the screen after each scan
                screen.fill(WHITE)
                for scan in sweep.get_scans():
                        #Store samples in scan array
                        scans = scan.samples[:]
                        
                        #Loop for each sample
                        for i in range(len(scans)):
                                #Store direction property of each sample in angles array
                                angles = str(scans[i][0])
                                #Remove last three digits of anglea
                                if(len(angles[:]) == 6):
                                        angleArray = int(angles[:3])
                                else: 
                                        angleArray = int(angles[:2])

                                summation += angleArray
                                numAngles += 1

                                if(numAngles != 0):
                                        target = summation/numAngles
                                
                                #Calculate x and y components of each sample based on basic trig
                                if scans[i][2] > 100:
                                        x = int(0.75 * (scans[i][1] * math.cos(angleArray * math.pi / 180)))
                                        y = int(0.75 * (scans[i][1] * math.sin(angleArray * math.pi / 180)))

                                        if(target < 180 and target > 0 and scans[i][1] < 100):
                                                speed = 10
                                                arduino.write("t-20\n")
                                                print("Wall is in range")
                                                pygame.draw.circle(screen, (255, 0, 0), [800 - (y + 400), 600 - (x + 300)], 2)
                                        else:
                                                speed = 0
                                                arduino.write("t20\n")
                                                print("Wall out of range")
                                                #Draw circle on screen based on x and y components
                                                pygame.draw.circle(screen, BLACK, [800 - (y + 400), 600 - (x + 300)], 2)
                        
                        #Update screen with all the points from the sample
                        pygame.display.update()
                        screen.fill(WHITE)
                        keyboard()

                        if(numAngles != 0):
                                target = summation/numAngles

                        if(target > 0):
                                arduino.write("t10\n")
                        else:
                                arduino.write("t-10\n")
                        
                        arduino.write("m%d\n"%speed)
                        
                        print("Target speed %d"%speed)
                        print("Target angle %d"%target)

                        summation = 0
                        numAngles = 0
