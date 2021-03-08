Developer - Arvind Ramachandran

Project title - Thermodynamic Analyzer

Contact - aramac13@asu.edu

# TAC-2.0

TAC-2.0 is the latest TAC program. TAC stands for ThermoAnalyzer Controller. This program is responsible for controlling system variables in the ThermoAnalyzer (TA), data acquisiton from the 5 different TA instruments, and handling the experimenter's commands via the TAGUI program. 

## Module Functionality

The different scripts here are different modules that have functions like

a. main.py - Contains the main machine loop. In the machine loop, two main tasks are handled. The first - the 5 instruments are read and the data is uptated in the register model. The second - commands from the user are read and are directed to the command processor. The replies from the command processor are sent back to the 
user via the TAGUI platform

b. Data_lib.py - Contains all system variables stored in a register model. Contains functions that enable system variable(s) to be set, modified or retrieved. 

c. Command_proc.py - Processing commands from the experimenter and getting the TA to do them 

d. Command_Dict.py - Contains a dictionary to hold command codes

e. Config.py - Enables you to read and update the PH2O.json, containing the PID values for the humidity control loop

f. global_variables.py - Contains all the variables that need to be accessed across different modules. 

g. IRGA.py - The IRGA module enables serial communication with the Infrared Gas Analyzer (IRGA)

f. TC.py - The TC module enables serial communication with the three different temperature controllers (Sample chamber, conditoning chamber, dew point generator temperature controllers)
