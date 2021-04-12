from GameState import GameState
from GameOperations import Players, Weapons, SessionState, Weapdeck, Roomsdeck, Chardeck
from random import randint
from flask import Flask, jsonify, request, render_template, session
from flask_session import Session
from flask_cors import CORS
import uuid
import datetime
import random


rooms = [
    "Kitchen",
    "Conservatory",
    "Dining Room",
    "Ballroom",
    "Study Hall",
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
weapons = [
    "Rope",  # 7
    "Lead Pipe",  # 8
    "Knife",  # 9
    "Wrench",  # 10
    "Candlestick",  # 11
    "Revolver"  # 12
]
characselectdeck = []
app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=365)
app.secret_key = "00000000"
Session(app)

playerturn = 0
roomzdeck = Roomsdeck(rooms)
characdeck = Chardeck(characters)
weapondeck = Weapdeck(weapons)
rope = Weapons(weapons[0], [0, 0, 3], 7)
leadpipe = Weapons(weapons[1], [0, 2, 3], 8)
knife = Weapons(weapons[2], [0, 4, 3], 9)
wrench = Weapons(weapons[3], [2, 0, 3], 10)
candlestick = Weapons(weapons[4], [2, 2, 3], 11)
revolver = Weapons(weapons[5], [2, 4, 3], 12)
weaponsarray = [knife, rope, leadpipe, wrench, candlestick, revolver]
totaldeck = []
playerarray = []
selectedChars = []
casefile = []
subturnqueue = []
gamestate = GameState(casefile, 0, 0, False, [[[0, 0, 0, 7, 0, 0], [0], [0, 0, 0, 8, 0, 0], [0], [0, 0, 0, 9, 0, 0]],
                                              [[0], [99], [0], [99], [0]],
                                              [[0, 0, 0, 10, 0, 0], [0], [0, 0, 0, 11, 0, 0], [0], [0, 0, 0, 12, 0, 0]],
                                              [[0], [99], [0], [99], [0]],
                                              [[0, 0, 0, 0, 0, 0], [0], [0, 0, 0, 0, 0, 0], [0], [0, 0, 0, 0, 0, 0]]],
                      False, 0)

uid = ""
playername = ""
maxSessionPlayers = 6
isSessionFull = False
isPlayerReady = False
sessionstate = SessionState(playername, uid)

CORS(app)

def adduser(uid):
    print("Number of players:  " + str(len(playerarray)))
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
        totaldeck.append(rooms)
        totaldeck.append(characters)
        totaldeck.append(weapons)
        gamestate.setCasefile(casefile)

    for i in range(5):
        playername = "Player" + str(i + 1)
        character = characters[i]
        characselectdeck.append(character)
        hand = []
        location = []
        for i in range(3):
            random.shuffle(totaldeck)
            hand.append(totaldeck[0])
            del totaldeck[0]
        if character == characselectdeck[0]:
            location = [0, 3]
        elif character == characselectdeck[1]:
            location = [4, 3]
        elif character == characselectdeck[2]:
            location = [3, 0]
        elif character == characselectdeck[3]:
            location = [1, 0]
        elif character == characselectdeck[4]:
            location = [4, 1]
        elif character == characselectdeck[5]:
            location = [1, 4]
        player = Players(playername, character, hand, location)
        playerarray.append(player)
        if len(playerarray) == 1:
            gamestate.setNumOfPlayers(1)
        elif len(playerarray) == 2:
            gamestate.setNumOfPlayers(2)
        elif len(playerarray) == 3:
            gamestate.setNumOfPlayers(3)
        elif len(playerarray) == 4:
            gamestate.setNumOfPlayers(4)
        elif len(playerarray) == 5:
            gamestate.setNumOfPlayers(5)
        elif len(playerarray) == 6:
            gamestate.setNumOfPlayers(6)
            gamestate.setGameRunning(True)
            gamestate.setPlayerturn(1)
            sessionstate.isSessionFull(True)
        board = gamestate.getGameBoard()
        board[player.getLocation()[0]][player.getLocation()[1]][0] = len(playerarray)
        gamestate.setGameBoard(board)
        sessionstate.setUid(uid)
        sessionstate.setName(playername)
        return jsonify(result="success", Player1=playername, isSessionFull=isSessionFull)


@app.route('/getsession')
@app.route('/makeready')
@app.route('/session')
def sessions():
    if 'uid' not in session:
        session['uid'] = uuid.uuid4()
        uid = session['uid']
    else:
        uid = session['uid']
    return adduser(uid)

@app.route('/killsession')
def popsession():
    session.pop('uid', None)
    gamestate.setGameRunning(False)
    return "Session deleted"


@app.route('/getstate', methods=['GET'])
def hello():
    if (len(playerarray) == 1):
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                        'Player1': {'name': playerarray[0].getName(), 'character': playerarray[0].getCharacter(),
                                    'location': playerarray[0].getLocation(), 'hand': playerarray[0].getHand()},
                        'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(),
                        'gameboard': gamestate.getGameBoard()})
    if (len(playerarray) == 2):
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                        'Player1': {'name': playerarray[0].getName(), 'character': playerarray[0].getCharacter(),
                                    'location': playerarray[0].getLocation(), 'hand': playerarray[0].getHand()},
                        'Player2': {'name': playerarray[1].getName(), 'character': playerarray[1].getCharacter(),
                                    'location': playerarray[1].getLocation(), 'hand': playerarray[1].getHand()},
                        'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(),
                        'gameboard': gamestate.getGameBoard()})
    if (len(playerarray) == 3):
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                        'Player1': {'name': playerarray[0].getName(), 'character': playerarray[0].getCharacter(),
                                    'location': playerarray[0].getLocation(), 'hand': playerarray[0].getHand()},
                        'Player2': {'name': playerarray[1].getName(), 'character': playerarray[1].getCharacter(),
                                    'location': playerarray[1].getLocation(), 'hand': playerarray[1].getHand()},
                        'Player3': {'name': playerarray[2].getName(), 'character': playerarray[2].getCharacter(),
                                    'location': playerarray[2].getLocation(), 'hand': playerarray[2].getHand()},
                        'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(),
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
                        'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(),
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
        print("Moving player " + character + " to " + str(xcoordinate) + ", " + str(ycoordinate))
        newLocation = [xcoordinate, ycoordinate]
        count = 1
        for x in playerarray:
            print("Checking " + character + " against " + x.getName())
            if (x.getName() == character):
                oldLocation = x.getLocation()
                board = gamestate.getGameBoard()
                board[oldLocation[0]][oldLocation[1]][0] = 0
                board[newLocation[0]][newLocation[1]][0] = count
                
                print("Found match. Moving from " + str(oldLocation))
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
        weaponnum = 0
        for x in weaponsarray:
            if (x.getName() == weapon):
                weaponloc = x.getLocation()
                weaponnum = x.getWeapon()
        count = 1
        for x in playerarray:
            if (x.getCharacter() == character):
                oldLocation = x.getLocation()
                board = gamestate.getGameBoard()
                board[oldLocation[0]][oldLocation[1]][0] = 0
                board[weaponloc[0]][weaponloc[1]][weaponloc[2]] = 0
                board[newLocation[0]][newLocation[1]][0] = count
                board[newLocation[0]][newLocation[1]][3] = weaponnum
                x.setLocation(newLocation)
                for x in weaponsarray:
                    if (x.getName() == weapon):
                        x.setLocation([newLocation[0], newLocation[1], 3])
                gamestate.setGameBoard(board)
                message = "{0} suggest that the murder was committed by {1} in the {2} with a {3}".format(
                    playercharacter,
                    character,
                    room,
                    weapon)
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
        if (gamestate.getPlayerturn() == 4):
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
