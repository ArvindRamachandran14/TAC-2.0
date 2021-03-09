import json

class Config():

    """class that holds the PID parameters for humidity control loop"""

    def __init__(self):
        self.cfgFile = 'pH2O_PID.json'
        self.cfg = json.load(open(self.cfgFile,'r'))
        self.pH2O_P = self.cfg["pH2O_P"]
        self.pH2O_I = self.cfg["pH2O_I"]
        self.pH2O_D = self.cfg["pH2O_D"]
        #print(pH2O_P, pH2O_I, pH2O_D)

    def update(self):

        """funciton that updates the json file the current PID parameters for humidity control loop"""
        
        self.cfg["pH2O_P"] = self.pH2O_P
        self.cfg["pH2O_I"] = self.pH2O_I
        self.cfg["pH2O_D"] = self.pH2O_D
        with open(self.cfgFile, 'w') as fCfg:
            json.dump(self.cfg, fCfg)