import time

import datetime

import serial

ser_PC = serial.Serial('/dev/ttyUSB0',9600, timeout=3)

filename = "PC_commands.txt"
file = open(filename, "w")


try:
    while True:
    # Read all the ADC channel values in a list.
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        file.write(st)
        file.write('\t')
        
        string = ser_PC.readline().decode()
        
        file.write(string)
        
        print(string)
        
        file.write('\n')
        
        ser_PC.write('Output'.encode())

except KeyboardInterrupt:
    file.write('Program terminated by Keyboard Interruption at time')
    file.write(st)
    file.close()