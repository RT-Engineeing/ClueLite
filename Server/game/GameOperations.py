from random import randint
from flask import session, jsonify
import uuid


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
    def __init__(self, uid, gamestate):
        self.uid = uid
        self.gamestate = gamestate

    def getUid(self):
        return session['uid']

    def setUid(self, uid):
        self.uid = uid

    def getGameState(self):
        return self.gamestate

    def setGameState(self, gamestate):
        return self.gamestate

    def isSessionFull(self, uid, maxSessionPlayers):
        if maxSessionPlayers == 6:
            return True
        return False

    def createSession(self, playername, maxSessionPlayers):
        if maxSessionPlayers == 0 or maxSessionPlayers >= 6:
            session['uid'] = uuid.uuid4()
            session['playername'] = playername
            maxSessionPlayers += 1

            return jsonify(
                sessionId=str(session['uid']),
                playername=session['playername'],
                totalPlayers=maxSessionPlayers,
                result=playername + "has been added to the session."
            )
        else:
            session['uid'] = uuid.uuid4()
            if 'playername' not in session:
                session['playername'] = playername
                maxSessionPlayers += 1
            return jsonify(
                sessionId=str(session['uid']),
                playername=session['playername'],
                totalPlayers=maxSessionPlayers,
                result=playername + " has been added to the session."
            )

    def endSession(self, uid, gamestate):
        uid = session['uid']
        session.pop('uid', None)
        gamestate.setGameRunning(False)
        return jsonify(
            sessionId=uid,
            result="The session has been terminated."
        )


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
