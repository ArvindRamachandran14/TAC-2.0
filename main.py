import DataLib

import serial

import IRGA

import TC

import Command_proc

import datetime

import time

import global_variables as g

def main():

    #################################   Define Serial Ports   ################################# 

    g.gv.TC_CC.set_control_type()

    g.gv.TC_CC.power_on()

    #TC_SC.power_off()

    #TC_DPG.power_off()

    try:

        while True:
            
            current_time = time.time()
        
            time_stamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
            
            Read_Instruments(g.gv.dl, g.gv.irga, g.gv.TC_SC, g.gv.TC_CC, g.gv.TC_DPG, time_stamp)

            Cmd_prc = Command_proc.Command_Proc(g.gv.dl, g.gv.ser_PC.readline().decode(), time_stamp)
            
            Output = Cmd_prc.Do_it()
            
            #print(type(Output))
            
            if isinstance(Output, bool):
                
                pass

            elif isinstance(Output, tuple):
            
                g.gv.ser_PC.write((str(Output[0])+'---'+str(Output[1])).encode())
            
                g.gv.ser_PC.write(('\r'+'\n').encode())

            else:

                g.gv.ser_PC.write(Output.encode())
                
                g.gv.ser_PC.write(('\r'+'\n').encode())
          
            
            #print('Timestamp: '+ str(time_stamp))
            
            #print('pCO2: '+ str(dl.getParm('pCO2'))+ ' ppm')
            
            #print('pH2O: '+ str(dl.getParm('pH2O'))+ ' ppt')
            
            #print('Cell Temp: ' + str(dl.getParm('Cell_temp'))+ ' C')
            
            #print('Cell Pressure: ' + str(dl.getParm('Cell_pressure'))+ ' kPa')

            #print('Cell Voltage: ' + str(dl.getParm('IVOLT'))+ ' V')
            
            #print('\n')
        
    except KeyboardInterrupt:
	   g.gv.TC_CC.power_off()
     print('Terminated')
    
 
def Read_Instruments(dl, irga, TC_SC, TC_CC, TC_DPG, time_stamp):
    
    #print(irga.read_IRGA())
   
   #print('reading instruments')
   
   IRGA_list = g.gv.irga.read_IRGA()

   #TC_list = [0,0,0,0]

   TC_list = [g.gv.TC_SC.read_temperature(0), g.gv.TC_SC.read_temperature(1), g.gv.TC_CC.read_temperature(0), g.gv.TC_DPG.read_temperature(0)]
   
   g.gv.dl.setParm('pCO2', IRGA_list[0], time_stamp)

   g.gv.dl.setParm('pH2O', IRGA_list[1], time_stamp)
   
   g.gv.dl.setParm('Cell_pressure', IRGA_list[2], time_stamp)
   
   g.gv.dl.setParm('Cell_temp', IRGA_list[3], time_stamp)
   
   g.gv.dl.setParm('IVOLT', IRGA_list[4], time_stamp)

   g.gv.dl.setParm('SC_T1', TC_list[0], time_stamp)

   g.gv.dl.setParm('SC_T2', TC_list[1], time_stamp)

   g.gv.dl.setParm('CC_T1', TC_list[2], time_stamp)

   g.gv.dl.setParm('DPG_T1', TC_list[3], time_stamp)

main()
