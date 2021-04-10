from State import GameState
from Player import Players
from weapon import Weapons
from weaponsdeck import weapdeck
from roomdeck import roomsdeck
from characterdeck import chardeck
from random import randint
import random
from flask import Flask, jsonify, request, render_template
app = Flask(__name__)
#weapon numbers 7 = rope 8 = lead pipe 9 = knife 10 = wrench 11 = candlestick 12 = revolver 
playerturn = 0
roomzdeck = roomsdeck(["Kitchen", "Conservatory", "Dining Room", "Ballroom", "Study", "Hall", "Lounge", "Library", "Billiard Room"])
characdeck = chardeck(["Miss Scarlet", "Mrs. White", "Mrs. Peacock", "Professor Plum", "Mr.Green", "Colonel Mustard"])
characselectdeck = ["Miss Scarlet", "Mrs. White", "Mrs. Peacock", "Professor Plum", "Mr.Green", "Colonel Mustard"]
weapondeck = weapdeck(["Rope", "Lead Pipe", "Knife", "Wrench", "Candlestick", "Revolver"])
roomcoordinate = {'Study' : [0,0] , 'Hall': [0,2] , 'Lounge': [0,4], 'Library': [2,0], 'Billiard Room': [2,2], 'Dining Room': [2,4], 'Conservatory': [4,0], 'Ballroom':[4,2], 'Kitchen':[4,4]}
knife = Weapons("Knife",[0,4,3] ,9)
rope = Weapons("Rope", [0,0,3], 7)
leadpipe = Weapons("Lead Pipe", [0,2,3], 8)
wrench = Weapons("Wrench", [2,0,3], 10)
candlestick = Weapons("Candlestick", [2,2,3], 11)
revolver = Weapons("Revolver", [2,4,3], 12)
weaponsarray = [knife, rope, leadpipe, wrench, candlestick, revolver]
totaldeck = []
playerarray = []
casefile = []
subturnqueue = []
gamestates = {}
gamestate = GameState(casefile, 0, 0, False, [[[0,0,0,7,0,0],[0],[0,0,0,8,0,0],[0],[0,0,0,9,0,0]],
                                            [[0],[99],[0],[99],[0]],
                                            [[0,0,0,10,0,0],[0],[0,0,0,11,0,0],[0],[0,0,0,12,0,0]],
                                            [[0],[99],[0],[99],[0]],
                                            [[0,0,0,0,0,0],[0],[0,0,0,0,0,0],[0],[0,0,0,0,0,0]]], False, 0)
@app.route('/signup', methods=['POST'])
def adduser():
    #adds playersd 
    if (request.method == 'POST'):
        if (len(playerarray) == 0):
            random.shuffle(roomzdeck)
            casefile.append(roomzdeck[0])
            del roomzdeck[0]
            random.shuffle(characdeck)
            casefile.append(characdeck[0])
            del characdeck[0]
            random.shuffle(weapondeck)
            casefile.append(weapondeck[0])
            del weapondeck[0]
            totaldeck.append(roomzdeck)
            totaldeck.append(characdeck)
            totaldeck.append(weapondeck)
            gamestate.setCasefile(casefile)
        if (len(playerarray) < 4):
            user_json = request.get_json()
            playername = user_json["playername"]
            characterselected = user_json["character"]
            #will have to verify that character had not already been chosen.
            hand = []
            location = []
            if not playerarray:
                for i in range(3):
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
                gamestate.setNumOfPlayers(1) 
            if (len(playerarray) == 2):
                gamestate.setNumOfPlayers(2) 
            if (len(playerarray) == 3):
                gamestate.setNumOfPlayers(3) 
            if (len(playerarray) == 4):
                gamestate.setNumOfPlayers(4) 
                gamestate.setGameRunning(True)
                gamestate.setPlayerturn(1)
            if (len(playerarray) > 4):
                return jsonify({"result":"Maximum number of players"})
            board = gamestate.getGameBoard()
            board[player.getLocation()[0]][player.getLocation()[1]][0] = len(playerarray)
            gamestate.setGameBoard(board)
            return jsonify({"result":"success"})      
        #for the time being we will have a default of 4 players
    else:
        return jsonify({'result': 'Error'})
        #first player in gets the leader control but for now we will just begin the game once for people have joined


@app.route('/getstate', methods=['GET'])
def hello():
    if (len(playerarray) == 0):
        #do the player registration 
        random.shuffle(roomzdeck)
        casefile.append(roomzdeck[0])
        del roomzdeck[0]
        random.shuffle(characdeck)
        casefile.append(characdeck[0])
        del characdeck[0]
        random.shuffle(weapondeck)
        casefile.append(weapondeck[0])
        del weapondeck[0]
        totaldeck.append(roomzdeck)
        totaldeck.append(characdeck)
        totaldeck.append(weapondeck)
        gamestate.setCasefile(casefile)
        user_json = request.get_json()
        for i in range(6)
            playername = "Player" + str(i)
            characterselected = characselectdeck[i]
            hand = []
            location = []
            for i in range(3):
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
                gamestate.setNumOfPlayers(1) 
            if (len(playerarray) == 2):
                gamestate.setNumOfPlayers(2) 
            if (len(playerarray) == 3):
                gamestate.setNumOfPlayers(3) 
            if (len(playerarray) == 4):
                gamestate.setNumOfPlayers(4) 
            if (len(playerarray) == 5):
                gamestate.setNumOfPlayers(5)
            if (len(playerarray) == 6):
                gamestate.setNumOfPlayers(6)
                gamestate.setGameRunning(True)
                gamestate.setPlayerturn(1)
            board = gamestate.getGameBoard()
            board[player.getLocation()[0]][player.getLocation()[1]][0] = len(playerarray)
            gamestate.setGameBoard(board)
            return jsonify({"result":"success"})      
    if (len(playerarray) == 1):
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(), 'Player1': {'name': playerarray[0].getName(), 'character': playerarray[0].getCharacter(), 'location': playerarray[0].getLocation(), 'hand': playerarray[0].getHand()}, 'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(), 'gameboard': gamestate.getGameBoard()})
    if (len(playerarray) == 2):
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(), 'Player1': {'name': playerarray[0].getName(), 'character': playerarray[0].getCharacter(), 'location': playerarray[0].getLocation(), 'hand': playerarray[0].getHand()}, 'Player2': {'name': playerarray[1].getName(), 'character': playerarray[1].getCharacter(), 'location': playerarray[1].getLocation(), 'hand': playerarray[1].getHand()}, 'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(), 'gameboard': gamestate.getGameBoard()})
    if (len(playerarray) == 3):
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(), 'Player1': {'name': playerarray[0].getName(), 'character': playerarray[0].getCharacter(), 'location': playerarray[0].getLocation(), 'hand': playerarray[0].getHand()}, 'Player2': {'name': playerarray[1].getName(), 'character': playerarray[1].getCharacter(), 'location': playerarray[1].getLocation(), 'hand': playerarray[1].getHand()}, 'Player3': {'name': playerarray[2].getName(), 'character': playerarray[2].getCharacter(), 'location': playerarray[2].getLocation(), 'hand': playerarray[2].getHand()}, 'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(), 'gameboard': gamestate.getGameBoard()})
    if (len(playerarray) == 4):
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(), 'Player1': {'name': playerarray[0].getName(), 'character': playerarray[0].getCharacter(), 'location': playerarray[0].getLocation(), 'hand': playerarray[0].getHand()}, 'Player2': {'name': playerarray[1].getName(), 'character': playerarray[1].getCharacter(), 'location': playerarray[1].getLocation(), 'hand': playerarray[1].getHand()}, 'Player3': {'name': playerarray[2].getName(), 'character': playerarray[2].getCharacter(), 'location': playerarray[2].getLocation(), 'hand': playerarray[2].getHand()}, 'Player4': {'name': playerarray[3].getName(), 'character': playerarray[3].getCharacter(), 'location': playerarray[3].getLocation(), 'hand': playerarray[3].getHand()},'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(), 'gameboard': gamestate.getGameBoard()})
    if (len(playerarray) == 6):
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(), 'SessionID': "sessionidwillbehere", 'Player1': {'name': playerarray[0].getName(), 'character': playerarray[0].getCharacter(), 'location': playerarray[0].getLocation(), 'hand': playerarray[0].getHand()}, 'Player2': {'name': playerarray[1].getName(), 'character': playerarray[1].getCharacter(), 'location': playerarray[1].getLocation(), 'hand': playerarray[1].getHand()}, 'Player3': {'name': playerarray[2].getName(), 'character': playerarray[2].getCharacter(), 'location': playerarray[2].getLocation(), 'hand': playerarray[2].getHand()}, 'Player4': {'name': playerarray[3].getName(), 'character': playerarray[3].getCharacter(), 'location': playerarray[3].getLocation(), 'hand': playerarray[3].getHand()}, 'Player5': {'name': playerarray[4].getName(), 'character': playerarray[4].getCharacter(), 'location': playerarray[4].getLocation(), 'hand': playerarray[4].getHand()}, 'Player6': {'name': playerarray[5].getName(), 'character': playerarray[5].getCharacter(), 'location': playerarray[5].getLocation(), 'hand': playerarray[5].getHand()}, 'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(), 'gameboard': gamestate.getGameBoard()})
    return jsonify({'error': 'Not enough players have been registered'})
@app.route('/Movement', methods=['POST'])
def Move():
    if (request.method == 'POST'):
        some_json = request.get_json()
        
        character = some_json["character"]
        sessionkey = some_json["sessionkey"]
        xcoordinate = some_json["x"]
        ycoordinate = some_json["y"]
        locgamestate = gamestates[sessionkey]
        
        if(not isinstance(xcoordinate, int)):
            xcoordinate =  int(xcoordinate)
        ycoordinate = some_json["y"]
        if(not isinstance(ycoordinate, int)):
            ycoordinate =  int(ycoordinate)
        newLocation = [xcoordinate, ycoordinate]
        count = 1 
        for x in playerarray:
            if(x.getCharacter() == character):
                oldLocation = x.getLocation()
                board = locgamestate.getGameBoard()
                board[oldLocation[0]][oldLocation[1]][0] = 0
                board[newLocation[0]][newLocation[1]][0] = count              
                x.setLocation(newLocation) 
                locgamestate.setGameBoard(board)
            count+=1
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'Error'})
@app.route('/suggdisprove', methods=['GET'])
def suggdisprove():
    if(request.method == 'GET')
@app.route('/Suggestion', methods=['POST'])
def Suggest():
    if (request.method == 'POST'):
        some_json = request.get_json()
        weapon = some_json["weapon"]
        room = some_json["room"]
        character = some_json["character"]
        playercharacter = some_json["playerchar"]
        sessionkey = some_json["sessionkey"]
        xcoordinate = some_json["x"]
        ycoordinate = some_json["y"]
        locgamestate = gamestates[sessionkey]
        if(not isinstance(xcoordinate, int)):
            xcoordinate =  int(xcoordinate)
        if(not isinstance(ycoordinate, int)):
            ycoordinate =  int(ycoordinate)
            
        newLocation = [xcoordinate, ycoordinate]
        weaponloc = []
        weaponnum = 0
        for x in weaponsarray:
            if(x.getName() == weapon):
                weaponloc = x.getLocation()
                weaponnum = x.getWeapon()
        count = 1 
        for x in playerarray:
            if(x.getCharacter() == character):
                oldLocation = x.getLocation()
                board = locgamestate.getGameBoard()
                board[oldLocation[0]][oldLocation[1]][0] = 0
                board[weaponloc[0]][weaponloc[1]][weaponloc[2]] = 0
                board[newLocation[0]][newLocation[1]][0] = count
                board[newLocation[0]][newLocation[1]][3] = weaponnum
                x.setLocation(newLocation)
                for x in weaponsarray:
                    if(x.getName() == weapon):
                        x.setLocation([newLocation[0], newLocation[1], 3])
                locgamestate.setGameBoard(board)
                message = "{0} suggest that the murder was committed by {1} in the {2} with a {3}".format(
                    playercharacter, 
                    character,
                    room,
                    weapon)
            count+=1
        counter = 1 
        for x in playerarray:
            if(x.getCharacter() == character):
                locgamestate.setSubturn(counter)
            count+=1
        return jsonify(result='success', message=message)
    else:
        return jsonify(result='error')

@app.route('/Accusation', methods=['POST'])
def Accuse():
    #needs to finish cleaning this out
    if (request.method == 'POST'):
        some_json = request.get_json()
        weapon = some_json["weapon"]
        suspect = some_json["suspect"]
        character = some_json["character"]
        sessionkey = some_json["sessionkey"]
        room = some_json["room"]
        xcoordinate = some_json["x"]
        locgamestate = gamestates[sessionkey]
        if(not isinstance(xcoordinate, int)):
            xcoordinate =  int(xcoordinate)
        ycoordinate = some_json["y"]
        if(not isinstance(ycoordinate, int)):
            ycoordinate =  int(ycoordinate)
        newLocation = [xcoordinate, ycoordinate]
        count = 1 
        for x in playerarray:
            if(x.getCharacter() == character):
                oldLocation = x.getLocation()
                board = locgamestate.getGameBoard()
                board[oldLocation[0]][oldLocation[1]][0] = 0
                board[newLocation[0]][newLocation[1]][0] = count
                x.setLocation(newLocation)
                message = "{0} has made the accusation that the murder was committed by {1} in the {2} with a {3}".format(
                    x.getCharacter(), 
                    suspect,
                    newLocation,
                    weapon)
            count+=1
        return jsonify(result='success', message=message)
    else:
        return jsonify(result= 'error')

@app.route('/Endturn', methods=['POST'])
def EndTurn():
    if(request.method == 'POST'):
        some_json = request.get_json()
        planernum = some_json["playernum"]
        sessionkey = some_json["sessionkey"]
        locgamestate = gamestates[sessionkey]
        #will need to add validation for the playernum 
        if(gamestate.getPlayerturn() == 4):
            gamestate.setPlayerturn = 1
        else:
            gamestate.setPlayerturn(gamestate.getPlayerturn + 1)

@app.route('/Subturn', methods=['POST'])
def SubTurn():
    if(request.method == 'POST'):
        some_json = request.get_json()
        #needed for validation later
        sessionkey = some_json["sessionkey"]
        locgamestate = gamestates[sessionkey]
        character = some_json["character"]
        card = some_json["card"]
        subturnqueue.append(card)

@app.route('/SubTurnRequest', methods=['GET'])
def SubTurnReq():
    sessionkey = some_json["sessionkey"]
    locgamestate = gamestates[sessionkey]
    card = subturnqueue[0]
    del subturnqueue[0]
    gamestate.setSubturn(0)
    return jsonify({'card': card})
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

