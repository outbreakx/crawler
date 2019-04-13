import json,random

class UserAgents:
    def __init__(self):
        with open('user-agents.json') as json_file:  
            self.user_agents = json.load(json_file)
            self.len = len(self.user_agents)

    def getRandomUserAgent(self):
        random_index = random.randint(0,self.len-1)
        return self.user_agents[random_index]