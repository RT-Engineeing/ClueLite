from flask import jsonify
class Session:
    def __init__(self, uid, gamestate):
        self.uid = uid
        self.gamestate = gamestate
        self.playernum = 0
        self.players = []

    def addPlayer(self, playername):
        self.players.append(playername)

    def removePlayer(self, playername):
        self.players.remove(playername)

    def getReady(self):
        return self.players

    def getPlayernum(self):
        return self.playernum

    def setPlayernum(self, playernum):
        self.playernum = playernum

    def getUid(self):
        return self.uid;

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

    def setReady(self, uid, playername, isReady):
        if isReady is True:
            if self.getReady() is True:
                self.gamestate.setGameRunning(True)
                self.gamestate.setPlayerturn(1)
            return jsonify(
                sessionId=uid,
                playername=playername,
                playerready=str(isReady),
                result=playername + " is ready."
            )
        return jsonify(
            sessionId=uid,
            playername=playername,
            playerready=str(isReady),
            result=playername + " is not ready."
        )

