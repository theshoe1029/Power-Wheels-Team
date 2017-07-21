import serial, struct, os, math, pygame, time
import Tkinter as tk

arduino = serial.Serial('COM9')
print(arduino.name)

def turn(direction):
        turn = turn + (1 * direction)
        arduino.write("t")
        arduino.write(turn)
        arduino.write("\n")
        print(arduino.readline())

def key_input(event):
        key_press = event.keysym.lower()
        print(key_press)

        if key_press == 'w':
                arduino.write("m10\n")
        elif key_press == 's':
                arduino.write("m-10\n")
        else:
                arduino.write("m0\n")

        if key_press == "a":
                turn(1)
        elif key_press == "d":
                turn(-1)
        else:
                arduino.write("t0\n")

command = tk.Tk()
command.bind_all('key_input', key_input)
command.mainloop()
