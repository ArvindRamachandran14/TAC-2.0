

############## Module that processes the commands from the user ##############

import global_variables as g

import Command_Dict

import datetime

import time

class Command_Proc():
    """docstring for Command_Proc"""

    def __init__(self, dl, string, time_stamp):

        self.dl = dl
 
        self.string = string

        self.strings =  self.string.split('\n')[0].split(' ')

        self.time_stamp = time_stamp


    def Do_it(self):

        ############# Function that executes the command #############s
    
        #print(self.strings)
        
        if self.strings in ([u''], [u'\n'], [u'\r']): # User enters a new line or does not enter anything - no action requied, return False
        
            return False

        elif self.string == 'c-check\n':

            return 'Ok\n'

        elif self.strings[0] == 's': #Check to see if command is a set command
	
            print(self.strings)
            
            if self.strings[1] in self.dl.getParmDict().keys(): # Check if the variable to be set is legit
                
                #print(float(self.strings[2]))

        	    #print(self.strings[1])

                ###### check if self.strings[1] is a parameter that can actually be set or if it is a readonly paramter

                if self.strings[1][0:2] == "SC":

                    #Need to check if the self.strings[2] (set point) is a legit value - float/int, within range

                    Output_string = g.gv.TC_SC.write_command(Command_Dict.Command_Dict[self.strings[1]+'_write'], int(float(self.strings[2])*100)) # Performing set operation, return string - Done, Input Error, Checksum Error

                    if Output_string == "Done":

                        current_time = time.time() # current time 

                        time_stamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')

                        g.gv.dl.setParm(self.strings[1], g.gv.TC_SC.read_value(Command_Dict.Command_Dict[self.strings[1]+'_read'])/100.0, time_stamp)

                        Output_string = 'e 0'

                elif self.strings[1][0:2] == "CC":

                    #Need to check if the set point is a legit value - float/int, within range
                    
                    Output_string = g.gv.TC_CC.write_command(Command_Dict.Command_Dict[self.strings[1]+'_write'], int(float(self.strings[2])*100))

                    print(Output_string)

                    if Output_string == "Done":

                        current_time = time.time() # current time 

                        time_stamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')

                        g.gv.dl.setParm(self.strings[1], g.gv.TC_CC.read_value(Command_Dict.Command_Dict[self.strings[1]+'_read'])/100.0, time_stamp)

                        Output_string = 'e 0'

                elif self.strings[1][0:2] == "DP":

                    #Need to check if the set point is a legit value - float/int, within range
                    
                    Output_string = g.gv.TC_DPG.write_command(Command_Dict.Command_Dict[self.strings[1]+'_write'], int(float(self.strings[2])*100))

                    if Output_string == "Done":

                        current_time = time.time() # current time 

                        time_stamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')

                        g.gv.dl.setParm(self.strings[1], g.gv.TC_DPG.read_value(Command_Dict.Command_Dict[self.strings[1]+'_read'])/100.0, time_stamp)

                        Output_string = 'e 0'

                else: 

                    Output_string = 'e 3' #readonly paramter

                return(Output_string) 

            else:

                return('e 2') # Variable does not exist, return error message string  

        elif self.strings[0] == 'g': #Check to see if command is a get command     
		
            if self.strings[-1] == 'all':

                #print('getting all data')

                return(self.dl.get_all_data())
	
	   
            elif self.strings[-1] in self.dl.getParmDict().keys(): # Check if the variable requeseted is legit

                return(self.dl.getParm(self.strings[-1])) # Obtain value from register, return tuple to lab PC
            
            else:
            
                return('e 2') # Variable does not exist, return error message string 

        else:
            
            print(self.strings)

            return('e 1') # Wrong command
