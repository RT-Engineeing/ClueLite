from Session import Session
from GameState import GameState
from GameOperations import Players, Weapons, Weapdeck, Roomsdeck, Chardeck
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import random
import json
import Cards
import copy
app = Flask(__name__)
rooms = copy.deepcopy(Cards.ROOMS)
suggrooms = copy.deepcopy(Cards.ROOMS)
characters = copy.deepcopy(Cards.CHARACTERS)
charactersind = copy.deepcopy(Cards.CHARACTERS)
weapons = copy.deepcopy(Cards.WEAPONS)

roomcoordinates = [
    [4, 4],
    [4, 0],
    [2, 4],
    [4, 2],
    [0, 0],
    [0, 2],
    [0, 4],
    [2, 0],
    [2, 2]
]
uids = []

playerturn = 1
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
messagequeue = [[], [], [], [], [], []]
totaldeck = []
playerarray = []
selectedChars = []
casefile = []
subturnqueue = []
characselectdeck = []
suggestionmessage = []
gamestate = GameState(casefile, 0, 1, False, [[["Rope"], [], ["Lead Pipe"], [], ["Knife"]],
                                              [[], [], [], [], []],
                                              [["Wrench"], [], ["Candlestick"],
                                                  [], ["Revolver"]],
                                              [[], [], [], [], []],
                                              [[], [], [], [], []]],
                      False, 0)
maxSessionPlayer = 0
isPlayerReady = False
tempvar = 0
session = Session(random.randint(100000, 999999), gamestate)

CORS(app)


def adduser(uid):
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
        print("case file:  " + str(casefile))
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
        print("setting hand for " + character + ": " + str(hand))
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
            sessionId=str(session.getSessionid()),
            playername=playername,
            totalPlayers=session.getPlayernum(),
            yourcharacter=player.getCharacter(),
            result=playername + " has been added to the session.",
        )
        uids.append(uid)
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
            # newgamestate.setGameRunning(True)
            newgamestate.setPlayerturn(1)
        board = newgamestate.getGameBoard()
        arr = board[player.getLocation()[0]][player.getLocation()[1]]
        arr.append(player.getCharacter())
        board[player.getLocation()[0]][player.getLocation()[1]] = arr
        newgamestate.setGameBoard(board)
        session.setGameState(newgamestate)
        session.setPlayernum(len(playerarray))
        # session.addPlayer(player)
        sessionstring = jsonify(
            sessionId=str(session.getSessionid()),
            playername=playername,
            totalPlayers=session.getPlayernum(),
            yourcharacter=player.getCharacter(),
            result=playername + " has been added to the session.",
        )
        uids.append(uid)
        return sessionstring


@app.route('/ready', methods=['POST', 'GET'])
def playersready():
    if request.method == 'POST':
        some_json = request.get_json()
        playername = some_json["playername"]
        sessionId = some_json["sessionId"]
        playerready = some_json["playerready"]
        if playerready == "True":
            isReady = True
            session.addPlayer(playername)
            if session.getPlayernum() == 6:
                gamestate.setGameRunning(True)
            return session.setReady(sessionId, playername, isReady)
        else:
            session.removePlayer(playername)
            isReady = False
            return session.setReady(sessionId, playername, isReady)
    elif request.method == 'GET':
        lobbyPlayers = []
        for p in playerarray:
            lobbyPlayers.append(p.getName())
        if len(session.getReady()) == 6:
            return jsonify(status='true',
                           playersready=session.getReady(),
                           lobbyPlayers=lobbyPlayers
                           )
        else:
            return jsonify(status='false',
                           playersready=session.getReady(),
                           lobbyPlayers=lobbyPlayers
                           )
    else:
        return jsonify(
            result="error",
            message="The {0} }method is not supported.".format(
                str(request.method))
        )


@app.route('/session', methods=['POST'])
def sessions():
    some_json = request.get_json()
    uid = some_json["uid"]
    return adduser(uid)


@app.route('/getstate', methods=['POST'])
def hello():
    some_json = request.get_json()
    uid = some_json["uid"]
    messages = []
    count = 0
    for x in uids:
        if x == uid:
            messages = messagequeue[count]
        count += 1
    if len(playerarray) == 1:
        if gamestate.getGameWon():
            return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                            'Player1': {'name': playerarray[0].getName(), 'character': playerarray[0].getCharacter(),
                                        'location': playerarray[0].getLocation(), 'hand': playerarray[0].getHand()},
                            'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(),
                            'gamerunning': gamestate.getGameRunning(), 'messages': messages,
                            'subturn': gamestate.getSubturn(),
                            'gameboard': gamestate.getGameBoard(), 'casefile': gamestate.getCasefile()})
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                        'Player1': {'name': playerarray[0].getName(), 'character': playerarray[0].getCharacter(),
                                    'location': playerarray[0].getLocation(), 'hand': playerarray[0].getHand()},
                        'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(),
                        'gamerunning': gamestate.getGameRunning(), 'messages': messages,
                        'subturn': gamestate.getSubturn(),
                        'gameboard': gamestate.getGameBoard()})
    if len(playerarray) == 2:
        if gamestate.getGameWon():
            return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                            'Player1': {'name': playerarray[0].getName(), 'character': playerarray[0].getCharacter(),
                                        'location': playerarray[0].getLocation(), 'hand': playerarray[0].getHand()},
                            'Player2': {'name': playerarray[1].getName(), 'character': playerarray[1].getCharacter(),
                                        'location': playerarray[1].getLocation(), 'hand': playerarray[1].getHand()},
                            'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(),
                            'gamerunning': gamestate.getGameRunning(), 'messages': messages,
                            'subturn': gamestate.getSubturn(),
                            'gameboard': gamestate.getGameBoard(), 'casefile': gamestate.getCasefile()})
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                        'Player1': {'name': playerarray[0].getName(), 'character': playerarray[0].getCharacter(),
                                    'location': playerarray[0].getLocation(), 'hand': playerarray[0].getHand()},
                        'Player2': {'name': playerarray[1].getName(), 'character': playerarray[1].getCharacter(),
                                    'location': playerarray[1].getLocation(), 'hand': playerarray[1].getHand()},
                        'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(),
                        'gamerunning': gamestate.getGameRunning(), 'messages': messages,
                        'subturn': gamestate.getSubturn(),
                        'gameboard': gamestate.getGameBoard()})
    if len(playerarray) == 3:
        if gamestate.getGameWon():
            return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                            'Player1': {'name': playerarray[0].getName(), 'character': playerarray[0].getCharacter(),
                                        'location': playerarray[0].getLocation(), 'hand': playerarray[0].getHand()},
                            'Player2': {'name': playerarray[1].getName(), 'character': playerarray[1].getCharacter(),
                                        'location': playerarray[1].getLocation(), 'hand': playerarray[1].getHand()},
                            'Player3': {'name': playerarray[2].getName(), 'character': playerarray[2].getCharacter(),
                                        'location': playerarray[2].getLocation(), 'hand': playerarray[2].getHand()},
                            'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(),
                            'gamerunning': gamestate.getGameRunning(), 'messages': messages,
                            'subturn': gamestate.getSubturn(),
                            'gameboard': gamestate.getGameBoard(), 'casefile': gamestate.getCasefile()})
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                        'Player1': {'name': playerarray[0].getName(), 'character': playerarray[0].getCharacter(),
                                    'location': playerarray[0].getLocation(), 'hand': playerarray[0].getHand()},
                        'Player2': {'name': playerarray[1].getName(), 'character': playerarray[1].getCharacter(),
                                    'location': playerarray[1].getLocation(), 'hand': playerarray[1].getHand()},
                        'Player3': {'name': playerarray[2].getName(), 'character': playerarray[2].getCharacter(),
                                    'location': playerarray[2].getLocation(), 'hand': playerarray[2].getHand()},
                        'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(),
                        'gamerunning': gamestate.getGameRunning(), 'messages': messages,
                        'subturn': gamestate.getSubturn(),
                        'gameboard': gamestate.getGameBoard()})
    if len(playerarray) == 4:
        if gamestate.getGameWon():
            return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                            'Player1': {'name': playerarray[0].getName(), 'character': playerarray[0].getCharacter(),
                                        'location': playerarray[0].getLocation(), 'hand': playerarray[0].getHand()},
                            'Player2': {'name': playerarray[1].getName(), 'character': playerarray[1].getCharacter(),
                                        'location': playerarray[1].getLocation(), 'hand': playerarray[1].getHand()},
                            'Player3': {'name': playerarray[2].getName(), 'character': playerarray[2].getCharacter(),
                                        'location': playerarray[2].getLocation(), 'hand': playerarray[2].getHand()},
                            'Player4': {'name': playerarray[3].getName(), 'character': playerarray[3].getCharacter(),
                                        'location': playerarray[3].getLocation(), 'hand': playerarray[3].getHand()},
                            'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(),
                            'gamerunning': gamestate.getGameRunning(), 'messages': messages,
                            'subturn': gamestate.getSubturn(),
                            'gameboard': gamestate.getGameBoard(), 'casefile': gamestate.getCasefile()})
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                        'Player1': {'name': playerarray[0].getName(), 'character': playerarray[0].getCharacter(),
                                    'location': playerarray[0].getLocation(), 'hand': playerarray[0].getHand()},
                        'Player2': {'name': playerarray[1].getName(), 'character': playerarray[1].getCharacter(),
                                    'location': playerarray[1].getLocation(), 'hand': playerarray[1].getHand()},
                        'Player3': {'name': playerarray[2].getName(), 'character': playerarray[2].getCharacter(),
                                    'location': playerarray[2].getLocation(), 'hand': playerarray[2].getHand()},
                        'Player4': {'name': playerarray[3].getName(), 'character': playerarray[3].getCharacter(),
                                    'location': playerarray[3].getLocation(), 'hand': playerarray[3].getHand()},
                        'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(),
                        'gamerunning': gamestate.getGameRunning(), 'messages': messages,
                        'subturn': gamestate.getSubturn(),
                        'gameboard': gamestate.getGameBoard()})
    if len(playerarray) == 5:
        if gamestate.getGameWon():
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
                            'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(),
                            'gamerunning': gamestate.getGameRunning(), 'messages': messages,
                            'subturn': gamestate.getSubturn(),
                            'gameboard': gamestate.getGameBoard(), 'casefile': gamestate.getCasefile()})
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
                        'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(),
                        'gamerunning': gamestate.getGameRunning(), 'messages': messages,
                        'subturn': gamestate.getSubturn(),
                        'gameboard': gamestate.getGameBoard()})
    if len(playerarray) == 6:
        if gamestate.getGameWon():
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
                            'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(),
                            'gamerunning': gamestate.getGameRunning(), 'messages': messages,
                            'subturn': gamestate.getSubturn(),
                            'gameboard': gamestate.getGameBoard(), 'casefile': gamestate.getCasefile()})
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
                        'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(),
                        'gamerunning': gamestate.getGameRunning(), 'messages': messages,
                        'subturn': gamestate.getSubturn(),
                        'gameboard': gamestate.getGameBoard()})
    messagequeue[count].clear()
    return jsonify(
        result="error"
    )


@app.route('/movement', methods=['POST'])
def move():
    if request.method == 'POST':
        some_json = request.get_json()
        character = some_json["character"]
        xcoordinate = some_json["x"]
        ycoordinate = some_json["y"]

        if not isinstance(xcoordinate, int):
            xcoordinate = int(xcoordinate)
        if not isinstance(ycoordinate, int):
            ycoordinate = int(ycoordinate)
        print("Moving player " + character + " to " +
              str(xcoordinate) + ", " + str(ycoordinate))
        newLocation = [xcoordinate, ycoordinate]
        count = 1
        for x in playerarray:
            if x.getName() == character:
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
        return jsonify(
            result="success"
        )
    else:
        return jsonify(
            result="error"
        )


@app.route('/suggestionresponse', methods=['POST'])
def suggresponse():
    some_json = request.get_json()
    suggestion = some_json["childSuggestion"]
    if suggestion == "":
        message = "There were no cards to display."
        receiveplayer = gamestate.getPlayerturn()
        messagequeue[receiveplayer - 1].append(message)
    else:
        message = suggestion
        receiveplayer = gamestate.getPlayerturn()
        messagequeue[receiveplayer - 1].append(message)
    gamestate.setSubturn(0)
    return jsonify(
        result="success"
    )


@app.route('/suggestion', methods=['POST'])
def suggest():
    if (request.method == 'POST'):
        some_json = request.get_json()
        weapon = some_json["weapon"]
        room = some_json["room"]
        character = some_json["suspect"]
        uid = some_json["uid"]
        playcounter = 0
        playercounter = 0
        playercharacter = ""
        for x in uids:
            if x == uid:
                playercharacter = playerarray[playcounter].getCharacter()
                playercounter = playcounter
            playcounter += 1
        xcoordinate = 0
        ycoordinate = 0
        tempcounter = 0
        for temp in suggrooms:
            if temp == room:
                xcoordinate = roomcoordinates[tempcounter][0]
                ycoordinate = roomcoordinates[tempcounter][1]
            tempcounter += 1

        if not isinstance(xcoordinate, int):
            xcoordinate = int(xcoordinate)
        if not isinstance(ycoordinate, int):
            ycoordinate = int(ycoordinate)

        newLocation = [4 - xcoordinate, 4 - ycoordinate]
        weaponloc = []
        weaponname = ""
        for x in weaponsarray:
            if (x.getName() == weapon):
                weaponloc = x.getLocation()
                weaponname = x.getName()
        count = 1
        for x in playerarray:
            if x.getCharacter() == character:
                oldLocation = x.getLocation()
                board = gamestate.getGameBoard()
                arr = board[oldLocation[0]][oldLocation[1]]
                for character2 in range(len(arr)):
                    if arr[character2] == x.getCharacter():
                        arr.pop(character2)
                board[oldLocation[0]][oldLocation[1]] = arr
                arr2 = board[weaponloc[0]][weaponloc[1]]
                for weapon2 in range(len(arr2)):
                    if arr2[weapon2] == weaponname:
                        arr2.pop(weapon2)
                board[weaponloc[0]][weaponloc[1]] = arr2
                arr3 = board[newLocation[0]][newLocation[1]]
                print(arr3)
                arr3.append(weapon)
                print(arr3)
                arr3.append(character)
                print(arr3)
                board[newLocation[0]][newLocation[1]] = arr3
                print(board[newLocation[0]][newLocation[1]])
                x.setLocation(newLocation)
                for x in weaponsarray:
                    if x.getName() == weapon:
                        x.setLocation([newLocation[0], newLocation[1]])
                gamestate.setGameBoard(board)
                message = "[SUGGESTION] {0} suggest that the murder was committed by {1} in the {2} with a {3}".format(
                    playercharacter,
                    character,
                    room,
                    weapon)
                temp = 0
                temp2 = 0
                for y in playerarray:
                    if y.getCharacter() == character:
                        temp2 = temp
                    temp += 1
                messagequeue[temp2].append(message)
                suggestionmessage.append(message)
            count += 1
        counter = 1
        for x in playerarray:
            if x.getCharacter() == character:
                gamestate.setSubturn(counter)
            count += 1

        return jsonify(result='success', message=message)
    else:
        return jsonify(result='error')


@app.route('/accusation', methods=['POST'])
def accuse():
    if request.method == 'POST':
        some_json = request.get_json()
        weapon = some_json["weapon"]
        suspect = some_json["suspect"]
        uid = some_json["uid"]
        room = some_json["room"]
        playcounter = 0
        for x in uids:
            if x == uid:
                character = playerarray[playcounter].getCharacter()
            playcounter += 1
        accusation_set = [room, suspect, weapon]
        message = "[ACCUSATION] {0} has made the accusation that the murder was committed by {1} in the {2} with a {3}".format(
            character,
            suspect,
            room,
            weapon)
        for i in range(6):
            messagequeue[i].append(message)
        if set(accusation_set) == set(casefile):
            message = "[ACCUSATION] {0} has won the game.".format(character)
            for i in range(6):
                messagequeue[i].append(message)
            gamestate.setGameWon(True)
            gamestate.setGameRunning(False)
            return jsonify(
                result="success",
                gamewon=str(gamestate.getGameWon()),
                gamerunning=str(gamestate.getGameRunning()),
                message=message
            )
        message = "[ACCUSATION] {0} has made a false accusation and can no longer win the game.".format(
            character)
        for i in range(6):
            messagequeue[i].append(message)
        return jsonify(
            result="success",
            message=message
        )
    message = "The {0} is not supported by this endpoint. Please try again.".format(
        str(request.method))
    return jsonify(
        result="error",
        message=message
    )


@app.route('/endturn', methods=['POST'])
def endTurn():
    if request.method == 'POST':
        some_json = request.get_json()
        uid = some_json["uid"]
        # will need to add validation for the playernum
        if gamestate.getPlayerturn() == 6:
            gamestate.setPlayerturn = 1
        else:
            gamestate.setPlayerturn(gamestate.getPlayerturn() + 1)
        return jsonify(result="success")


@app.route('/cards', methods=['GET'])
def cards():
    requestJSON = None

    if request.method == 'GET':
        weapons = Cards.WEAPONS
        characters = Cards.CHARACTERS
        rooms = Cards.ROOMS
        return jsonify(json.dumps({'weapons': weapons, 'rooms': rooms, 'characters': characters}))


@ app.route('/')
def index():
    return f"Welcome to ClueLite.\n Click Play to start the game."


if __name__ == "__main__":
    app.run(debug=True)
