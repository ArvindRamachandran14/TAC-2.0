import serial
import IRGA
import command_proc
import datetime as dt
import time
from datetime import datetime
import global_variables as g
import command_dict
import json
import asyncio
import os
import sys

class TAC():

    """ The main class that implements the TAC program responsible for reading the 5 TA instruments and processing the user commands received from TAGUI"""

    def __init__(self):
        self.delta_T = 2.0
        self.sem = asyncio.Semaphore(1)  
        self.bdone = False

    async def Read_Instruments(self, Cmd_prc):

        """ Function to read the 5 TA instruments in every machine cycle"""

        try:
            start = datetime.now()
            while not self.bdone:
                async with self.sem:
                    current_time = time.time() # current time 
                    time_stamp = dt.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S.%f') # create time stamp in specific format        
                    IRGA_list = g.gv.irga.read_IRGA() # Read IRGA 

                    # Updated the registers with the most recently read system variables in 
                    g.gv.dl.setParm('pCO2', IRGA_list[0], time_stamp) 
                    g.gv.dl.setParm('pH2O', IRGA_list[1], time_stamp)
                    g.gv.dl.setParm('CellP', IRGA_list[2], time_stamp)
                    CellT = IRGA_list[3]
                    g.gv.dl.setParm('CellT', IRGA_list[3], time_stamp)
                    g.gv.dl.setParm('IVOLT', IRGA_list[4], time_stamp)
                    DPT = IRGA_list[5]
                    g.gv.dl.setParm('DPT', IRGA_list[5], time_stamp)
                    SC_T = g.gv.TC_SC.read_value(command_dict.Command_Dict['SC_T_read'])/100.0
                    g.gv.dl.setParm('SC_T', SC_T, time_stamp)
                    SC_Tblock = g.gv.TC_SC.read_value(command_dict.Command_Dict['SC_Tblock_read'])/100.0
                    g.gv.dl.setParm('SC_Tblock', SC_Tblock, time_stamp)
                    SC_output = ((g.gv.TC_SC.read_value(command_dict.Command_Dict['SC_output_read'])/100.0)/5.11)*100.0 #convert to decimal then convert to %
                    g.gv.dl.setParm('SC_output', SC_output, time_stamp)
                    CC_T = g.gv.TC_CC.read_value(command_dict.Command_Dict['CC_T_read'])/100.0
                    g.gv.dl.setParm('CC_T', CC_T, time_stamp)
                    CC_output = ((g.gv.TC_CC.read_value(command_dict.Command_Dict['CC_output_read'])/100.0)/5.11)*100.0 #convert to decimal then convert to %
                    g.gv.dl.setParm('CC_output', CC_output, time_stamp)
                    DPG_T = g.gv.TC_DPG.read_value(command_dict.Command_Dict['DPG_T_read'])/100.0
                    g.gv.dl.setParm('DPG_T', DPG_T, time_stamp)
                    DPG_output = ((g.gv.TC_DPG.read_value(command_dict.Command_Dict['DPG_output_read'])/100.0)/5.11)*100.0 #convert to decimal then convert to %
                    g.gv.dl.setParm('DPG_output', DPG_output, time_stamp)
                    WGT = 10 #to be edited
                    #WGT = ((m.get_adc(0,1))/4096.0)*10
                    g.gv.dl.setParm('WGT', WGT, time_stamp)
                    
                    #Check for normal operation of TA
                    if CellT > 50.0 and DPT < 45.0 and DPT > CC_T and CC_T > SC_T and SC_T > DPG_T:
                        pass
                    else:
                        g.gv.dl.setParm('Status', 1, time_stamp)

                    #Humidity control
                    if Cmd_prc.dl.getParm("DPG_power")[0]:
                        DPG_ctrl = Cmd_prc.Convert_to_DPG_ctrl()
                        print('DPG_ctrl', DPG_ctrl)
                        Output_string = Cmd_prc.Set_DPG_ctrl(DPG_ctrl)

                now = datetime.now()
                diff = now - start
                ms = diff.seconds * 1000 + diff.microseconds / 1000
                delay = self.delta_T-ms/1000.0
                print('Elapsed time: {0:.1f}, Delay: {1:.1f}'.format(ms, delay))
                start = now
                await asyncio.sleep(delay)

        except (ZeroDivisionError, RuntimeError, TypeError, NameError, KeyboardInterrupt) as e:
            self.Terminate(e)
   

    async def doCmd(self, Cmd_prc):

        """ Function to process the user commands received from TAGUI in every machine cycle"""

        try:
            while not self.bdone:
                async with self.sem:
                    user_input = g.gv.ser_PC.readline().decode()
                    if len(user_input) == 0:
                        pass
                    else:
                        Output = Cmd_prc.Do_it(user_input)

                        # Checking nature of output from command processor and write back to lab PC accordingly    
                        if isinstance(Output, bool): # Pass if False 
                            pass
                        elif isinstance(Output, dict):
                            print('output is a dictionary')
                        elif isinstance(Output, tuple):  # Write to PC if output is a tuple
                            g.gv.ser_PC.write((str(Output[0])+'---'+str(Output[1])+'\n').encode())
                        else:
                            print(Output)
                            g.gv.ser_PC.write((Output+'\n').encode()) # Likely a string with error code - display string on PC and then go to newline 
                await asyncio.sleep(0.1)

        except (ZeroDivisionError, RuntimeError, TypeError, NameError, KeyboardInterrupt) as e:
            self.Terminate(e) 

    def Terminate(self, e):

        """Function that terminates the TAC program when there is an error. The error is printed on the terminal in a user friendly format"""

        self.bdone = True
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        g.gv.TC_SC.write_command(command_dict.Command_Dict['SC_power_write'], 0) #Turn power off
        g.gv.TC_CC.write_command(command_dict.Command_Dict['CC_power_write'], 0) #Turn power off
        g.gv.TC_DPG.write_command(command_dict.Command_Dict['DPG_power_write'], 0) #Turn power off
        power_CC = g.gv.TC_CC.read_value(command_dict.Command_Dict['CC_power_read'])
        power_SC = g.gv.TC_SC.read_value(command_dict.Command_Dict['SC_power_read'])        
        power_DPG = g.gv.TC_DPG.read_value(command_dict.Command_Dict['DPG_power_read'])
        if power_CC == power_SC == power_DPG == 0: #Check that power was turned off
            print('Controllers turned off')
        else:
            print('One or more of the controllers still on')
        print('Terminated because ' + str(e)) #Print error message
        return None

async def main() :

    """Function that implements the TAC machine cycle and schedules the tasks related to read instruments and processing commands"""

    current_time = time.time()
    time_stamp = dt.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S.%f')
    tac = TAC()
    Cmd_prc = command_proc.Command_Proc(g.gv.dl)
    task1 = asyncio.create_task(tac.Read_Instruments(Cmd_prc))
    task2 = asyncio.create_task(tac.doCmd(Cmd_prc))
    await task1
    await task2
    
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()