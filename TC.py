import serial

import time 

import datetime


class TC():

	#List of Commands to perform TC operations

	pw_on = ['*','0','0','2','d','0','0','0','0','0','0','0','1','7','7','\r'] # Command to turn TC power on

	pw_off = ['*','0','0','2','d','0','0','0','0','0','0','0','0','7','6','\r']	# Command to turn TC power off

	bstc_25 =['*','0','0','1','c','0','0','0','0','0','9','c','4','b','4','\r'] # Command to set temp to 25 C

	bstc_30 =['*','0','0','1','c','0','0','0','0','0','b','b','8','e','0','\r'] # Command to set temp to 30 C
	
	bst = []

	bst.append(['*','0','0','0','1','0','0','0','0','0','0','0','0','4','1','\r']) # Command to read thermistor 1 temp from controller 

	bst.append(['*','0','0','0','6','0','0','0','0','0','0','0','0','4','6','\r']) # Command to read thermistor 2 temp from controller 

	read_ctl_type = ['*','0','0','4','4','0','0','0','0','0','0','0','0','4','8','\r'] #Command to Read CONTROL TYPE of TC
	
	set_ctl_type = ['*','0','0','2','b','0','0','0','0','0','0','0','1','7','5','\r'] #Command to Set CONTROL TYPE of TC to PID
	
	def __init__(self, ser): 

	    self.ser = ser 

	    self.dict = {}
        
            self.buf_read_temp=[0,0,0,0,0,0,0,0,0,0,0,0] # Buffer to read temperature

	    self.buf_ctl_type = [0,0,0,0,0,0,0,0,0,0,0,0] # Buffer to record CONTROL TYPE 

	    self.buf_set_temp = [0,0,0,0,0,0,0,0,0,0,0,0] #Buffer to record response to SET TEMP
            
            self.string_read_temperature = "0x" # String to read temperature 
            
            self.string_ctl_type = "" #String to record CONTROL TYPE 
            
            self.string_set_temp = "" #String to record response to SET TEMP
    
	def power_on(self):
	     
	    print("Turning TC_CC ON")
		
	    for pn in range(0,16):
	        self.ser.write((TC.pw_on[pn]).encode())
		time.sleep(0.001)

	def power_off(self):
	     
	     print("Turning TC_CC OFF")

	     for pn in range(0,16):
	         self.ser.write((TC.pw_off[pn]).encode())
		 time.sleep(0.001)

	def read_temperature(self,thermistor):

            self.buf_read_temp=[0,0,0,0,0,0,0,0,0,0,0,0]
	
            self.string_read_temp = "0x"

	    self.ser.reset_output_buffer()
	    self.ser.reset_input_buffer()

	    for pn in range(0,16):
		self.ser.write((TC.bst[thermistor][pn]).encode())
		time.sleep(0.001)

	    self.dict['timestamp'] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

	    for pn in range(0,12):
		self.buf_read_temp[pn]=self.ser.read(1)
            	time.sleep(0.001)

	    for i in range(1, 9):
		self.string_read_temp+=self.buf_read_temp[i].decode()

	    self.dict['temperature']  = int(self.string_read_temp,0)/100.0
	    
	    #print(self.dict['temperature'])

	    return(self.dict['temperature'])

	def set_temperature(self):
        
            self.buf_set_temp=[0,0,0,0,0,0,0,0,0,0,0,0]
	    self.string_set_temp = ""
	    
	    self.ser.reset_output_buffer()
	    self.ser.reset_input_buffer()

            for pn in range(0,16):
	        self.ser.write((TC.bstc_30[pn]).encode())
	        time.sleep(0.001)
	   
	    for i in range(0,12):
                self.buf_set_temp[i]=self.ser.read(1)
		time.sleep(0.001)
	    
	    for i in range(0,12):
		self.string_set_temp+=self.buf_set_temp[i].decode()

            return(self.string_set_temp)

	def read_control_type(self):
	    

            self.buf_ctl_type=[0,0,0,0,0,0,0,0,0,0,0,0] 
            self.string_ctl_type = ""

	    self.ser.reset_output_buffer()
	    self.ser.reset_input_buffer()

	    for pn in range(0,16):
	        self.ser.write((TC.read_ctl_type[pn]).encode())

	    for i in range(0,12):
                self.buf_ctl_type[i]=self.ser.read(1)
		time.sleep(0.001)

	    for i in range(0,12):
		self.string_ctl_type+=self.buf_ctl_type[i].decode()
 
            return(self.string_ctl_type)
	
	def set_control_type(self):

	    self.ser.reset_output_buffer()
	    self.ser.reset_input_buffer()

            for pn in range(0,16):
	        self.ser.write((TC.set_ctl_type[pn]).encode())
