from random import randint

class Players:
    def __init__(self, name, uid, character, hand, location):
        self.name = name
        self.uid = uid
        self.character = character
        self.hand = hand
        self.location = location

    def getName(self):
        return self.name

    def getUid(self):
        return self.uid

    def getCharacter(self):
        return self.character

    def getHand(self):
        return self.hand

    def getLocation(self):
        return self.location

    def setName(self, name):
        self.name = name

    def setUid(self, uid):
        self.name = uid

    def setCharacter(self, character):
        self.character = character

    def setHand(self, hand):
        self.hand = hand

    def setLocation(self, location):
        self.location = location

class Weapons:
    def __init__(self, name, location):
        self.name = name
        self.location = location

    def getName(self):
        return self.name

    def getLocation(self):
        return self.location

    def setName(self, name):
        self.name = name

    def setLocation(self, location):
        self.location = location


class Weapdeck:
    def __init__(self, deck):
        self.cards = deck

    def dealcard(self):
        val = randint(0, len(self.cards))
        return self.cards[val]


class Chardeck:
    def __init__(self, deck):
        self.cards = deck

    def dealcard(self):
        val = randint(0, len(self.cards))
        return self.cards[val]


class Roomsdeck:
    def __init__(self, deck):
        self.cards = deck

    def dealcard(self):
        val = randint(0, len(self.cards))
        return self.cards[val]
