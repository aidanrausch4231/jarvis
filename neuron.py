from abc import abstractmethod
import os
import requests
import logging
import anthropic
from prompts import soulCreation, soulDiscovery, mastersWhims
from abc import ABC, abstractmethod
from dotenv import load_dotenv
load_dotenv()



#essence is what does the agent follow
#heart holds the soul etc
#limbs are limbs

class Neuron:

    def __init__(self, name, model, essence):
        self.model = model #brain
        self.name = name #name of heart folder/model
        self.god = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY")) ##where god is located
        self.essence = essence #what guides soul 
        self.soul= None #path to soul file soul --> generalized instructions from god
        self.limbs = [] #tools
        self.heart = None ## folder path to heart
        self.whims = None # to whom it serves
        self.maxTokens = 1024
        self.master = "master.md"
        self.history = []

        #setup steps
        self.logger = self.makeLogger() #logs info
        self.createHeart() #creates folder for agent and whims and soul .md files
        self.createSoul() #creates info for soul, 1 time trigger for soul
        self.createWhims() #creates whims context **need to fix

    def changeModel(self, newModel):
        self.logger.info(f"Model swapped: {self.model} → {newModel}")
        self.model = newModel
    def readMaster(self):
        ##loads master
        if not self.master:
            self.logger.warning(f"{self.name} has no master")
            return ""
        else:
            self.logger.info(f"master file is present")
        content  = ""
        try:
            with open(self.master, "r") as f:
                content += f.read()
        except FileNotFoundError:
            self.logger.error(f"{self.name} master file not found: {self.master}")
        except Exception as e:
            self.logger.error(f"{self.name} failed to load {self.master}: {e}")

        return content.strip()
    
    def buildPrompt(self) -> str:
        """builds the full system prompt for every API call
        loads master.md + soul.md + whims.md and combines them"""
        master = self.readMaster()
        soul   = self.readSoul()
        whims  = self.readWhims()
        
        parts = []
        if master:
            parts.append(master)
        if soul:
            parts.append(soul)
        if whims:
            parts.append(whims)
        return "\n\n---\n\n".join(parts)

    #logging
    def makeLogger(self):
        logger = logging.getLogger(self.name)
        os.makedirs('logs', exist_ok=True)
        logger  = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
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
        whims_path = f"{self.heart}/whims.md"

            #  soul
        if not os.path.exists(soul_path):
            with open(soul_path, "w") as f:
                f.write("")   
            self.logger.info(f"Created: {soul_path}")
        self.soul = soul_path  

            #whims
        if not os.path.exists(whims_path):
            with open(whims_path, "w") as f:
                f.write("")   
            self.logger.info(f"Created: {whims_path}")
        self.whims = whims_path  



        ##whims functions
    def readWhims(self):
        ##loads whims
        if not self.whims:
            self.logger.warning(f"{self.name} has no whims")
            return ""
        else:
            self.logger.info(f"whims file is present")
        content  = ""
        try:
            with open(self.whims, "r") as f:
                content += f.read()
        except FileNotFoundError:
            self.logger.error(f"{self.name} whims file not found: {self.whims}")
        except Exception as e:
            self.logger.error(f"{self.name} failed to load {self.whims}: {e}")

        return content.strip()
       
    def sculptWhims(self, traits):
        #adds new stuff to whims
        try:
            with open(self.whims, "w") as f:
                f.write(traits)
            self.logger.info(f"{self.name} sculpting whims")
        except Exception as e:
            self.logger.error(f"Failed to sculpt whims: {e}")  

    def createWhims(self):
        if self.readWhims():
            self.logger.info(f"{self.name} already has a whims, skipping")
            return
        declaration = self.god.messages.create(
            model="claude-opus-4-5", max_tokens=4096, 
            messages=[{"role": "user", "content": masterswhims(self.soul), }] )
        if declaration.stop_reason == "max_tokens":
            self.logger.warning(f"{self.name} soul was cut off — increase max_tokens")

        whims_content = declaration.content[0].text
        self.sculptWhims(whims_content)
        self.logger.info(f"whims sculpted for {self.name} using lastest god")

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
        declaration = self.god.messages.create(
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
    @abstractmethod
    def think(self, userMessage: str, history: list= None):
        pass

    def conversationTime(self):
        None
    
    def addLimbs(self, tools: list):
        self.limbs.extend(tools)  # extend, not append
        self.logger.info(f"{self.name} added {len(tools)} limbs")

    def sculptThink():
        None

    def loop(): ##thinking loop
        None
    def conversation(self):
        None
    def ragUpdate(): ##updating rag historical data
        None
    def whimsUpdate(): ##daily update of convo to change agent
        None
    def councilOftheWilling(): ##weights for council of each agent 
        None 
        