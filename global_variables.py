
import tc 

import datalib

import IRGA

import serial

import asyncio #timing to work right asychronous call - go and read the data and the meanwhile you can do other things

class gv():

    """class that holds all the variables that need to be accessed across different modules.""" 

    ser_TC_SC = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.1)

    ser_TC_DPG = serial.Serial('/dev/ttyUSB1', 9600, timeout=0.1)

    ser_TC_CC = serial.Serial('/dev/ttyUSB2', 9600, timeout=0.1)

    ser_IRGA= serial.Serial('/dev/ttyUSB3', 9600, timeout=0.1)

    ser_PC = serial.Serial('/dev/ttyUSB4', 9600, timeout=0.1)

    ser_PC.stopbits = 2

    dl = datalib.DataLib() 

    irga = IRGA.IRGA(ser_IRGA) 

    TC_SC = tc.TC(ser_TC_SC)

    TC_CC = tc.TC(ser_TC_CC)

    TC_DPG = tc.TC(ser_TC_DPG)
