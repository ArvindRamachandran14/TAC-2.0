############## Module that processes the commands from the user ##############

import global_variables as g
import command_dict
import datetime as dt
import time
import os 
from math import exp, log
import asyncio #timing to work right asychronous call - go and read the data and the meanwhile you can do other things

class Command_Proc():
    def __init__(self, dl):
        self.dl = dl
        self.switch = ['off', 'on']
        self.err = 0.0
        self.err_1 = 0.0                            # Previous value of error
        self.errDot = 0.0                           # Derivative of error at iternation n
        self.errSum = 0.0                           # Integral of error
        self.deltaT = 2.0                           #machine cycle takes 2 seconds 

    # Function that executes commands
    def Do_it(self, string):

        self.string = string
        self.strings =  self.string.split('\n')[0].split(' ')
        if self.strings in ([u''], [u'\n'], [u'\r']): # User enters a new line or does not enter anything - no action requied, return False
            return False
        elif self.string == 'c-check\n':
            return 'Ok\n'
        elif self.strings[0] == 'r': #register command 
            if self.strings[1] in self.dl.getParmDict().keys(): # Check if the variable to be set is legit
                current_time = time.time() # current time 
                time_stamp = dt.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
                g.gv.dl.setParm(self.strings[1], 0.0, time_stamp)
                Output_string = 'e 0' #Success
            else:
                Output_string = 'e 2' # Variable does not exist, return error message string  
            return(Output_string)

        elif self.strings[0] == 's': #set command
            print(self.strings)
            if self.strings[1] in self.dl.getParmDict().keys(): # Check if the variable to be set is legit
                ###### check if self.strings[1] is a parameter that can actually be set or if it is a readonly paramter
                if self.strings[1] == "ByPass":
                    os.system("megaio 0 rwrite 8 "+self.switch[int(self.strings[2])])
                    current_time = time.time() # current time 
                    time_stamp = dt.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
                    g.gv.dl.setParm(self.strings[1], int(self.strings[2]), time_stamp)
                    Output_string = 'e 0'

                elif self.strings[1] == "IRGA_pump":
                    os.system("megaio 0 rwrite 7 "+self.switch[int(self.strings[2])])
                    current_time = time.time() # current time 
                    time_stamp = dt.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
                    g.gv.dl.setParm(self.strings[1], int(self.strings[2]), time_stamp)
                    Output_string = 'e 0'

                elif self.strings[1][0:2] == "SC":
                    #Need to check if the self.strings[2] (set point) is a legit value - float/int, within range
                    Output_string = g.gv.TC_SC.write_command(command_dict.Command_Dict[self.strings[1]+'_write'], int(float(self.strings[2])*100)) # Performing set operation, return string - Done, Input Error, Checksum Error
                    print(Output_string)
                    if Output_string == "Done":
                        current_time = time.time() # current time 
                        time_stamp = dt.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
                        g.gv.dl.setParm(self.strings[1], g.gv.TC_SC.read_value(command_dict.Command_Dict[self.strings[1]+'_read'])/100.0, time_stamp)
                        Output_string = 'e 0'
                        #return(Output_string)

                elif self.strings[1][0:2] == "CC":
                    #Need to check if the set point is a legit value - float/int, within range
                    Output_string = g.gv.TC_CC.write_command(command_dict.Command_Dict[self.strings[1]+'_write'], int(float(self.strings[2])*100))
                    print(Output_string)
                    if Output_string == "Done":
                        current_time = time.time() # current time 
                        time_stamp = dt.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
                        g.gv.dl.setParm(self.strings[1], g.gv.TC_CC.read_value(command_dict.Command_Dict[self.strings[1]+'_read'])/100.0, time_stamp)
                        Output_string = 'e 0'

                elif self.strings[1][0:3] == "DPG":
                    Output_string = g.gv.TC_DPG.write_command(command_dict.Command_Dict[self.strings[1]+'_write'], int(float(self.strings[2])*100))
                    print(Output_string)
                    if Output_string == "Done":
                        current_time = time.time() # current time 
                        time_stamp = dt.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
                        g.gv.dl.setParm(self.strings[1], g.gv.TC_DPG.read_value(command_Dict.command_Dict[self.strings[1]+'_read'])/100.0, time_stamp)
                        Output_string = 'e 0'

                elif self.strings[1]== "pH2O_P":
                    current_time = time.time() # current time 
                    time_stamp = dt.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
                    g.gv.dl.setParm(self.strings[1], float(self.strings[2]), time_stamp)
                    self.dl.cfg.pH2O_P = float(self.strings[2])
                    self.dl.cfg.update()
                    Output_string = 'e 0'

                elif self.strings[1]== "pH2O_I":
                    current_time = time.time() # current time 
                    time_stamp = dt.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
                    g.gv.dl.setParm(self.strings[1], float(self.strings[2]), time_stamp)
                    self.dl.cfg.pH2O_I = float(self.strings[2])
                    self.dl.cfg.update()
                    Output_string = 'e 0'

                elif self.strings[1]== "pH2O_D":
                    current_time = time.time() # current time 
                    time_stamp = dt.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')            
                    g.gv.dl.setParm(self.strings[1], float(self.strings[2]), time_stamp)
                    self.dl.cfg.pH2O_D = float(self.strings[2])
                    self.dl.cfg.update()
                    Output_string = 'e 0'

                elif self.strings[1] == "DPG_set": 
                    current_time = time.time() # current time 
                    time_stamp = dt.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
                    g.gv.dl.setParm("DPG_set", float(self.strings[2]),time_stamp)
                    g.gv.dl.setParm("RH_set", 0.0, time_stamp)
                    g.gv.dl.setParm("pH2O_set", 0.0, time_stamp)
                    Output_string = 'e 0'

                elif self.strings[1] == "RH_set":
                    
                    current_time = time.time() # current time 
                    time_stamp = dt.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
                    g.gv.dl.setParm("DPG_set", 0.0, time_stamp)
                    g.gv.dl.setParm("RH_set", float(self.strings[2]), time_stamp)
                    g.gv.dl.setParm("pH2O_set", 0.0, time_stamp)
                    Output_string = 'e 0'

                elif self.strings[1] == "pH2O_set":
                    current_time = time.time() # current time 
                    time_stamp = dt.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
                    g.gv.dl.setParm("DPG_set", 0.0, time_stamp)
                    g.gv.dl.setParm("RH_set", 0.0, time_stamp)
                    g.gv.dl.setParm("pH2O_set", float(self.strings[2]), time_stamp)
                    Output_string = 'e 0'

                else: 
                    Output_string = 'e 3' #readonly paramter

            else:
                Output_string = 'e 2' # Variable does not exist, return error message string  

            return(Output_string)

        elif self.strings[0] == 'g': # get command     
            
            if self.strings[1] == 'all':
                return(self.dl.get_all_data())
            elif self.strings[1] == 'cal_basic_variables':
                print('g cal_basic_variables command received')
                return(self.dl.get_cal_basic_variables())

            elif self.strings[1] == 'cal_all_variables':
                print('g cal_all_variables command received')
                return(self.dl.get_cal_all_variables())

            elif self.strings[1] in self.dl.getParmDict().keys(): # Check if the variable requeseted is legit
                return(self.dl.getParm(self.strings[-1])) # Obtain value from register, return tuple to lab PC
                
            else:
                return('e 2') # Variable does not exist, return error message string 
        else:
                
            print(self.strings)
            return('e 1') # Wrong command

    def Set_DPG_ctrl(self, DPG_ctrl):

        Output_string = g.gv.TC_DPG.write_command(command_Dict.Command_Dict['DPG_set_write'], int(DPG_ctrl)*100)
        return(Output_string)

    def Convert_to_DPG_ctrl(self):
            
        ph2oNeed = 0.0
        if self.dl.getParm('DPG_set')[0]!=0:
            Ctrl_type = "TDP"
            P_h2o =  self.ph2oSat(float(self.dl.getParm('DP_set')[0])) #Pascal
            ph2oNeed = (P_h2o/(self.dl.getParm('CellP')[0]*1000))*1000 # Pa to ppt

        elif self.dl.getParm('RH_set')[0]!=0:

            #print('RH_set, SC_T, pH2O_sat = ', self.dl.getParm('RH_set')[0], self.dl.getParm('SC_T')[0], self.ph2oSat(self.dl.getParm('SC_T')[0]))
            P_h2o =  (float(self.dl.getParm('RH_set')[0])*0.01)*self.ph2oSat(self.dl.getParm('SC_T')[0]) #Pascal
            ph2oNeed = (P_h2o/(self.dl.getParm('CellP')[0]*1000))*1000 # Pa to ppt
            Ctrl_type = "RH"

        elif self.dl.getParm('pH2O_set')[0]!=0:
            ph2oNeed = float(self.dl.getParm('pH2O_set')[0])
            Ctrl_type = "pH2O"

        else:
            Ctrl_type = "None"
            pass

        print('Control type', Ctrl_type)

        if ph2oNeed!=0:    
            DPG_ctrl = self.dewPointTemp(ph2oNeed*0.001*self.dl.getParm('CellP')[0]*1000) #ppt to Pa
            #self.err = DPG_ctrl - self.dewPointTemp(self.dl.getParm('pH2O')[0]*0.001*self.dl.getParm('CellP')[0]*1000) #Error
            self.err = DPG_ctrl - self.dl.getParm('DPT')[0]
            self.errDot = (self.err - self.err_1) / self.deltaT     # Error derivative value
            self.err_1 = self.err                                   # Save the error value
            self.errSum += self.err                                 # Error sum value
            #print('DPT', self.dewPointTemp(self.dl.getParm('pH2O')[0]*self.dl.getParm('CellP')[0]))
            #print('Error', self.err)
            #print('Error derivative', self.errDot)
            #print('Error sum', self.errSum)
            DPG_ctrl = (self.dl.getParm('pH2O_P')[0]*self.err + self.dl.getParm('pH2O_D')[0]*self.errDot + self.dl.getParm('pH2O_I')[0]*self.errSum)
            limit = min(self.dl.getParm('SC_T')[0], self.dl.getParm('CC_T')[0]) #limiter to avoid condensation
            if DPG_ctrl > limit :
                DPG_ctrl = limit
            return DPG_ctrl


    # Function to calculate saturated pH2O at a given T
    def ph2oSat(self, T) :
        return 610.78 * exp((T * 17.2684) / (T + 238.3))

    # Function to calculate dew point at a given pH2O
    def dewPointTemp(self, ph2o) :
        w = log(ph2o / 610.78)
        return w * 238.3 / (17.294 - w)