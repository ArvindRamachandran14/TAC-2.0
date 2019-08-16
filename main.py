import DataLib

import serial

import IRGA

import TC

import Command_proc

import datetime

import time

def main():


    #################################   Define Serial Ports   ################################# 

    ser_TC_SC = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)

    ser_TC_DPG = serial.Serial('/dev/ttyUSB2', 9600, timeout=1)

    ser_TC_CC = serial.Serial('/dev/ttyUSB3', 9600, timeout=1)

    ser_IRGA= serial.Serial('/dev/ttyUSB4', 9600, timeout=1)

    ser_PC = serial.Serial('/dev/ttyUSB0', 9600, timeout=3)


    #################################   Object creation   ################################# 

    dl = DataLib.DataLib()  # initialization triggered when object is created 

    irga = IRGA.IRGA(ser_IRGA)

    TC_SC = TC.TC(ser_TC_SC)

    TC_CC = TC.TC(ser_TC_CC)

    TC_DPG = TC.TC(ser_TC_DPG)

    #TC_CC.power_off()

    #TC_SC.power_off()

    #TC_DPG.power_off()

    try:

        while True:
            
            current_time = time.time()
        
            time_stamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
            
            Read_Instruments(dl, irga, TC_SC, TC_CC, TC_DPG, time_stamp)

            Cmd_prc = Command_proc.Command_Proc(dl, ser_PC.readline().decode(), time_stamp)
            
            Output = Cmd_prc.Do_it()
            
            print(Output)
            
            if isinstance(Output, bool):
                
                pass
            
            elif isinstance(Output, str):
                
                ser_PC.write(Output.encode())
                
                ser_PC.write(('\r'+'\n').encode())
            
            else:
            
                ser_PC.write((str(Output[0])+'---'+str(Output[1])).encode())
            
                ser_PC.write(('\r'+'\n').encode())
            
            #print('Timestamp: '+ str(time_stamp))
            
            #print('pCO2: '+ str(dl.getParm('pCO2'))+ ' ppm')
            
            #print('pH2O: '+ str(dl.getParm('pH2O'))+ ' ppt')
            
            #print('Cell Temp: ' + str(dl.getParm('Cell_temp'))+ ' C')
            
            #print('Cell Pressure: ' + str(dl.getParm('Cell_pressure'))+ ' kPa')

            #print('Cell Voltage: ' + str(dl.getParm('IVOLT'))+ ' V')
            
            #print('\n')
        
    except KeyboardInterrupt:
        print('Terminated')
    
 
def Read_Instruments(dl, irga, TC_SC, TC_CC, TC_DPG, time_stamp):
    
    #print(irga.read_IRGA())
   
   print('reading instruments')
   
   IRGA_list = irga.read_IRGA()

   TC_list = [TC_SC.read_temperature(0), TC_CC.read_temperature(0), TC_DPG.read_temperature(0)]
   
   dl.setParm('pCO2', IRGA_list[0], time_stamp)

   dl.setParm('pH2O', IRGA_list[1], time_stamp)
   
   dl.setParm('Cell_pressure', IRGA_list[2], time_stamp)
   
   dl.setParm('Cell_temp', IRGA_list[3], time_stamp)
   
   dl.setParm('IVOLT', IRGA_list[4], time_stamp)

   dl.setParm('SC_T1', TC_list[0], time_stamp)

   dl.setParm('CC_T1', TC_list[1], time_stamp)

   dl.setParm('DPG_T1', TC_list[2], time_stamp)

main()