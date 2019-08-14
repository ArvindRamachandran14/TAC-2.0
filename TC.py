import serial

import time 

import datetime


class TC():

	buf=[0,0,0,0,0,0,0,0,0,0,0,0]

	power_on = ['*','0','0','2','d','0','0','0','0','0','0','0','1','7','7','\r'] # to turn power on

	power_off = ['*','0','0','2','d','0','0','0','0','0','0','0','0','7','6','\r']	# to turn power off

	bstc=['*','0','0','1','c','0','0','0','0','0','9','c','4','b','4','\r'] # To set temp to 25C

	bst[0] =['*','0','0','0','1','0','0','0','0','0','0','0','0','4','1','\r'] # to read thermistor temp 1 from controller 1

	bst[1] = ['*','0','0','0','1','0','0','0','0','0','0','0','0','4','2','\r'] # to read thermistor temp 1 from controller 2

	def __init__(self, ser):

		self.ser = ser 

		self.dict = {}
	
	def power_on(self):

		for pn in range(0,16):
			self.ser.write((TC.power_on[pn]).encode())
			time.sleep(0.001)

	def power_off(self):

		for pn in range(0,16):
			self.ser.write((TC.power_off[pn]).encode())
			time.sleep(0.001)

	def read_temperature(self,thermistor):

		for pn in range(0,16):
			self.ser.write((bst[thermistor][pn]).encode())
			time.sleep(0.001)

		self.dict['timestamp'] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

		for pn in range(0,12):
		    buf[pn]=self.ser.read(1)
		    time.sleep(0.001)

		for i in range(1, 9):
			string+=buf[i].decode()

		self.dict['temperature']  = int(string,0)/100.0

		return(self.dict)

	def set_temperature(self,self.ser):

		for pn in range(0,16):
			self.ser.write((bstc[pn]).encode())
			time.sleep(0.001)


