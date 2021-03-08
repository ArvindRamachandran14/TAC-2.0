
#IRGA module - 

import serial

import time 

import datetime

import re

import xml.etree.ElementTree as ET


class IRGA():

    def __init__(self, ser):

        # When an instance of this class is created, the serial port is initialized and the OUTRATE is set to zero

        # This makes sure the IRGA only sends values when requested

        self.ser = ser
        
        self.ser.write('<LI840> <CFG> <OUTRATE> 0 </OUTRATE> </CFG> </LI840>'.encode()) #Set the OUTRATE to 0
        
        self.xmlstring = self.ser.readline().decode() 
	
        self.ser.write('<LI840><DATA>?</DATA></LI840>'.encode())

        self.return_list = []

    def read_IRGA(self):
        
        self.return_list = []

        self.xmlstring = self.ser.readline().decode() # Reading the output as an XML string 

        self.ser.write('<LI840><DATA>?</DATA></LI840>'.encode()) #Command to request output from IRGA
        
        self.root = ET.fromstring(self.xmlstring)

        #Add IRGA output to the return list 
            
        self.return_list.append(float(self.root[0].find('co2').text))

        self.return_list.append(float(self.root[0].find('h2o').text))

        self.return_list.append(float(self.root[0].find('cellpres').text))

        self.return_list.append(float(self.root[0].find('celltemp').text))

        self.return_list.append(float(self.root[0].find('ivolt').text))

        self.return_list.append(float(self.root[0].find('h2odewpoint').text))
            
        return(self.return_list)
