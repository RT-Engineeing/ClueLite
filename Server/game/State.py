class GameState: 
    def __init__(self, casefile, numofplayers, playerturn, gamewon, gameboard, gamerunning, subturn):
        self.numofplayers = numofplayers
        self.playerturn = playerturn
        self.gamewon = gamewon
        self.gameboard = gameboard
        self.gamerunning = gamerunning 
        self.casefile = casefile
        self.subturn = subturn

    def getSubturn(self):
        return self.subturn
    def getCasefile(self):
        return self.casefile
    def getNumOfPlayers(self):
        return self.numofplayers
    def getPlayerturn(self):
        return self.playerturn
    def getGameWon(self):
        return self.gamewon
    def getGameBoard(self):
        return self.gameboard
    def getGameRunning(self):
        return self.gamerunning
    def setSubturn(self):
        self.subturn = subturn
    def setCasefile(self, casefile):
        self.casefile = casefile
    def setGameBoard(self, gameboard):
        self.gameboard = gameboard
    def setPlayerturn(self, playerturn):
        self.playerturn = playerturn
    def setNumOfPlayers(self, numofplayers):
        self.numofplayers = numofplayers
    def setGameRunning(self, gamerunning):
        self.gamerunning = gamerunning
    def setGameWon(self, gamewon):
        self.gamewon = gamewon