import serial

import time 

import datetime

import Command_Dict

class TC():

    def __init__(self, ser):

        self.ser = ser

        self.output_buffer = []

    @classmethod
    def command_generator(cls, command, send_value): 

        #Function to generate the command to be sent to the TC, given the command type and sendvalue

        return_buffer = ['*', '0', '0'] # Full command to be returned 

        if len(command) == 2:

            return_buffer.append(command[0])

            return_buffer.append(command[1])

        else: 

            print(error)

            return(None)

        if send_value>=0:
            pass
        else:
            send_value = 2**32 + send_value #hex representation of negative numbers

        send_value_string = []

        for x in hex(send_value)[2:]:
            send_value_string.append(x) 

        return_buffer+= ['0']*(8-len(send_value_string)) # 8 digit hex representation

        return_buffer+= send_value_string

        ################################# Checksum calculation #################################

        checksum = 0

        for x in return_buffer[1:]:
            checksum += ord(x) 

        #print(checksum)

        return_buffer += hex(checksum)[-2:] #Add hex representation of checksum

        return_buffer += '\r'

        return(return_buffer)

    def send_command(self, command, send_value):

        #print(TC.command_generator(command, send_value))

        output_buffer=[]

        output_string = ""

	#print(command)

	#print(send_value)

        command_buffer = TC.command_generator(command, send_value) # Command generator function returns the command buffer to be sent to the TC

        ################################# Write command to TC #################################

        for pn in range(0,16):
            self.ser.write(command_buffer[pn].encode()) #ser is the serial port of the relevant TC
            time.sleep(0.001)

        ################################# Read response from TC #################################
	
	output_string = self.ser.readline().decode()

        for pn in range(len(output_string)):
            output_buffer.append(str(output_string[pn]))
            time.sleep(0.001)
        
        ################################# Checksum test #################################

        if command_buffer[5:-3] == output_buffer[1:-3]:

	    print(command_buffer)

            return('Done')

        else:
		
	    #print(command_buffer[5:-3])
	
	    #print(output_buffer[2:-3])

            return('Checksum error')

    def read_temperature(self, command, send_value):

        output_buffer=[0,0,0,0,0,0,0,0,0,0,0,0]

        string_read_temp = "0x"

        command_buffer = TC.command_generator(command, send_value)

        ################################# Write command to TC #################################

        for pn in range(0,16):
            self.ser.write(command_buffer[pn].encode())
            time.sleep(0.001)

        ################################# Read response from TC #################################

        for pn in range(0,12):
            output_buffer[pn]=self.ser.read(1)
            time.sleep(0.001)

        for i in range(1, 9):
            string_read_temp+=output_buffer[i].decode()

        return(int(string_read_temp,0)/100.0) #Convert to temperature


#tc = TC('Ser')

#tc.send_command(Command_Dict.Command_Dict['set_ctl_type'],1)
