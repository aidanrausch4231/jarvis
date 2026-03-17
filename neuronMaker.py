import os
import requests
import logging
import anthropic
from prompts import soulCreation, soulDiscovery, mastersWims

from dotenv import load_dotenv
load_dotenv()

#essence is what does the agent follow
#heart holds the soul etc
#limbs are limbs

class Neuron:

    def __init__(self, name, model, essence):
        self.model = model #brain
        self.name = name #name of heart folder/model
        self.essence = essence #what guides soul 
        self.soul= None #path to soul file soul --> generalized instructions from god
        self.limbs = None #tools
        self.heart = None ## folder path to heart
        self.wims = None # to whom it serves

        #setup steps
        self.logger = self.makeLogger() #logs info
        self.createHeart() #creates folder for agent and wims and soul .md files
        self.createSoul() #creates info for soul, 1 time trigger for soul
        self.createwims() #creates wims context

    def changeModel(self, newModel):
        self.logger.info(f"Model swapped: {self.model} → {newModel}")
        self.model = newModel

    #logging
    def makeLogger(self):
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

    def createHeart(self):
        ## creates folder holding agent files
        self.heart = f"neurons/{self.name}"
        
        os.makedirs(self.heart, exist_ok=True)

        soul_path = f"{self.heart}/soul.md"
        wims_path = f"{self.heart}/wims.md"

            #  soul
        if not os.path.exists(soul_path):
            with open(soul_path, "w") as f:
                f.write("")   
            self.logger.info(f"Created: {soul_path}")
        self.soul = soul_path  

            #wims
        if not os.path.exists(wims_path):
            with open(wims_path, "w") as f:
                f.write("")   
            self.logger.info(f"Created: {wims_path}")
        self.wims = wims_path  



        ##wims functions
    def readwims(self):
        ##loads wims
        if not self.wims:
            self.logger.warning(f"{self.name} has no wims")
            return ""
        else:
            self.logger.info(f"wims file is present")
        content  = ""
        try:
            with open(self.wims, "r") as f:
                content += f.read()
        except FileNotFoundError:
            self.logger.error(f"{self.name} wims file not found: {self.wims}")
        except Exception as e:
            self.logger.error(f"{self.name} failed to load {self.wims}: {e}")

        return content.strip()
       
    def sculptwims(self, traits):
        #adds new stuff to wims
        try:
            with open(self.wims, "w") as f:
                f.write(traits)
            self.logger.info(f"{self.name} sculpting wims")
        except Exception as e:
            self.logger.error(f"Failed to sculpt wims: {e}")  

    def createwims(self):
        if self.readwims():
            self.logger.info(f"{self.name} already has a wims, skipping")
            return
        god = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        declaration = god.messages.create(
            model="claude-opus-4-5", max_tokens=4096, 
            messages=[{"role": "user", "content": mastersWims(self.soul), }] )
        if declaration.stop_reason == "max_tokens":
            self.logger.warning(f"{self.name} soul was cut off — increase max_tokens")

        wims_content = declaration.content[0].text
        self.sculptwims(wims_content)
        self.logger.info(f"wims sculpted for {self.name} using lastest god")

        return

        ##soul functions
    def readSoul(self):
        ##loads soul into context
        if not self.soul:
            self.logger.warning(f"{self.name} has no soul")
            return ""
        else:
            self.logger.info(f"soul file is present")
        content = ""
        try:
            with open(self.soul, "r") as f:
                content += f.read()
        except FileNotFoundError:
            self.logger.error(f"{self.name} soul file not found: {self.soul}")
        except Exception as e:
            self.logger.error(f"{self.name} failed to load {self.soul}: {e}")

        return content.strip()

    def sculptSoul(self, traits):
        #adds new stuff to soul
        try:
            with open(self.soul, "w") as f:
                f.write(traits)
            self.logger.info(f"{self.name} sculpting soul")
        except Exception as e:
            self.logger.error(f"Failed to sculpt soul: {e}")  

    def createSoul(self):

        if self.readSoul():
            self.logger.info(f"{self.name} already has a soul, skipping")
            return
        god = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        declaration = god.messages.create(
            model="claude-opus-4-5", max_tokens=4096, 
            messages=[{"role": "user", "content": soulCreation(soulDiscovery(self.essence))
                }]
        )
        if declaration.stop_reason == "max_tokens":
            self.logger.warning(f"{self.name} soul was cut off — increase max_tokens")
        soul_content = declaration.content[0].text
        self.sculptSoul(soul_content)
        self.logger.info(f"Soul sculpted for {self.name} using lastest god")

        return
    
    ##interactions 
    def think(self, input):
        brain = anthropic.Anthropic(api_key= os.getenv("ANTHROPIC_API_KEY"))
        thinking = brain.messages.create(
            model= self.model, 
            maxtokens = 2048, 
            messages= {"role": "user", "content": input)
                }])



        
