#Temperature Controller module - applies to SC_TC, CC_TC, DPG_TC

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

    def write_command(self, command, send_value):

        #print(TC.command_generator(command, send_value))

        output_buffer=[]

        output_string = ""

    #print(command)

    #print(send_value)

        command_buffer = TC.command_generator(command, send_value) # Command generator function returns the command buffer to be sent to the TC

        ################################# Write command to TC #################################

        # Replace below lines of code with self.ser.write(command_buffer.encode()) 

        for pn in range(0,16):
            self.ser.write(command_buffer[pn].encode()) #ser is the serial port of the relevant TC
            time.sleep(0.001)

        ################################# Read response from TC #################################
	
        output_string = self.ser.readline().decode()

        #No need to put output_string into output_buffer

        for pn in range(len(output_string)):
            output_buffer.append(str(output_string[pn]))
            time.sleep(0.001)
        

        #The checksum test can be simplified by just looking for 'X' character in the output_string

        ################################# Checksum test #################################

        if command_buffer[5:-3] == output_buffer[1:-3]:

            return('Done')

        else:
    
            return('Checksum error: Command Buffer = '+ command_buffer[5:-3]+ ' Output Buffer = '+output_buffer[1:-3])

    def read_value(self, command):

        send_value = 0

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
            #time.sleep(0.001)

        if output_buffer[1:9] != "XXXXXXXX":
            
            for i in range(1, 9):
                string_read_temp+=output_buffer[i].decode()

            val = int(string_read_temp,0)

            if string_read_temp[2] >= ‘7’:

                val = -(2**32 – val)

            return(val)

        else:

            return(0)

         #Convert string to integer (actual output)

#tc = TC('Ser')

#tc.send_command(Command_Dict.Command_Dict['set_ctl_type'],1)
