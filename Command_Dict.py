Command_Dict = {}

Command_Dict['power'] = '2d' 

#################################### Read thermistors ####################################

Command_Dict['SC_T1'] = '01'

Command_Dict['SC_T2'] = '06'

Command_Dict['CC_T1'] = '01'

Command_Dict['DPG_T1'] = '01'

#################################### Send set point commands ####################################

Command_Dict['SC_T_Set'] = '1c'

Command_Dict['CC_T_Set'] = '1c'

Command_Dict['DPG_T_Set'] = '1c'

#################################### Set proprtional bandwidth ####################################

Command_Dict['SC_P']  = '1d'

Command_Dict['CC_P']  = '1d'

Command_Dict['CC_P']  = '1d'

#################################### Set integral gain ####################################

Command_Dict['SC_I'] = '1e'

Command_Dict['CC_I'] = '1e'

Command_Dict['DPG_I'] = '1e'

#################################### Set derivative gain ####################################

Command_Dict['SC_D'] = '1f'

Command_Dict['CC_D'] = '1f'

Command_Dict['DPG_D'] = '1f'

#################################### R/W Control types ####################################

Command_Dict['set_ctl_type'] =  '2b'

Command_Dict['read_ctl_type'] = '44'

#################################### Other commands ####################################

Command_Dict['read_propotional_width'] = '51'

Command_Dict['read_integral_gain'] = '52'

Command_Dict['read_derivative_gain'] = '53'
