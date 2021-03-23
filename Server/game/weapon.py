class Weapons: 
    def __init__(self, name, location, weapnum):
        self.name = name
        self.location = location
        self.weapnum = weapnum
    
    def getWeapon(self):
        return self.weapnum
    def getName(self):
        return self.name 
    def getLocation(self):
        return self.location
    def setWeapnum(self, weapnum):
        self.weapnum = weapnum
    def setName(self, name):
        self.name = name 
    def setLocation(self, location):
        self.location = location
