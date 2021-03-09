import serial
import time 
import datetime

class TC():

    """ Class that implements the temperature controller functionality - applies to SC_TC, CC_TC, DPG_TC"""

    def __init__(self, ser):
        self.ser = ser
        self.output_buffer = []

    @classmethod
    def command_generator(cls, command, send_value): 

        """Function to generate the command to be sent to the TC, given the command type and sendvalue"""
        
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
        checksum = 0

        for x in return_buffer[1:]:
            checksum += ord(x) # Checksum calculation 

        return_buffer += hex(checksum)[-2:] #Add hex representation of checksum
        return_buffer += '\r'
        return(return_buffer)

    def write_command(self, command, send_value):

        """Function to write the command bit by bit to the temperature contollers via serial communication"""

        output_buffer=[]
        output_string = ""
        command_buffer = TC.command_generator(command, send_value) # Command generator function returns the command buffer to be sent to the TC
        #Write command to TC
        for pn in range(0,16):
            self.ser.write(command_buffer[pn].encode()) #ser is the serial port of the relevant TC
            time.sleep(0.001)
	
        output_string = self.ser.readline().decode()  # Read response from TC 
        for pn in range(len(output_string)):
            output_buffer.append(str(output_string[pn]))
            time.sleep(0.001)
        
        #The checksum test can be simplified by just looking for 'X' character in the output_string
        if command_buffer[5:-3] == output_buffer[1:-3]: #Checksum test
            return('Done')
        else:
            return('Checksum error: Command Buffer = '+ command_buffer[5:-3]+ ' Output Buffer = '+output_buffer[1:-3])

    def read_value(self, command):

        """Function to read the temperature controllers in a bit by bit fashion via serial communication and return the decimal value"""

        send_value = 0
        output_buffer=[0,0,0,0,0,0,0,0,0,0,0,0]
        string_read_temp = "0x"
        command_buffer = TC.command_generator(command, send_value)
        for pn in range(0,16):
            self.ser.write(command_buffer[pn].encode()) # Write command to TC 
            time.sleep(0.001)
        for pn in range(0,12):
            output_buffer[pn]=self.ser.read(1) # Read response from TC
            #time.sleep(0.001)
        if output_buffer[1:9] != "XXXXXXXX":
            for i in range(1, 9):
                string_read_temp+=output_buffer[i].decode()
            val = int(string_read_temp,0)
            if string_read_temp[2] > '7':
                val = -(2**32-val)
            return(val)
        else:
            return(0)