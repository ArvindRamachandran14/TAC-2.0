
import DataLib

class Command_Proc():
    """docstring for Command_Proc"""
    def __init__(self, dl, string, time_stamp):

        self.dl = dl

        self.string = string

        self.strings =  self.string.split('-')

        self.time_stamp = time_stamp


    def Do_it(self):
    
        print(self.strings)
        
        if self.strings in ([u''], [u'\n'], [u'\r']):
        
            return False

        elif self.strings[0] == 's':
            
            if self.strings[1] in self.dl.getParmDict().keys():

                setParm(self, self.strings[1], float(self.strings[2]), self.time_stamp)

                return('Ok')

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
