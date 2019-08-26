import serial

import time 

import datetime


class TC():

	power_on = ['*','0','0','2','d','0','0','0','0','0','0','0','1','7','7','\r'] # to turn power on

	power_off = ['*','0','0','2','d','0','0','0','0','0','0','0','0','7','6','\r']	# to turn power off

	#bstc=['*','0','0','1','c','0','0','0','0','0','9','c','4','b','4','\r'] # To set temp to 25 C

	bstc=['*','0','0','1','c','0','0','0','0','0','b','b','8','d','c','\r'] # To set temp to 30 C
	
	bst = []

	bst.append(['*','0','0','0','1','0','0','0','0','0','0','0','0','4','1','\r']) # to read thermistor temp 1 from controller 1

	bst.append(['*','0','0','0','6','0','0','0','0','0','0','0','0','4','6','\r']) # to read thermistor temp 1 from controller 2

	control_type(['*','0','0','4','4','0','0','0','0','0','0','0','0','4','8','\r']) #Set control type to PID control

	def __init__(self, ser): 

	    self.ser = ser 

	    self.dict = {}
        
            self.buf=[0,0,0,0,0,0,0,0,0,0,0,0]
	
            self.string = "0x"
    
	def power_on(self):

		for pn in range(0,16):
			self.ser.write((TC.power_on[pn]).encode())
			time.sleep(0.001)

	def power_off(self):

		for pn in range(0,16):
			self.ser.write((TC.power_off[pn]).encode())
			time.sleep(0.001)

	def read_temperature(self,thermistor):

            self.buf=[0,0,0,0,0,0,0,0,0,0,0,0]
	
            self.string = "0x"

	    for pn in range(0,16):
			self.ser.write((TC.bst[thermistor][pn]).encode())
			time.sleep(0.001)

	    self.dict['timestamp'] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

	    for pn in range(0,12):
			self.buf[pn]=self.ser.read(1)
            time.sleep(0.001)

	    for i in range(1, 9):
			self.string+=self.buf[i].decode()

	    self.dict['temperature']  = int(self.string,0)/100.0
	    
	    #print(self.dict['temperature'])

	    return(self.dict['temperature'])

	def set_temperature(self):

            for pn in range(0,16):
			self.ser.write((bstc[pn]).encode())
			time.sleep(0.001)

	def read_control_type(self):

		for pn in range(0,16):
			self.ser.write((control_type[pn]).encode())


