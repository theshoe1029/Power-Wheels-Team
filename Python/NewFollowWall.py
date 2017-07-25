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

arduino = serial.Serial('COM7')
print(arduino.name)
right = False
max_turn = 28
wall_distance = 100
kp = 10
y_off = 300

def keyboard():
        for event in pygame.event.get():
            global right
            # determine if X was clicked, or Ctrl+W or Alt+F4 was used 
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_l:
                        right = False
                        print(right)

                if event.key == pygame.K_r:
                        right = True
                        print(right)

                if event.key == pygame.K_q:
                        arduino.close()
                        pygame.quit()
                        sys.exit()

#Initialize the sweep sensor
with Sweep('COM5')as sweep:
        
        #Set the sweep motor speeds and start scanning
        sweep.set_motor_speed(5)
        sweep.set_sample_rate(500)
        sweep.start_scanning()
        
        position = 0
           
        for scan in sweep.get_scans():
            screen.fill(WHITE)
            print(right);

            summation = 0
            num_distances = 0
            
            for sample in scan.samples:
                #print(sample)

                #Store direction property of each sample in angles array
                angle = sample.angle/1000

                x = int(sample.distance * math.sin(angle * math.pi / 180))
                y = int(sample.distance * math.cos(angle * math.pi / 180))
                    
                #Calculate x and y components of each sample based on basic trig
                if (y > 20):
                        if(y < 100 and y > -100 and x < 750 and x > 0 and right == False):
                                summation = summation + x
                                num_distances = num_distances + 1
                                        
                                pygame.draw.circle(screen, (0, 0, 255), [800 - (x + 400), 600 - (y + y_off)], 5)
                        elif(y < 100 and y > -100 and x < 0 and x > -750 and right == True):
                                summation = summation + x
                                num_distances = num_distances + 1
                                        
                                pygame.draw.circle(screen, (0, 0, 255), [800 - (x + 400), 600 - (y + y_off)], 5)
                        else:
                                #Draw circle on screen based on x and y components
                                pygame.draw.circle(screen, BLACK, [800 - (x + 400), 600 - (y + y_off)], 2)


            distance_avg = wall_distance
            if(num_distances != 0):
                    distance_avg = summation/num_distances
            pygame.draw.line(screen, (100, 100, 100), (400,0), (400, 600), 1)
            
            pygame.draw.rect(screen, (100, 100, 100), Rect(400-32, 600-(y_off+0), 64, 90), 1)
            
                #Draws center line
            if(right == False):
                pygame.draw.line(screen, (0, 255, 0), (400 - wall_distance,0), (400 - wall_distance, 600), 1)
                pygame.draw.line(screen, (255, 0, 0), (400 - distance_avg,0), (400 - distance_avg, 600), 1)
                error = distance_avg - wall_distance
            else:
                pygame.draw.line(screen, (0, 255, 0), (400 + wall_distance,0), (400 + wall_distance, 600), 1)
                pygame.draw.line(screen, (255, 0, 0), (400 - distance_avg,0), (400 - distance_avg, 600), 1)
                error = distance_avg + wall_distance

            if(error > 0):
                position = error * kp * error
            else:
                position = -1 * error * error * kp
            
            #Update screen with all the points from the sample
            pygame.display.update()
            screen.fill(WHITE)
            keyboard()
            
            if(position > max_turn):
                    position = max_turn
            if(position < -max_turn):
                    position = -max_turn

            arduino.write("t%d\n"%position)
            
            print("Target angle %d"%position)
            print("Error %d"%error)
