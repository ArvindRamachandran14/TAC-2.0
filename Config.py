

import json

class Config():

    def __init__(self):

        self.cfgFile = 'pH2O_PID.json'
        self.cfg = json.load(open(self.cfgFile,'r'))
        self.pH2O_P = self.cfg["pH2O_P"]
        self.pH2O_I = self.cfg["pH2O_I"]
        self.pH2O_D = self.cfg["pH2O_D"]

        #print(pH2O_P, pH2O_I, pH2O_D)

    def update(self):

        self.cfg["pH2O_P"] = self.pH2O_P
        self.cfg["pH2O_I"] = self.pH2O_I
        self.cfg["pH2O_D"] = self.pH2O_D

        with open(cfgFile, 'w') as fCfg:

            json.dump(cfg, fCfg)

