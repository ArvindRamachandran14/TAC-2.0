
#This module has all the variables that need to be accessed across different modules. 

import TC 

import Datalib

import IRGA

import serial

class gv():

    #################################   Serial port definiton   #################################     

    ser_TC_SC = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)

    ser_TC_DPG = serial.Serial('/dev/ttyUSB2', 9600, timeout=1)

    ser_TC_CC = serial.Serial('/dev/ttyUSB3', 9600, timeout=1)

    ser_IRGA= serial.Serial('/dev/ttyUSB4', 9600, timeout=1)

    ser_PC = serial.Serial('/dev/ttyUSB0', 9600, timeout=3)

    #################################   Object creation   ################################# 

    dl = DataLib.DataLib()  # initialization triggered when object is created 

    irga = IRGA.IRGA(ser_IRGA) 

    TC_SC = TC.TC(ser_TC_SC)

    TC_CC = TC.TC(ser_TC_CC)

    TC_DPG = TC.TC(ser_TC_DPG)