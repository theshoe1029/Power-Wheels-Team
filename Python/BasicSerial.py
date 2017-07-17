import serial

ran = 0

arduino = serial.Serial('COM9')
print(arduino.name)

while(arduino.is_open):
    if(ran == 0):
        arduino.write('t0\n')
        ran = 1
    print(arduino.readline())

arduino.close()

