class Player:
    def __init__(self, name, character, location, weapon):
        self.name = name
        self.character = character
        self.location = location
        self.weapon = weapon
    def getName(self):
        return self.name
    def getCharacter(self):
        return self.character
    def getLocation(self):
        return self.location
    def getWeapon(self):
        return self.weapon
    def setName(self, name):
        self.name = name
    def setCharacter(self, character):
        self.character = character
    def setLocation(self, location):
        self.location = location
    def setWeapon(self, weapon):
        self.weapon = weapon
