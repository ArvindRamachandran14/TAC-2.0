
import global_variables as g

import Command_Dict

import datetime

import time

class Command_Proc():
    """docstring for Command_Proc"""

    def __init__(self, dl, string, time_stamp):

        self.dl = dl
 
        self.string = string

        self.strings =  self.string.split('-')

        self.time_stamp = time_stamp


    def Do_it(self):
    
        #print(self.strings)
        
        if self.strings in ([u''], [u'\n'], [u'\r']): # User enters a new line or does not enter anything - no action requied, return False
        
            return False

        elif self.strings[0] == 's': #Check to see if command is a set command
            
            if self.strings[1] in self.dl.getParmDict().keys(): # Check if the variable to be set is legit
                
                #print(float(self.strings[2]))

        #print(self.strings[1])

                #self.dl.setParm(self.strings[1], float(self.strings[2]), self.time_stamp) # Update register with user specified set point
                
                #print(self.dl.getParm(self.strings[1])) 
        
        #print(Command_Dict.Command_Dict[self.strings[1]+'_write'])

                if self.strings[1][0:2] == "SC":

                    Output_string = g.gv.TC_SC.write_command(Command_Dict.Command_Dict[self.strings[1]+'_write'], int(float(self.strings[2])*100)) # Performing set operation, return string - Done, Input Error, Checksum Error

                    if Output_string == "Done":

                        current_time = time.time() # current time 

                        time_stamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')

                        g.gv.dl.setParm(self.strings[1], g.gv.TC_SC.read_value(Command_Dict.Command_Dict[self.strings[1]+'_read'])/100.0, time_stamp)

                elif self.strings[1][0:2] == "CC":
                
                    Output_string = g.gv.TC_CC.write_command(Command_Dict.Command_Dict[self.strings[1]+'_write'], int(float(self.strings[2])*100))

                    if Output_string == "Done":

                        current_time = time.time() # current time 

                        time_stamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')

                        g.gv.dl.setParm(self.strings[1], g.gv.TC_CC.read_value(Command_Dict.Command_Dict[self.strings[1]+'_read'])/100.0, time_stamp)

                elif self.strings[1][0:2] == "DP":
                    
                    g.gv.TC_DPG.write_command(Command_Dict.Command_Dict[self.strings[1]+'_write'], int(float(self.strings[2])*100))

                    if Output_string == "Done":

                        current_time = time.time() # current time 

                        time_stamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')

                        g.gv.dl.setParm(self.strings[1], g.gv.TC_DPG.read_value(Command_Dict.Command_Dict[self.strings[1]+'_read'])/100.0, time_stamp)

                return(Output_string) 

            else:

                return('Variable does not exist') # Variable does not exist, return error message string  

        elif self.strings[0] == 'g': #Check to see if command is a get command     
	              

            if self.strings[1][:-1] == 'all':

                return(self.dl.get_all_data())

            elif self.strings[1][:-1] in self.dl.getParmDict().keys(): # Check if the variable requeseted is legit

                return(self.dl.getParm(self.strings[1][:-1])) # Obtain value from register, return tuple to lab PC
            
                return('Variable does not exist') # Variable does not exist, return error message string 

        else:
            
            print(self.strings)

            return('Command Error') # Wrong command
