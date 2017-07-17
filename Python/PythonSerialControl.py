import serial

arduino = serial.Serial('COM8')
print(arduino.name)

for x in range(0,3):
    print(arduino.readline())

while True:
    command = input("Please enter command: ")
    if(command == "end"):
        arduino.close()
        print(arduino.readline())
    else:
        arduino.write(command)
        arduino.write("\n")
        print(arduino.readline())
    
