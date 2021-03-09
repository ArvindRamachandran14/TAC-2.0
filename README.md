Developer - Arvind Ramachandran

Project title - Thermodynamic Analyzer

Contact - aramac13@asu.edu

# TAC-2.0

ThermoAnalyzer Controller (TAC) is a Python-based program responsible for controlling system variables in the ThermoAnalyzer (TA), data acquisition from the 5 different TA instruments, and handling the experimenter's commands via the TAGUI program

TAC-2.0 is implemented in a Raspberry Pi computer in the CNCE lab at Arizona State University. To run the program, the Raspberry Pi needs to be connected to the TA and its instruments.

## Module Functionality

The different scripts here are different modules that have functions like

1. `main.py` Contains the main machine loop. In the machine loop, two main tasks are handled. The first - the 5 instruments are read and the data is uptated in the register model. The second - commands from the user are read and are directed to the command processor. The replies from the command processor are sent back to the user via the TAGUI platform

2. `data_lib.py` Contains all system variables stored in a register model. Contains functions that enable system variable(s) to be set, modified or retrieved. 

3. `command_proc.py` Processing commands from the experimenter and getting the TA to do them 

4. `command_dict.py` Contains a dictionary to hold command codes

5. `config.py` Enables you to read and update the PH2O.json, containing the PID values for the humidity control loop

6. `global_variables.py` Contains all the variables that need to be accessed across different modules. 

7. `IRGA.py` The IRGA module enables serial communication with the Infrared Gas Analyzer (IRGA)

8. `tc.py` The TC module enables serial communication with the three different temperature controllers (Sample chamber, conditioning chamber, dew point generator temperature controllers)

The TA is an apparatus that is used to study the thermodynamics of Direct Air Capture sorbents. Direct Air Capture (DAC) is the process of capturing CO2 from the atmosphere, as a way of managing the build up of CO2 in the atmosphere. You can learn more about DAC [here](https://cnce.engineering.asu.edu)