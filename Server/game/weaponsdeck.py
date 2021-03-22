from random import randint
class weapdeck:
    def __init__(self, deck):
        self.cards = deck
    def dealcard(self):
        val = randint(0,len(self.cards))
        return self.cards[val]