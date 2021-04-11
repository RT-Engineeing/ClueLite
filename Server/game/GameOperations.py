from random import randint


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


class SessionState:
    def __init__(self, name, uid):
        self.name = name
        self.uid = uid

    def getName(self):
        return self.name

    def getUid(self):
        return self.uid

    def setName(self, name):
        self.name = name

    def setUid(self, uid):
        self.uid = uid

    def isSessionFull(self, uid, sessionplayers):
        if sessionplayers == 6:
            return True
        return False


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


class weapdeck:
    def __init__(self, deck):
        self.cards = deck

    def dealcard(self):
        val = randint(0, len(self.cards))
        return self.cards[val]


class chardeck:
    def __init__(self, deck):
        self.cards = deck

    def dealcard(self):
        val = randint(0, len(self.cards))
        return self.cards[val]


class roomsdeck:
    def __init__(self, deck):
        self.cards = deck

    def dealcard(self):
        val = randint(0, len(self.cards))
        return self.cards[val]
