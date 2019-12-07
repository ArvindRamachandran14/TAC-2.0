

Command_Dict = {}

################################### Power ####################################

Command_Dict['power_write'] = '2d' 

Command_Dict['power_read'] = '46'

Command_Dict['power_output_read'] = '02'

#################################### Read thermistors ####################################

Command_Dict['SC_T1_read'] = '01'

Command_Dict['SC_T2_read'] = '06'

Command_Dict['CC_T1_read'] = '01'

Command_Dict['DPG_T1_read'] = '01'

#################################### Write set point  ####################################

Command_Dict['SC_T_Set_write'] = '1c'

Command_Dict['CC_T_Set_write'] = '1c'

Command_Dict['DPG_T_Set_write'] = '1c'


#################################### Read set point  ####################################

Command_Dict['SC_T_Set_read'] = '50'

Command_Dict['CC_T_Set_read'] = '50'

Command_Dict['DPG_T_Set_read'] = '50'

#################################### Write proprtional bandwidth ####################################

Command_Dict['SC_P_write']  = '1d'

Command_Dict['CC_P_write']  = '1d'

Command_Dict['DPG_P_write']  = '1d'

#################################### Read proprtional bandwidth ####################################

Command_Dict['SC_P_read']  = '51'

Command_Dict['CC_P_read']  = '51'

Command_Dict['DPG_P_read']  = '51'

#################################### Write integral gain ####################################

Command_Dict['SC_I_write'] = '1e'

Command_Dict['CC_I_write'] = '1e'

Command_Dict['DPG_I_write'] = '1e'

#################################### Read integral gain ####################################

Command_Dict['SC_I_read']  = '52'

Command_Dict['CC_I_read']  = '52'

Command_Dict['DPG_I_read']  = '52'


#################################### Write derivative gain ####################################

Command_Dict['SC_D_write'] = '1f'

Command_Dict['CC_D_write'] = '1f'

Command_Dict['DPG_D_write'] = '1f'


#################################### Read derivative gain ####################################

Command_Dict['SC_D_read'] = '53'

Command_Dict['CC_D_read'] = '53'

Command_Dict['DPG_D_read'] = '53'

#################################### R/W Control types ####################################

Command_Dict['set_ctl_type'] =  '2b'

Command_Dict['read_ctl_type'] = '44'

#################################### Other commands ####################################
