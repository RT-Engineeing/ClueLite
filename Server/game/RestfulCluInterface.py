from State import GameState
from Player import Players
from weaponsdeck import weapdeck
from roomdeck import roomsdeck
from characterdeck import chardeck
from random import randint
import random
from flask import Flask, jsonify, request
app = Flask(__name__)

playerturn = 0
roomzdeck = roomsdeck(["Kitchen", "Conservatory", "Dining Room", "Ballroom", "Study Hall", "Lounge", "Library", "Billiard Room"])
characdeck = chardeck(["Miss Scarlet", "Mrs. White", "Mrs. Peacock", "Professor Plum", "Mr.Green", "Colonel Mustard"])
characselectdeck = ["Miss Scarlet", "Mrs. White", "Mrs. Peacock", "Professor Plum", "Mr.Green", "Colonel Mustard"]
weapondeck = weapdeck(["Rope", "Lead Pipe", "Knife", "Wrench", "Candlestick", "Revolver"])
totaldeck = ["Miss Scarlet", "Mrs. White", "Mrs. Peacock", "Professor Plum", "Mr.Green", "Colonel Mustard", "Rope", "Lead Pipe", "Knife", "Wrench", "Candlestick", "Revolver", "Kitchen", "Conservatory", "Dining Room", "Ballroom", "Study Hall", "Lounge", "Library", "Billiard Room"]
playerarray = []
gamestate = GameState(0, 0, False, [[0,0,0,0,0],[0,99,0,99,0],[0,0,0,0,0],[0,99,0,99,0],[0,0,0,0,0]], False)
@app.route('/signup', methods=['POST'])
def adduser():
    #adds playersd 
    if (request.method == 'POST'):
        if (len(playerarray) < 4):
            user_json = request.get_json()
            playername = user_json["playername"]
            characterselected = user_json["character"]
            #will have to verify that character had not already been chosen.
            hand = []
            location = []
            if not playerarray:
                for i in range(6):
                    random.shuffle(totaldeck)
                    hand.append(totaldeck[0])
                    del totaldeck[0]
            else:
                for i in range(4):
                    random.shuffle(totaldeck)
                    hand.append(totaldeck[0])
                    del totaldeck[0]    
            if(characterselected == "Miss Scarlet"):
                location = [0,3]   
            if(characterselected == "Mrs. White"):
                location = [4,3]
            if(characterselected == "Mrs. Peacock"):
                location = [3,0]
            if(characterselected == "Professor Plum"):
                location = [1,0]
            if(characterselected == "Mr.Green"):
                location = [4,1]
            if(characterselected == "Colonel Mustard"):
                location = [1,4]
            player = Players(playername, characterselected, hand, location)
            playerarray.append(player)
            if (len(playerarray) == 1):
                gamestate.numofplayers = 1
            if (len(playerarray) == 2):
                gamestate.numofplayers = 2
            if (len(playerarray) == 3):
                gamestate.numofplayers = 3
            if (len(playerarray) == 4):
                gamestate.numofplayers = 4
            if (len(playerarray) > 4):
                return jsonify({"result":"Maximum number of players"})
            board = gamestate.getGameBoard()
            board[player.getLocation()[0]][player.getLocation()[1]] = len(playerarray)
            gamestate.setGameBoard(board)
            return jsonify({"result":"success"})      
        #for the time being we will have a default of 4 players
    else:
        return jsonify({'result': 'Error'})
        #first player in gets the leader control but for now we will just begin the game once for people have joined


@app.route('/getstate', methods=['GET'])
def hello():
    if (len(playerarray) == 1):
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(), 'Player1': {'name': playerarray[0].getName(), 'character': playerarray[0].getCharacter(), 'location': playerarray[0].getLocation(), 'hand': playerarray[0].getHand()}, 'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(), 'gameboard': gamestate.getGameBoard()})
    if (len(playerarray) == 2):
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(), 'Player1': {'name': playerarray[0].getName(), 'character': playerarray[0].getCharacter(), 'location': playerarray[0].getLocation(), 'hand': playerarray[0].getHand()}, 'Player2': {'name': playerarray[1].getName(), 'character': playerarray[1].getCharacter(), 'location': playerarray[1].getLocation(), 'hand': playerarray[1].getHand()}, 'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(), 'gameboard': gamestate.getGameBoard()})
    if (len(playerarray) == 3):
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(), 'Player1': {'name': playerarray[0].getName(), 'character': playerarray[0].getCharacter(), 'location': playerarray[0].getLocation(), 'hand': playerarray[0].getHand()}, 'Player2': {'name': playerarray[1].getName(), 'character': playerarray[1].getCharacter(), 'location': playerarray[1].getLocation(), 'hand': playerarray[1].getHand()}, 'Player3': {'name': playerarray[2].getName(), 'character': playerarray[2].getCharacter(), 'location': playerarray[2].getLocation(), 'hand': playerarray[2].getHand()}, 'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(), 'gameboard': gamestate.getGameBoard()})
    if (len(playerarray) == 4):
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(), 'Player1': {'name': playerarray[0].getName(), 'character': playerarray[0].getCharacter(), 'location': playerarray[0].getLocation(), 'hand': playerarray[0].getHand()}, 'Player2': {'name': playerarray[1].getName(), 'character': playerarray[1].getCharacter(), 'location': playerarray[1].getLocation(), 'hand': playerarray[1].getHand()}, 'Player3': {'name': playerarray[2].getName(), 'character': playerarray[2].getCharacter(), 'location': playerarray[2].getLocation(), 'hand': playerarray[2].getHand()}, 'Player4': {'name': playerarray[3].getName(), 'character': playerarray[3].getCharacter(), 'location': playerarray[3].getLocation(), 'hand': playerarray[3].getHand()},'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(), 'gameboard': gamestate.getGameBoard()})

@app.route('/Movement', methods=['POST'])
def Move():
    if (request.method == 'POST'):
        some_json = request.get_json()
        return jsonify({'you sent': some_json})
    else:
        return jsonify({'result': 'Error'})

@app.route('/Suggestion', methods=['POST'])
def Suggest():
    if (request.method == 'POST'):
        some_json = request.get_json()
        return jsonify({'you sent': some_json})
    else:
        return jsonify({'result': 'Error'})

@app.route('/Accusation', methods=['POST'])
def Accuse():
    if (request.method == 'POST'):
        some_json = request.get_json()
        return jsonify({'you sent': some_json})
    else:
        return jsonify({'result': 'Error'})

if __name__ == "__main__":
    app.run(debug=True)