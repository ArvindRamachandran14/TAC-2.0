
############## Script that reads and records the pCO2 values. Intended to run a CO2 leak test ##############


import serial 

#Line added on trial branch

Input_string = 'g-pCO2\n'


file_name = 'CO2_leak_test.txt'

file = open(file_name, 'w')

ser = serial.Serial('/dev/tty.usbserial-FTY3UOSS',9600,timeout=3)


try:

	while True:

		ser.write(Input_string.encode())

		Output_strings = ser.readline().decode()
	
		file.write(Output_strings.split('---')[0])
		file.write('	')
		file.write(Output_strings.split('---')[1])
		file.write('\n')

except KeyboardInterrupt:

	file.close()

	ser.close()
