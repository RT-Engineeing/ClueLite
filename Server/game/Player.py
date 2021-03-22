class Players: 
    def __init__(self, name, character, hand, location):
        self.name = name
        self.character = character
        self.hand = hand
        self.location = location
    
    def getName(self):
        return self.name 
    def getCharacter(self):
        return self.character
    def getHand(self):
        return self.hand
    def getLocation(self):
        return self.location
    def setName(self, name):
        self.name = name 
    def setCharacter(self, character):
        self.character = character
    def setHand(self, hand):
        self.hand = hand
    def setLocation(self, location):
        self.location = location
