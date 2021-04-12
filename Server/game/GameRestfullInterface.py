from _ast import Global
from Session import Session
from GameState import GameState
from GameOperations import Players, Weapons, Weapdeck, Roomsdeck, Chardeck
from random import randint
from flask import Flask, jsonify, request, render_template
import random
import itertools
import os

app = Flask(__name__)
rooms = [
    "Kitchen",
    "Conservatory",
    "Dining Room",
    "Ballroom",
    "Study",
    "Hall",
    "Lounge",
    "Library",
    "Billiard Room"
]
characters = [
    "Miss Scarlet",
    "Mrs. White",
    "Mrs. Peacock",
    "Professor Plum",
    "Mr.Green",
    "Colonel Mustard"
]
charactersind = [
    "Miss Scarlet",
    "Mrs. White",
    "Mrs. Peacock",
    "Professor Plum",
    "Mr.Green",
    "Colonel Mustard"
]
weapons = [
    "Rope",  # 7
    "Lead Pipe",  # 8
    "Knife",  # 9
    "Wrench",  # 10
    "Candlestick",  # 11
    "Revolver"  # 12
]

playerturn = 0
roomzdeck = Roomsdeck(rooms)
characdeck = Chardeck(characters)
weapondeck = Weapdeck(weapons)
rope = Weapons(weapons[0], [0, 0], 7)
leadpipe = Weapons(weapons[1], [0, 2], 8)
knife = Weapons(weapons[2], [0, 4], 9)
wrench = Weapons(weapons[3], [2, 0], 10)
candlestick = Weapons(weapons[4], [2, 2], 11)
revolver = Weapons(weapons[5], [2, 4], 12)
weaponsarray = [knife, rope, leadpipe, wrench, candlestick, revolver]
totaldeck = []
playerarray = []
selectedChars = []
casefile = []
subturnqueue = []
characselectdeck = []
suggestionmessage =[]
gamestate = GameState(casefile, 0, 0, False, [[["Rope"], [], ["Lead Pipe"], [], ["Knife"]],
                                              [[], [], [], [], []],
                                              [["Wrench"], [], ["Candlestick"], [], ["Revolver"]],
                                              [[], [], [], [], []],
                                              [[], [], [], [], []]],
                      False, 0)
maxSessionPlayer = 0
isPlayerReady = False
tempvar = 0
session = Session(random.randint(100000, 999999), gamestate)

def adduser():
    if len(playerarray) == 0:
        random.shuffle(rooms)
        casefile.append(rooms[0])
        del rooms[0]
        random.shuffle(characters)
        casefile.append(characters[0])
        del characters[0]
        random.shuffle(weapons)
        casefile.append(weapons[0])
        del weapons[0]
        global totaldeck
        totaldeck.extend(rooms)
        totaldeck.extend(weapons)
        totaldeck.extend(characters)
        newgamestate = gamestate
        newgamestate.setCasefile(casefile)
        playername = "Player" + str(len(playerarray) + 1)
        character = charactersind[len(playerarray)]
        characselectdeck.append(character)
        hand = []
        location = []
        for i in range(3):
            random.shuffle(totaldeck)
            hand.append(totaldeck[0])
            del totaldeck[0]
        if character == 'Miss Scarlet':
            location = [0, 3]
        elif character == 'Mrs. White':
            location = [4, 3]
        elif character == 'Mrs. Peacock':
            location = [3, 0]
        elif character == 'Professor Plum':
            location = [1, 0]
        elif character == 'Mr.Green':
            location = [4, 1]
        elif character == 'Colonel Mustard':
            location = [1, 4]
        player = Players(playername, character, hand, location)
        playerarray.append(player)
        p = len(playerarray)
        if 1 >= p <= 5:
            newgamestate.setNumOfPlayers(p)
        elif p == 6:
            newgamestate.setNumOfPlayers(p)
            newgamestate.setGameRunning(True)
            newgamestate.setPlayerturn(1)
        board = newgamestate.getGameBoard()
        arr = board[player.getLocation()[0]][player.getLocation()[1]]
        arr.append(player.getCharacter())
        board[player.getLocation()[0]][player.getLocation()[1]] = arr
        newgamestate.setGameBoard(board)
        session.setGameState(newgamestate)
        session.setPlayernum(len(playerarray))
        sessionstring = jsonify(
            sessionkey=str(session.getUid()),
            playername=playername,
            totalPlayers=session.getPlayernum(),
            yourcharacter=player.getCharacter(),
            result=playername + "has been added to the session.",
        )
        return sessionstring
    else:
        newgamestate = session.getGameState()
        playername = "Player" + str(session.getPlayernum() + 1)
        character = charactersind[session.getPlayernum()]
        characselectdeck.append(character)
        hand = []
        location = []
        for i in range(3):
            random.shuffle(totaldeck)
            hand.append(totaldeck[0])
            del totaldeck[0]
        if character == 'Miss Scarlet':
            location = [0, 3]
        elif character == 'Mrs. White':
            location = [4, 3]
        elif character == 'Mrs. Peacock':
            location = [3, 0]
        elif character == 'Professor Plum':
            location = [1, 0]
        elif character == 'Mr.Green':
            location = [4, 1]
        elif character == 'Colonel Mustard':
            location = [1, 4]
        player = Players(playername, character, hand, location)
        playerarray.append(player)
        p = len(playerarray)
        if 1 <= p <= 5:
            newgamestate.setNumOfPlayers(p)
        elif p == 6:
            newgamestate.setNumOfPlayers(p)
            #newgamestate.setGameRunning(True)
            #newgamestate.setPlayerturn(1)
        board = newgamestate.getGameBoard()
        arr = board[player.getLocation()[0]][player.getLocation()[1]]
        arr.append(player.getCharacter())
        board[player.getLocation()[0]][player.getLocation()[1]] = arr
        newgamestate.setGameBoard(board)
        session.setGameState(newgamestate)
        session.setPlayernum(len(playerarray))
        #session.addPlayer(player)
        sessionstring = jsonify(
            sessionId=str(session.getUid()),
            playername=playername,
            totalPlayers=session.getPlayernum(),
            yourcharacter=player.getCharacter(),
            result=playername + "has been added to the session.",
        )
        return sessionstring


@app.route('/ready', methods=['POST', 'GET'])
def playersready():
    if request.method == 'POST':
        some_json = request.get_json()
        playername = some_json["playername"]
        uid = some_json["lobbyid"]
        playerready = some_json["playerready"]
        if playerready == "True":
            isReady = True
            session.addPlayer(playername)
            return session.setReady(uid, playername, isReady)
        isReady = False
        return session.setReady(uid, playername, isReady)
    if request.method == 'GET':
        if len(session.getReady()) == 6:
            return jsonify(status='true',
                           playersready=session.getReady())
        else:
            return jsonify(status='false',
                           playersready=session.getReady())

@app.route('/session')
def sessions():
    return adduser()


@app.route('/getstate', methods=['GET'])
def hello():
    if (len(playerarray) == 1):
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                        'Player1': {'name': playerarray[0].getName(), 'character': playerarray[0].getCharacter(),
                                    'location': playerarray[0].getLocation(), 'hand': playerarray[0].getHand()},
                        'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(), 'gamerunning': gamestate.getGameRunning(),
                        'gameboard': gamestate.getGameBoard()})
    if (len(playerarray) == 2):
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                        'Player1': {'name': playerarray[0].getName(), 'character': playerarray[0].getCharacter(),
                                    'location': playerarray[0].getLocation(), 'hand': playerarray[0].getHand()},
                        'Player2': {'name': playerarray[1].getName(), 'character': playerarray[1].getCharacter(),
                                    'location': playerarray[1].getLocation(), 'hand': playerarray[1].getHand()},
                        'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(), 'gamerunning': gamestate.getGameRunning(),
                        'gameboard': gamestate.getGameBoard()})
    if (len(playerarray) == 3):
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                        'Player1': {'name': playerarray[0].getName(), 'character': playerarray[0].getCharacter(),
                                    'location': playerarray[0].getLocation(), 'hand': playerarray[0].getHand()},
                        'Player2': {'name': playerarray[1].getName(), 'character': playerarray[1].getCharacter(),
                                    'location': playerarray[1].getLocation(), 'hand': playerarray[1].getHand()},
                        'Player3': {'name': playerarray[2].getName(), 'character': playerarray[2].getCharacter(),
                                    'location': playerarray[2].getLocation(), 'hand': playerarray[2].getHand()},
                        'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(), 'gamerunning': gamestate.getGameRunning(),
                        'gameboard': gamestate.getGameBoard()})
    if (len(playerarray) == 4):
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                        'Player1': {'name': playerarray[0].getName(), 'character': playerarray[0].getCharacter(),
                                    'location': playerarray[0].getLocation(), 'hand': playerarray[0].getHand()},
                        'Player2': {'name': playerarray[1].getName(), 'character': playerarray[1].getCharacter(),
                                    'location': playerarray[1].getLocation(), 'hand': playerarray[1].getHand()},
                        'Player3': {'name': playerarray[2].getName(), 'character': playerarray[2].getCharacter(),
                                    'location': playerarray[2].getLocation(), 'hand': playerarray[2].getHand()},
                        'Player4': {'name': playerarray[3].getName(), 'character': playerarray[3].getCharacter(),
                                    'location': playerarray[3].getLocation(), 'hand': playerarray[3].getHand()},
                        'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(), 'gamerunning': gamestate.getGameRunning(),
                        'gameboard': gamestate.getGameBoard()})
    if (len(playerarray) == 5):
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                        'Player1': {'name': playerarray[0].getName(), 'character': playerarray[0].getCharacter(),
                                    'location': playerarray[0].getLocation(), 'hand': playerarray[0].getHand()},
                        'Player2': {'name': playerarray[1].getName(), 'character': playerarray[1].getCharacter(),
                                    'location': playerarray[1].getLocation(), 'hand': playerarray[1].getHand()},
                        'Player3': {'name': playerarray[2].getName(), 'character': playerarray[2].getCharacter(),
                                    'location': playerarray[2].getLocation(), 'hand': playerarray[2].getHand()},
                        'Player4': {'name': playerarray[3].getName(), 'character': playerarray[3].getCharacter(),
                                    'location': playerarray[3].getLocation(), 'hand': playerarray[3].getHand()},
                        'Player5': {'name': playerarray[4].getName(), 'character': playerarray[4].getCharacter(),
                                    'location': playerarray[4].getLocation(), 'hand': playerarray[4].getHand()},
                        'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(), 'gamerunning': gamestate.getGameRunning(),
                        'gameboard': gamestate.getGameBoard()})
    if (len(playerarray) == 6):
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                        'Player1': {'name': playerarray[0].getName(), 'character': playerarray[0].getCharacter(),
                                    'location': playerarray[0].getLocation(), 'hand': playerarray[0].getHand()},
                        'Player2': {'name': playerarray[1].getName(), 'character': playerarray[1].getCharacter(),
                                    'location': playerarray[1].getLocation(), 'hand': playerarray[1].getHand()},
                        'Player3': {'name': playerarray[2].getName(), 'character': playerarray[2].getCharacter(),
                                    'location': playerarray[2].getLocation(), 'hand': playerarray[2].getHand()},
                        'Player4': {'name': playerarray[3].getName(), 'character': playerarray[3].getCharacter(),
                                    'location': playerarray[3].getLocation(), 'hand': playerarray[3].getHand()},
                        'Player5': {'name': playerarray[4].getName(), 'character': playerarray[4].getCharacter(),
                                    'location': playerarray[4].getLocation(), 'hand': playerarray[4].getHand()},
                        'Player6': {'name': playerarray[5].getName(), 'character': playerarray[5].getCharacter(),
                                    'location': playerarray[5].getLocation(), 'hand': playerarray[5].getHand()},
                        'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(), 'gamerunning': gamestate.getGameRunning(),
                        'gameboard': gamestate.getGameBoard()})
    return jsonify({'error': 'error'})


@app.route('/Movement', methods=['POST'])
def Move():
    if (request.method == 'POST'):
        some_json = request.get_json()

        character = some_json["character"]
        xcoordinate = some_json["x"]
        ycoordinate = some_json["y"]

        if (not isinstance(xcoordinate, int)):
            xcoordinate = int(xcoordinate)
        ycoordinate = some_json["y"]
        if (not isinstance(ycoordinate, int)):
            ycoordinate = int(ycoordinate)
        newLocation = [xcoordinate, ycoordinate]
        count = 1
        for x in playerarray:
            if (x.getCharacter() == character):
                oldLocation = x.getLocation()
                board = gamestate.getGameBoard()
                arr = board[oldLocation[0]][oldLocation[1]]
                arr2 = board[newLocation[0]][newLocation[1]]
                for character in range(len(arr)):
                    if arr[character] == x.getCharacter():
                        arr.pop(character)
                arr2.append(x.getCharacter())
                board[oldLocation[0]][oldLocation[1]] = arr
                board[newLocation[0]][newLocation[1]] = arr2
                x.setLocation(newLocation)
                gamestate.setGameBoard(board)
            count += 1
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'Error'})


@app.route('/Suggestion', methods=['POST'])
def Suggest():
    if (request.method == 'POST'):
        some_json = request.get_json()
        weapon = some_json["weapon"]
        room = some_json["room"]
        character = some_json["character"]
        playercharacter = some_json["playerchar"]
        xcoordinate = some_json["x"]
        ycoordinate = some_json["y"]

        if (not isinstance(xcoordinate, int)):
            xcoordinate = int(xcoordinate)
        ycoordinate = some_json["y"]
        if (not isinstance(ycoordinate, int)):
            ycoordinate = int(ycoordinate)

        newLocation = [xcoordinate, ycoordinate]
        weaponloc = []
        weaponname = ""
        for x in weaponsarray:
            if (x.getName() == weapon):
                weaponloc = x.getLocation()
                weaponname = x.getName()
        count = 1
        for x in playerarray:
            if (x.getCharacter() == character):
                oldLocation = x.getLocation()
                board = gamestate.getGameBoard()
                arr = board[oldLocation[0]][oldLocation[1]]
                for character in range(len(arr)):
                    if arr[character] == x.getCharacter():
                        arr.pop(character)
                board[oldLocation[0]][oldLocation[1]] = arr
                arr2 = board[weaponloc[0]][weaponloc[1]]
                for weapon in range(len(arr2)):
                    if arr2[weapon] == weaponname:
                        arr2.pop(weapon)
                board[weaponloc[0]][weaponloc[1]] = arr2
                arr3 = board[newLocation[0]][newLocation[1]]
                arr3.append(weapon)
                arr3.append(character)
                board[newLocation[0]][newLocation[1]] = arr3
                x.setLocation(newLocation)
                for x in weaponsarray:
                    if (x.getName() == weapon):
                        x.setLocation([newLocation[0], newLocation[1]])
                gamestate.setGameBoard(board)
                message = "{0} suggest that the murder was committed by {1} in the {2} with a {3}".format(
                    playercharacter,
                    character,
                    room,
                    weapon)
                suggestionmessage.append(message)
            count += 1
        counter = 1
        for x in playerarray:
            if (x.getCharacter() == character):
                gamestate.setSubturn(counter)
            count += 1

        return jsonify(result='success', message=message)
    else:
        return jsonify(result='error')


@app.route('/Accusation', methods=['POST'])
def Accuse():
    # needs to finish cleaning this out
    if (request.method == 'POST'):
        some_json = request.get_json()
        weapon = some_json["weapon"]
        suspect = some_json["suspect"]
        character = some_json["character"]
        room = some_json["room"]
        xcoordinate = some_json["x"]
        if (not isinstance(xcoordinate, int)):
            xcoordinate = int(xcoordinate)
        ycoordinate = some_json["y"]
        if (not isinstance(ycoordinate, int)):
            ycoordinate = int(ycoordinate)
        newLocation = [xcoordinate, ycoordinate]
        count = 1
        for x in playerarray:
            if (x.getCharacter() == character):
                oldLocation = x.getLocation()
                board = gamestate.getGameBoard()
                board[oldLocation[0]][oldLocation[1]][0] = 0
                board[newLocation[0]][newLocation[1]][0] = count
                x.setLocation(newLocation)
                message = "{0} has made the accusation that the murder was committed by {1} in the {2} with a {3}".format(
                    x.getCharacter(),
                    suspect,
                    newLocation,
                    weapon)
            count += 1
        return jsonify(result='success', message=message)
    else:
        return jsonify(result='error')


@app.route('/Endturn', methods=['POST'])
def EndTurn():
    if (request.method == 'POST'):
        some_json = request.get_json()
        playernum = some_json["playernum"]
        # will need to add validation for the playernum
        if (gamestate.getPlayerturn() == 6):
            gamestate.setPlayerturn = 1
        else:
            gamestate.setPlayerturn(gamestate.getPlayerturn + 1)


@app.route('/Subturn', methods=['POST'])
def SubTurn():
    if (request.method == 'POST'):
        some_json = request.get_json()
        # needed for validation later
        character = some_json["character"]
        card = some_json["card"]
        subturnqueue.append(card)


@app.route('/SubTurnRequest', methods=['GET'])
def SubTurnReq():
    card = subturnqueue[0]
    del subturnqueue[0]
    gamestate.setSubturn(0)
    return jsonify({'card': card})


@app.route('/')
def index():
    return f"Welcome to ClueLite.\n Click Play to start the game."


if __name__ == "__main__":
    app.run(debug=True)
