
import global_variables as g

class Command_Proc():
    """docstring for Command_Proc"""

    def __init__(self, dl, string, time_stamp):

        self.dl = dl

        self.string = string

        self.strings =  self.string.split('-')

        self.time_stamp = time_stamp


    def Do_it(self):
    
        #print(self.strings)
        
        if self.strings in ([u''], [u'\n'], [u'\r']):
        
            return False

        elif self.strings[0] == 's':
            
            if self.strings[1] in self.dl.getParmDict().keys():
                
                #print(float(self.strings[2]))

                self.dl.setParm(self.strings[1], float(self.strings[2]), self.time_stamp)
                
                #print(self.dl.getParmDict(self.strings[1])) 

                if self.strings[1] in ['SC_T_Set', 'CC_T_Set', 'DPG_T_Set']:

                    if self.strings[1] == 'SC_T_Set':

                        return(g.gv.TC_SC.set_temperature(float(self.strings[2])))

                    elif self.strings[1] == 'CC_T_Set':

                        return(g.gv.TC_CC.set_temperature(float(self.strings[2])))

                    elif self.strings[1] == 'DPG_T_Set':strings

                        return(g.gv.TC_DPG.set_temperature(float(self.strings[2])))

            else:

                return('Input Error')

        elif self.strings[0] == 'g':

            if self.strings[1][:-1] in self.dl.getParmDict().keys():

                return(self.dl.getParm(self.strings[1][:-1]))
            
            else:
            
                return('Input Error')

        else:
            
            print(self.strings)

            return('Input Error')
