from flask import jsonify
class Session:
    def __init__(self, sessionId, gamestate):
        self.sessionId = sessionId
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

    def getSessionid(self):
        return self.sessionId;

    def setSessionid(self, sessionId):
        self.sessionId = sessionId

    def getGameState(self):
        return self.gamestate

    def setGameState(self, gamestate):
        return self.gamestate

    def isSessionFull(self, sessionId, maxSessionPlayers):
        if maxSessionPlayers == 6:
            return True
        return False

    def setReady(self, sessionId, playername, isReady):
        if isReady is True:
            if self.getReady() is True:
                self.gamestate.setGameRunning(True)
                self.gamestate.setPlayerturn(1)
            return jsonify(
                sessionId=sessionId,
                playername=playername,
                playerready=str(isReady),
                result=playername + " is ready."
            )
        return jsonify(
            sessionId=sessionId,
            playername=playername,
            playerready=str(isReady),
            result=playername + " is not ready."
        )

