import DataLib

import serial

import IRGA

import Command_proc

import datetime

import time

ser_IRGA= serial.Serial('/dev/ttyUSB3', 9600, timeout=1)

while(True):
    print(ser_IRGA.readline())