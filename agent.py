import os
import requests
import logging

class Neuron:
    def __init__(self, name, model, goal, tools=None):
        self.model = model
        self.name = name
        self.goal = goal
        self.soul= None
        self.tools = tools
        self.heart = None



        self.logger = self.make_logger()
        self.create_heart()

    def create_heart(self):
        ## creates folder holding agent files
        self.heart = f"neurons/{self.name}"
        
        os.makedirs(self.heart, exist_ok=True)

        soul_path = f"{self.heart}/soul.md"
        if not os.path.exists(soul_path):
            with open(soul_path, "w") as f:
                f.write("")                     # empty to save tokens
            self.logger.info(f"Created: {soul_path}")
        self.soul = soul_path  

    def make_logger(self):
        os.makedirs('logs', exist_ok=True)
        logger  = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)
        
        handler = logging.FileHandler(f"logs/{self.name}.log")
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(handler)

        console = logging.StreamHandler()
        console.setFormatter(logging.Formatter("%(name)s - %(message)s"))
        logger.addHandler(console)

        return logger

    def read_soul(self):
        ##loads soul into context
        if not self.soul:
            self.logger.warning(f"{self.name} has no soul")
            return ""
        else:
            self.logger.info(f"soul is present")
        soul = ""
        try:
            with open(soul, "r") as f:
                soul += f.read() +"--> /n/n above is your guidlines, below is your actions"
        except FileNotFoundError:
            self.logger.error(f"{self.name} soul file not found: {soul}")
        except Exception as e:
            self.logger.error(f"{self.name} failed to load {soul}: {e}")

            return soul.strip()
    def changeModel(self, newModel):
        self.logger.info(f"Model swapped: {self.model} → {newModel}")
        self.model = newModel

    def sculptSoul(self, memories):
        try:
            with open(self.soul, "w") as f:
                f.write(memories)
            self.logger.info(f"{self.name} sculpting soul")
        except Exception as e:
            self.logger.error(f"Failed to sculpt soul: {e}")        

    
    
