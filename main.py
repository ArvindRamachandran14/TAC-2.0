
#################################  Import relevant packages  ################################# 

import DataLib

import serial

import IRGA

import TC

import Command_proc

import datetime

import time

import global_variables as g

import Command_Dict

#import dicttoxml

import json

import megaio as m


def main():

    #################################  Turn power on and set control type  ################################# 

    g.gv.TC_CC.write_command(Command_Dict.Command_Dict['set_ctl_type'], 1)

    g.gv.TC_CC.write_command(Command_Dict.Command_Dict['set_ctl_type'], 1)

    try:

        while True:

            #################################  Machine loop  ################################# 
                        
            current_time = time.time() # current time 
                
            time_stamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S.%f') # create time stamp in specific format
                        
            #print(time_stamp)

            Read_Instruments(g.gv.dl, g.gv.irga, g.gv.TC_SC, g.gv.TC_CC, g.gv.TC_DPG, time_stamp)  # read all instruments

            user_input = g.gv.ser_PC.readline()

            #print(user_input)
            
            Cmd_prc = Command_proc.Command_Proc(g.gv.dl, user_input.decode(), time_stamp) # perform user directed action from command line
                        
            Output = Cmd_prc.Do_it() # Output of said action from command processor
                        
            #print(type(Output))

            ########## Checking nature of output from command processor and write back to lab PC accordingly  ####### 
                        
            if isinstance(Output, bool): # Pass if False 
                                
                pass

            elif isinstance(Output, dict):

                print('output is a dictionary')

                #xmlstring = dicttoxml.dicttoxml(Output)

                #result_string = json.dumps(Output) 

                #g.gv.ser_PC.write(xmlstring)

                #g.gv.ser_PC.write(('\r'+'\n').encode())


            elif isinstance(Output, tuple):  # Write to PC if output is a tuple
                        
                g.gv.ser_PC.write((str(Output[0])+'---'+str(Output[1])).encode())
                        
                g.gv.ser_PC.write(('\r'+'\n').encode())

            elif Output == 'Ok':

                g.gv.ser_PC.write(Output.encode())

            else:
        
                g.gv.ser_PC.write(Output.encode()) # Likely a string - display string on PC and then go to newline 
                                
                g.gv.ser_PC.write(('\r'+'\n').encode())
                    
                #print('Timestamp: '+ str(time_stamp))
                        
                #print('pCO2: '+ str(dl.getParm('pCO2'))+ ' ppm')
                        
                #print('pH2O: '+ str(dl.getParm('pH2O'))+ ' ppt')
                        
                #print('Cell Temp: ' + str(dl.getParm('Cell_temp'))+ ' C')
                        
                #print('Cell Pressure: ' + str(dl.getParm('Cell_pressure'))+ ' kPa')

                #print('Cell Voltage: ' + str(dl.getParm('IVOLT'))+ ' V')
                        
                #print('\n')
                
    except (RuntimeError, TypeError, NameError, KeyboardInterrupt) as e:
         
        g.gv.TC_CC.write_command(Command_Dict.Command_Dict['power_write'], 0)

        power = g.gv.TC_CC.read_value(Command_Dict.Command_Dict['power_read'])

        if power == 0:

            print('Controller turned off')

        elif power ==1:

            print('Controller still on')

        print('Terminated because ' + str(e))
        

def Read_Instruments(dl, irga, TC_SC, TC_CC, TC_DPG, time_stamp):

     #Function to read instruments - IRGA, TC_SC, TC_CC, TC_DPG

     #print(irga.read_IRGA())
     
     #print('reading instruments')
     
     IRGA_list = g.gv.irga.read_IRGA() # Read IRGA 

     # Updated the registers with the most recently read system variables in 

     g.gv.dl.setParm('pCO2', IRGA_list[0], time_stamp) 

     g.gv.dl.setParm('pH2O', IRGA_list[1], time_stamp)
     
     g.gv.dl.setParm('Cell_pressure', IRGA_list[2], time_stamp)

     Cell_temp = IRGA_list[3]
     
     g.gv.dl.setParm('Cell_temp', Cell_temp, time_stamp)
     
     g.gv.dl.setParm('IVOLT', IRGA_list[4], time_stamp)

     Dew_point_temp =  IRGA_list[5]

     g.gv.dl.setParm('Dew_point_temp', Dew_point_temp, time_stamp)

     SC_T1 = g.gv.TC_SC.read_value(Command_Dict.Command_Dict['SC_T1_read'])/100.0

     g.gv.dl.setParm('SC_T1', SC_T1, time_stamp)

     SC_T2 = g.gv.TC_SC.read_value(Command_Dict.Command_Dict['SC_T2_read'])/100.0

     g.gv.dl.setParm('SC_T2', SC_T2, time_stamp)

     CC_T1 = g.gv.TC_CC.read_value(Command_Dict.Command_Dict['CC_T1_read'])/100.0

     g.gv.dl.setParm('CC_T1', CC_T1, time_stamp)

     DPG_T1 = g.gv.TC_DPG.read_value(Command_Dict.Command_Dict['DPG_T1_read'])/100.0

     g.gv.dl.setParm('DPG_T1', DPG_T1, time_stamp)

     Sample_weight = ((m.get_adc(0,1))/4096.0)*10

     g.gv.dl.setParm('Sample_weight', Sample_weight, time_stamp)

     if Cell_temp > 50.0 and Dew_point_temp < 45.0 and Dew_point_temp > CC_T1 and CC_T1 > SC_T1 and SC_T1 > DPG_T1:
        
         pass
        
     else:

        g.gv.dl.setParm('Status', 1, time_stamp)

main() # Call main
