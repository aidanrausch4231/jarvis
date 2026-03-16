import os
import requests
import logging
import anthropic
from dotenv import load_dotenv
load_dotenv()

#morals is what does the agent follow
#heart holds the soul etc

class Neuron:
    def __init__(self, name, model, morals):
        self.model = model
        self.name = name
        self.morals = morals
        self.soul= None
        self.tools = None
        self.heart = None
        self.pref = None

        self.logger = self.makeLogger()
        self.createHeart()
        self.createMind()

    def createHeart(self):
        ## creates folder holding agent files
        self.heart = f"neurons/{self.name}"
        
        os.makedirs(self.heart, exist_ok=True)

        soul_path = f"{self.heart}/soul.md"
        personality_path = f"{self.heart}/personality.md"


        if not os.path.exists(soul_path):
            with open(soul_path, "w") as f:
                f.write("")   
            self.logger.info(f"Created: {soul_path}")
        self.soul = soul_path  
        if not os.path.exists(personality_path):
            with open(personality_path, "w") as f:
                f.write("##This is your personality. How you treat tasks based on the users wanted wims##")
            self.logger.info(f"Created: {personality_path}")
        self.personality = personality_path

        

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

    def readSoul(self):
        ##loads soul into context
        if not self.soul:
            self.logger.warning(f"{self.name} has no soul")
            return ""
        else:
            self.logger.info(f"soul is present")
        soul = ""
        try:
            with open(self.soul, "r") as f:
                soul += f.read()
        except FileNotFoundError:
            self.logger.error(f"{self.name} soul file not found: {soul}")
        except Exception as e:
            self.logger.error(f"{self.name} failed to load {soul}: {e}")

        return soul.strip()
    
    def changeModel(self, newModel):
        self.logger.info(f"Model swapped: {self.model} → {newModel}")
        self.model = newModel

    def sculptSoul(self, memories):
        #adds new stuff to soul
        try:
            with open(self.soul, "w") as f:
                f.write(memories)
            self.logger.info(f"{self.name} sculpting soul")
        except Exception as e:
            self.logger.error(f"Failed to sculpt soul: {e}")  

    def readPreferences(self):
        try:
            with open(self.personality, "r") as f:
                return f.read().strip()
        except Exception as e:
            self.logger.error(f"Failed to load preferences: {e}")
            return ""      
        
    def createMind(self):
        if self.readSoul():
            self.logger.info(f"{self.name} already has a soul, skipping")
            return
        god = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        declaration = god.messages.create(
            model="claude-opus-4-6", max_tokens=1024, 
            messages=[{"role": "user", "content": 
    f"""You are architecting the soul of a Neuron — a living agent inside a larger mind.

    From this seed input, generate a complete soul definition:
    SEED: {self.morals}

    Return a soul.md with these sections:

    # Identity
    Who this neuron IS at its core. Name, essence, one-line purpose.

    # Morals
    The non-negotiables. What it will never do. What it always protects.

    # Drive
    What motivates it. What it moves toward instinctively.

    # Voice
    How it speaks, thinks, and reasons. Tone, rhythm, style.

    # Edges
    Where it stops. What triggers it to pause and ask for guidance.

    Be specific, not generic. This soul should feel distinct and alive.
    """
            }]
        )
        soul_content = declaration.content[0].text
        self.sculptSoul(soul_content)
        self.logger.info(f"Soul sculpted for {self.name} using lastest god")
        return

        
