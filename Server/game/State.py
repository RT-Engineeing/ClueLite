class GameState: 
    def __init__(self, numofplayers, player1, player2, player3, player4, player5, player6, playerturn, gamewon, gameboard):
        self.numofplayers = numofplayers
        self.player1 = player1
        self.player2 = player2
        self.player3 = player3
        self.player4 = player4
        self.player5 = player5
        self.player6 = player6
        self.playerturn = playerturn
        self.gamewon = gamewon
        self.gameboard = gameboard 

    def getNumOfPlayers(self):
        return self.numofplayers
    def getPlayer1(self):
        return self.player1
    def getPlayer2(self):
        return self.player2
    def getPlayer3(self):
        return self.player3
    def getPlayer4(self):
        return self.player4
    def getPlayer5(self):
        return self.player5
    def getPlayer6(self):
        return self.player6
    def getPlayerturn(self):
        return self.playerturn
    def getGameWon(self):
        return self.gamewon
    def getGameBoard(self):
        return self.gameboard
    def setNumOfPlayers(self, numofplayers):
        self.numofplayers = numofplayers
    def setPlayer1(self, player1):
        self.player1 = player1
    def setPlayer2(self, player2):
        self.player2 = player2
    def setPlayer3(self, player3):
        self.player3 = player3
    def setPlayer4(self, player4):
        self.player4 = player4
    def setPlayer5(self, player5):
        self.player5 = player5
    def setPlayer6(self, player6):
        self.player6 = player6