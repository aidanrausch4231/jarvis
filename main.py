from neuron import Neuron
from neurons.gmail.gmailNeuron import GmailNeuron
def main():

    # create the agent
    gmail = GmailNeuron()

    # call it
    reply, history = gmail.think("write an email draft to big time ceo about me getting big time job please to matt wilkson at Monsoon for software engineer-- i already had an internship last yar at his b2b sas company that does book sales")
    
    print(reply)
    reply, history = gmail.think("adjust email to add claims from resume")
    print("\n\n this is the histroy \n\n")
    print (history)
if __name__ == "__main__": 
    main()