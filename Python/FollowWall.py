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
        
        position = 0
        wall_distance = 150
        kp = 0.01
        
        while True:
                #Refresh the screen after each scan
                screen.fill(WHITE)

                for scan in sweep.get_scans():
                        #Store samples in scan array
                        scans = scan.samples[:]

                        error = 0
                        distance_avg = 0
                        summation = 0
                        num_distances = 0

                        #Loop for each sample
                        for i in range(len(scans)):
                                #Store direction property of each sample in angles array
                                angle = str(scans[i][0])
                                adjustedAngle = int(angle)/1000
                                
                                #Calculate x and y components of each sample based on basic trig
                                if scans[i][2] > 100:
                                        x = int(scans[i][1] * math.cos(adjustedAngle * math.pi / 180))
                                        y = int(scans[i][1] * math.sin(adjustedAngle * math.pi / 180))

                                        if(adjustedAngle < 40 and adjustedAngle > 20 and x < 500 and x > 10):
                                                summation = summation + x
                                                num_distances = num_distances + 1
                                                        
                                                pygame.draw.circle(screen, (0, 0, 255), [800 - (y + 400), 600 - (x + 300)], 5)
                                        else:
                                                #Draw circle on screen based on x and y components
                                                pygame.draw.circle(screen, BLACK, [800 - (y + 400), 600 - (x + 300)], 2)


                        distance_avg = wall_distance
                        if(num_distances != 0):
                                distance_avg = summation/num_distances
                                
                        error = distance_avg - wall_distance
                                
                        position = position + (error * kp)

                        pygame.draw.line(screen, (0, 255, 0), (400 - wall_distance,0), (400 - wall_distance, 600), 1)

                        pygame.draw.line(screen, (255, 0, 0), (400 - distance_avg,0), (400 - distance_avg, 600), 1)
                        
                        #Update screen with all the points from the sample
                        pygame.display.update()
                        screen.fill(WHITE)
                        keyboard()
                        
                        if(position > 10):
                                position = 10
                        if(position < -10):
                                position = -10

                        arduino.write("t%d\n"%position)
                        
                        print("Target angle %d"%position)
                        print("Error %d"%error)


                 


