
# -*- coding: utf-8 -*-

""" DataLib.py

        Adapted from  Original issue - 03/12/2019 - KDT
"""

import time 

import datetime

class Register():
    def __init__(self, _i, _n, _v, _ts):
        self.index  = _i
        self.name = _n
        self.value = _v
        self.time_stamp = _ts

class DataLib():

    # Controller data manager

    def __init__(self):
        
        # Thermocouples

        init_ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

        self.SC_T1 = Register(1, 'SC_T1', 0.0, init_ts) #Temperature inside the sample chamber
        self.SC_T2 = Register(2, 'SC_T2', 0.0, init_ts) # Temperature of the temperature block /gas pre heater
        self.DPG_T1 = Register(3, 'DPG_T1', 0.0, init_ts) #Set point temperature of the dew point generator
        self.CC_T1 = Register(4, 'CC_T1', 0.0, init_ts) #Temperature of the conditioning chamber

        # Setpoints
        self.SC_T_Set = Register(5, 'SC_T_Set', 0.0, init_ts) #Sample chamber temp controller set point
        self.DPG_T_Set = Register(6, 'DPG_T_Set', 0.0, init_ts) #Conditioning chamber temp controller set point
        self.CC_T_Set = Register(7, 'CC_T_Set', 0.0, init_ts) #Dew point generator temp controller set point

        # PID values
            
        self.SC_P = Register(8, 'SC_P', 0.0, init_ts) #Sample chamber temp controller proportional gain
        self.SC_I = Register(9, 'SC_I', 0.0, init_ts) #Sample chamber temp controller integral gain
        self.SC_D = Register(10, 'SC_D', 0.0, init_ts) #Sample chamber temp controller differential gain

        self.DPG_P = Register(11, 'DPG_P', 0.0, init_ts) #DPG  temp controller proportional gain
        self.DPG_I = Register(12, 'DPG_I', 0.0, init_ts) #DPG  temp controllerintegral gain
        self.DPG_D = Register(13, 'DPG_D', 0.0, init_ts) #DPG  temp controller differential gain

        self.CC_P = Register(14, 'CC_P', 0.0, init_ts) #Conditioning chamber temp controller proportional gain
        self.CC_I = Register(15, 'CC_I', 0.0, init_ts) #Conditioning chamber temp controller proportional gain
        self.CC_D = Register(16, 'CC_D', 0.0, init_ts) #Conditioning chamber temp controller proportional gain

        # Controller State and Output 

        self.SC_State = Register(17,'SC_State', 0, init_ts) 
        self.SC_Output = Register(18,'SC_Output', 0.0, init_ts)
        self.DPG_State = Register(19,'DPG_State', 0, init_ts)
        self.DPG_Output = Register(20,'DPG_Output', 0.0, init_ts)
        self.CC_State = Register(21,'CC_State', 0, init_ts)
        self.CC_Output = Register(22,'CC_Output', 0.0, init_ts)
        
        # IRGA
        self.Cell_pressure = Register(23,'Cell_pressure', 0.0, init_ts) #Cell Pressure
        self.Cell_temp = Register(24,'Cell_temp', 0.0, init_ts) # Cell Temp
        self.IVOLT = Register(25, 'IVOLT', 0.0, init_ts) # Voltage supplied to IRGA
        self.pH2O = Register(26, 'pH2O', 0.0, init_ts)    # Partial pressure H20 (Pa)
        self.pCO2 = Register(27, 'pCO2', 0.0, init_ts)   # Partial pressure CO2 (Pa)
        self.Dew_point_temp = Register(28, 'Dew_point_temp', 0.0, init_ts)

        #Others

        self.Sample_weight = Register(29, 'Sample_weight', 0.0, init_ts) #Weight of the sample
        self.V_state = Register(30, 'V_state',0.0, init_ts) #Desired valve state – bypass/norma

        # Control
        self.Run = Register(31, "Run", 0, init_ts)

        #Status 

        self.Status = Register(32, "Status", 0, init_ts)

        # The parameter dictionary with register objects
        self.parmDict = {
            self.SC_T1.name : self.SC_T1,
            self.SC_T2.name : self.SC_T2, 
            self.DPG_T1.name : self.DPG_T1,
            self.CC_T1.name :  self.CC_T1,
            self.SC_T_Set.name : self.SC_T_Set,
            self.CC_T_Set.name: self.CC_T_Set,
            self.DPG_T_Set.name: self.DPG_T_Set,
            self.SC_P.name : self.SC_P, 
            self.SC_I.name : self.SC_I,
            self.SC_D.name : self.SC_D,
            self.DPG_P.name : self.DPG_P, 
            self.DPG_I.name : self.DPG_I,
            self.DPG_D.name : self.DPG_D,
            self.CC_P.name : self.CC_P, 
            self.CC_I.name : self.CC_I,
            self.CC_D.name : self.CC_D,
            self.SC_State.name : self.SC_State,
            self.SC_Output.name : self.SC_Output,
            self.DPG_State.name : self.DPG_Output,
            self.DPG_Output.name : self.DPG_Output,
            self.CC_State.name: self.CC_State,
            self.CC_Output.name: self.CC_Output,
            self.Cell_pressure.name: self.Cell_pressure,
            self.Cell_temp.name: self.Cell_temp,
            self.IVOLT.name: self.IVOLT,
            self.pH2O.name: self.pH2O,
            self.pCO2.name: self.pCO2,
            self.Dew_point_temp.name: self.Dew_point_temp,
            self.Sample_weight.name: self.Sample_weight,
            self.V_state.name: self.V_state,
            self.Run.name: self.Run,
            self.Status.name: self.Status
        }

    def getParmDict(self):
        
        return self.parmDict

    def get_all_data(self):

        ######### Function to get all the data at once from TA #########

        all_data_dict = {}

        string = ""

        for key in ['SC_T1', 'SC_T2', 'CC_T1', 'DPG_T1', 'pH2O', 'pCO2', 'Dew_point_temp', 'Sample_weight', 'Status']:

            string += str(self.parmDict[key].value) 

            string += ','

        return(string)

    def setParm(self, key, value, time_stamp):
        ######### Function to set a certain system variable's value #########
        if key in self.parmDict:
            self.parmDict[key].value = value
            self.parmDict[key].time_stamp = time_stamp
            return True
        else:
            return False

    def getParm(self, key):
        ######### Function to get a certain system variable's value #########
        if key in self.parmDict:
            value = self.parmDict[key].value
            time_stamp = self.parmDict[key].time_stamp
        else:
            value = float('NaN')
            time_stamp = 'NaN'
        return value, time_stamp

    def parmName(self, key):
        ######### Function to get a certain system variable's name #########
        if key in self.parmDict:
            name = self.parmDict[key].name
        else:
            name = ''
        return name