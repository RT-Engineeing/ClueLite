from Session import Session
from GameState import GameState
from GameOperations import Players, Weapons, Weapdeck, Roomsdeck, Chardeck
from MessageManager import MessageManager
from flask import Flask, jsonify, request, render_template
from LinkedList import Node, SLinkedList
from flask_cors import CORS
import random
import json
import Cards
import copy
import time

app = Flask(__name__)
rooms = copy.deepcopy(Cards.ROOMS)
suggrooms = copy.deepcopy(Cards.ROOMS)
characters = copy.deepcopy(Cards.CHARACTERS)
charactersind = copy.deepcopy(Cards.CHARACTERS)
weapons = copy.deepcopy(Cards.WEAPONS)

playerturnlist = SLinkedList()
botlist = SLinkedList()
currentNode = Node(99)
node1 = Node(99)
node2 = Node(99)
node3 = Node(99)
node4 = Node(99)
node5 = Node(99)
playernamecache = []

roomcoordinates = [
    [4, 4],  # Kitchen
    [4, 0],  # Conservatory
    [2, 4],  # Dinning Room
    [4, 2],  # Ballroom
    [0, 0],  # Study
    [0, 2],  # Hall
    [0, 4],  # Lounge
    [2, 0],  # library
    [2, 2]  # Billiard Room
]
hallwaycoordinates = [
    [0, 1],  # Study_Hall
    [0, 3],  # Hall_Lounge
    [1, 0],  # Library_Study
    [1, 2],  # Billiard_Hall
    [1, 4],  # Lounge_Dinning
    [2, 1],  # Billiard_Library
    [2, 3],  # Billiard_Dinning
    [3, 0],  # Conservatory_Library
    [3, 2],  # Billiard_Ball
    [3, 4],  # Dinning_Kitchen
    [4, 1],  # Ball_Conservatory
    [4, 3]   # Kitchen_Ball
]
# Available hall paths when moving
Study_Hall = [[0, 0], [0, 2]]
Hall_Lounge = [[0, 2], [0, 4]]
Lounge_Dinning = [[0, 4], [2, 4]]
Dinning_Kitchen = [[2, 4], [4, 4]]
Kitchen_Ball = [[4, 4], [4, 2]]
Ball_Conservatory = [[4, 2], [4, 0]]
Conservatory_Library = [[4, 0], [2, 0]]
Library_Study = [[2, 0], [0, 0]]
Billiard_Hall = [[2, 2], [0, 2]]
Billiard_Library = [[2, 2], [2, 0]]
Billiard_Dinning = [[2, 2], [2, 4]]
Billiard_Ball = [[2, 2], [4, 2]]

# Available room, hall, and secret passage paths when moving
Study = [[4, 4], [0, 1], [1, 0]]
Lounge = [[4, 0], [0, 3], [1, 4]]
Hall = [[0, 1], [0, 3], [1, 2]]
Kitchen = [[0, 0], [3, 4], [4, 3]]
Conservatory = [[0, 4], [4, 1], [3, 0]]
Dinning = [[1, 4], [3, 4], [2, 3]]
Ball = [[4, 3], [4, 1], [3, 2]]
Library = [[3, 0], [2, 1], [1, 0]]
Billiard = [[1, 2], [2, 1], [3, 2], [2, 3]]

boardcoordinates = {
    rooms[0]: roomcoordinates[0],
    rooms[1]: roomcoordinates[1],
    rooms[2]: roomcoordinates[2],
    rooms[3]: roomcoordinates[3],
    rooms[4]: roomcoordinates[4],
    rooms[5]: roomcoordinates[5],
    rooms[6]: roomcoordinates[6],
    rooms[7]: roomcoordinates[7],
    rooms[8]: roomcoordinates[8],
}

uids = []
characteruseddict = {True: [], False: ["Miss Scarlet",
                                       "Mrs. White",
                                       "Mrs. Peacock",
                                       "Professor Plum",
                                       "Mr.Green",
                                       "Colonel Mustard"]}


playerturn = 1
messageManager = MessageManager()
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
                      False, 0, "")
maxSessionPlayer = 0
isPlayerReady = False
tempvar = 0
session = Session(random.randint(100000, 999999), gamestate)
messageToSend = ""


CORS(app)


def validatePlayer(uid):
    for p in playerarray:
        if uid != p.getUid():
            return False


def validatePlayerTurn(uid):
    if uid != currentNode.getuid():
        return False


def validatePlayerSuspect(suspect):
    if suspect not in charactersind:
        return False


def validateHallwayIsEmpty(loc):
    if loc in playerturnlist.getPlayersLoc():
        if loc in hallwaycoordinates:
            return False


def validatePlayerIsInRoom(uid, room):
    loc = boardcoordinates[room]
    if uid == currentNode.getuid():
        p = currentNode.getplayer()
        if p.getLocation in roomcoordinates:
            if p.getLocation() != loc:
                return False


def validateBoardMovement(loc, character):
    busyLocations = playerturnlist.getPlayersLoc()
    p = currentNode.getplayer()
    if character == p.getCharacter():
        charLoc = p.getLocation()
        if charLoc in hallwaycoordinates:
            if charLoc == hallwaycoordinates[0]:
                if loc not in Study_Hall:
                    return False
            elif charLoc == hallwaycoordinates[1]:
                if loc not in Hall_Lounge:
                    return False
            elif charLoc == hallwaycoordinates[2]:
                if loc not in Library_Study:
                    return False
            elif charLoc == hallwaycoordinates[3]:
                if loc not in Billiard_Hall:
                    return False
            elif charLoc == hallwaycoordinates[4]:
                if loc not in Lounge_Dinning:
                    return False
            elif charLoc == hallwaycoordinates[5]:
                if loc not in Billiard_Library:
                    return False
            elif charLoc == hallwaycoordinates[6]:
                if loc not in Billiard_Dinning:
                    return False
            elif charLoc == hallwaycoordinates[7]:
                if loc not in Conservatory_Library:
                    return False
            elif charLoc == hallwaycoordinates[8]:
                if loc not in Billiard_Ball:
                    return False
            elif charLoc == hallwaycoordinates[9]:
                if loc not in Dinning_Kitchen:
                    return False
            elif charLoc == hallwaycoordinates[10]:
                if loc not in Ball_Conservatory:
                    return False
            elif charLoc == hallwaycoordinates[11]:
                if loc not in Kitchen_Ball:
                    return False
        elif charLoc in roomcoordinates:
            if charLoc == roomcoordinates[0]:
                if loc not in Kitchen:
                    return False
                if loc == Kitchen[1]:
                    if loc in busyLocations:
                        return False
                elif loc == Kitchen[2]:
                    if loc in busyLocations:
                        return False
            elif charLoc == roomcoordinates[1]:
                if loc not in Conservatory:
                    return False
                if loc == Conservatory[1]:
                    if loc in busyLocations:
                        return False
                elif loc == Conservatory[2]:
                    if loc in busyLocations:
                        return False
            elif charLoc == roomcoordinates[2]:
                if loc not in Dinning:
                    return False
                if loc == Dinning[0]:
                    if loc in busyLocations:
                        return False
                elif loc == Dinning[1]:
                    if loc in busyLocations:
                        return False
                elif loc == Dinning[2]:
                    if loc in busyLocations:
                        return False
            elif charLoc == roomcoordinates[3]:
                if loc not in Ball:
                    return False
                if loc == Ball[0]:
                    if loc in busyLocations:
                        return False
                elif loc == Ball[1]:
                    if loc in busyLocations:
                        return False
                elif loc == Ball[2]:
                    if loc in busyLocations:
                        return False
            elif charLoc == roomcoordinates[4]:
                if loc not in Study:
                    return False
                if loc == Study[1]:
                    if loc in busyLocations:
                        return False
                elif loc == Study[2]:
                    if loc in busyLocations:
                        return False
            elif charLoc == roomcoordinates[5]:
                if loc not in Hall:
                    return False
                if loc == Hall[0]:
                    if loc in busyLocations:
                        return False
                elif loc == Hall[1]:
                    if loc in busyLocations:
                        return False
                elif loc == Hall[2]:
                    if loc in busyLocations:
                        return False
            elif charLoc == roomcoordinates[6]:
                if loc not in Lounge:
                    return False
                if loc == Lounge[1]:
                    if loc in busyLocations:
                        return False
                elif loc == Lounge[2]:
                    if loc in busyLocations:
                        return False
            elif charLoc == roomcoordinates[7]:
                if loc not in Library:
                    return False
                if loc == Library[0]:
                    if loc in busyLocations:
                        return False
                elif loc == Library[1]:
                    if loc in busyLocations:
                        return False
                elif loc == Library[2]:
                    if loc in busyLocations:
                        return False
            elif charLoc == roomcoordinates[8]:
                if loc not in Billiard:
                    return False
                if loc == Billiard[0]:
                    if loc in busyLocations:
                        return False
                elif loc == Billiard[1]:
                    if loc in busyLocations:
                        return False
                elif loc == Billiard[2]:
                    if loc in busyLocations:
                        return False
                elif loc == Billiard[3]:
                    if loc in busyLocations:
                        return False
        return True


def adduser(uid):
    if playerturnlist.listlength() >= 6:
        sessionstring = jsonify(
            sessionId=str(session.getSessionid()),
            result=" Session is full",
        )
        uids.append(uid)
        return sessionstring
    if playerturnlist.listlength() == 0:
        initgame()
    newgamestate = gamestate
    newgamestate.setCasefile(casefile)
    playername = "Player" + str(playerturnlist.listlength() + 1)
    character = charactersind.pop(random.randrange(len(charactersind)))
    hand = []
    location = []
    if character == 'Miss Scarlet':
        location = [0, 3]
        templist = characteruseddict.get(False)
        templist.remove('Miss Scarlet')
        templist2 = characteruseddict.get(True)
        templist2.append('Miss Scarlet')
        updict = {True: templist2}
        updict2 = {False: templist}
        characteruseddict.update(updict)
        characteruseddict.update(updict2)
    elif character == 'Mrs. White':
        location = [4, 3]
        templist = characteruseddict.get(False)
        templist.remove('Mrs. White')
        templist2 = characteruseddict.get(True)
        templist2.append('Mrs. White')
        updict = {True: templist2}
        updict2 = {False: templist}
        characteruseddict.update(updict)
        characteruseddict.update(updict2)
    elif character == 'Mrs. Peacock':
        location = [3, 0]
        templist = characteruseddict.get(False)
        templist.remove('Mrs. Peacock')
        templist2 = characteruseddict.get(True)
        templist2.append('Mrs. Peacock')
        updict = {True: templist2}
        updict2 = {False: templist}
        characteruseddict.update(updict)
        characteruseddict.update(updict2)
    elif character == 'Professor Plum':
        location = [1, 0]
        templist = characteruseddict.get(False)
        templist.remove('Professor Plum')
        templist2 = characteruseddict.get(True)
        templist2.append('Professor Plum')
        updict = {True: templist2}
        updict2 = {False: templist}
        characteruseddict.update(updict)
        characteruseddict.update(updict2)
    elif character == 'Mr.Green':
        location = [4, 1]
        templist = characteruseddict.get(False)
        templist.remove('Mr.Green')
        templist2 = characteruseddict.get(True)
        templist2.append('Mr.Green')
        updict = {True: templist2}
        updict2 = {False: templist}
        characteruseddict.update(updict)
        characteruseddict.update(updict2)
    elif character == 'Colonel Mustard':
        location = [1, 4]
        templist = characteruseddict.get(False)
        templist.remove('Colonel Mustard')
        templist2 = characteruseddict.get(True)
        templist2.append('Colonel Mustard')
        updict = {True: templist2}
        updict2 = {False: templist}
        characteruseddict.update(updict)
        characteruseddict.update(updict2)
    player = Players(playername, uid, character, hand, location)
    playerarray.append(player)
    print("setting hand for " + character + ": " + str(hand))
    if playerturnlist.listlength() == 0:
        playerturnlist.headval = Node(1, uid, player)
        global currentNode
        currentNode = playerturnlist.headval
    elif playerturnlist.listlength() == 1:
        global node1
        node1 = Node(playerturnlist.listlength() + 1, uid, player)
        currentNode.nextval = node1
    elif playerturnlist.listlength() == 2:
        global node2
        node2 = Node(playerturnlist.listlength() + 1, uid, player)
        node1.nextval = node2
    elif playerturnlist.listlength() == 3:
        global node3
        node3 = Node(playerturnlist.listlength() + 1, uid, player)
        node2.nextval = node3
    elif playerturnlist.listlength() == 4:
        global node4
        node4 = Node(playerturnlist.listlength() + 1, uid, player)
        node3.nextval = node4
    elif playerturnlist.listlength() == 5:
        global node5
        node5 = Node(playerturnlist.listlength() + 1, uid, player)
        node4.nextval = node5
    newgamestate.setNumOfPlayers(playerturnlist.listlength())
    board = newgamestate.getGameBoard()
    arr = board[player.getLocation()[0]][player.getLocation()[1]]
    arr.append(player.getCharacter())
    board[player.getLocation()[0]][player.getLocation()[1]] = arr
    newgamestate.setGameBoard(board)
    session.setGameState(newgamestate)
    session.setPlayernum(playerturnlist.listlength())
    sessionstring = jsonify(
        sessionId=str(session.getSessionid()),
        uid=str(uid),
        playername=playername,
        totalPlayers=session.getPlayernum(),
        yourcharacter=player.getCharacter(),
        result=playername + " has been added to the session.",
    )
    uids.append(uid)
    messageManager.addUuid(uid)
    return sessionstring


def initgame():
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


@app.route('/ready', methods=['POST', 'GET'])
def playersready():
    if request.method == 'POST':
        some_json = request.get_json()
        playername = some_json["playerAlias"]
        sessionId = some_json["sessionId"]
        playerready = some_json["playerready"]
        playeruid = some_json["uid"]
        global currentNode
        global playernamecache
        global node3
        global node4
        global node5
        if playerready == "True":
            isReady = True
            # session.addPlayer(playername)
            if currentNode.uid == playeruid:
                tempplayer = currentNode.getplayer()
                tempplayer.setName(playername)
                currentNode.setready(isReady)
                currentNode.setplayer(tempplayer)
            else:
                currentNode = playerturnlist.headval
                while currentNode is not None:
                    if currentNode.getuid() == playeruid:
                        tempplayer = currentNode.getplayer()
                        tempplayer.setName(playername)
                        currentNode.setready(isReady)
                        currentNode.setplayer(tempplayer)
                    currentNode = currentNode.nextval
                currentNode = playerturnlist.headval
            if (playerturnlist.checkready()) and (playerturnlist.listlength() >= 2):
                gamestate.setGameRunning(True)
                gamestate.setNumOfPlayers(playerturnlist.listlength())
                gamestate.setPlayerturn(1)
                currentNode = playerturnlist.headval
                if playerturnlist.listlength() == 4:
                    extracounter = 0
                    while currentNode is not None:
                        playerobj = currentNode.getplayer()
                        playernamecache.append(playerobj.getName())
                        temphand = playerobj.getHand()
                        for i in range(4):
                            random.shuffle(totaldeck)
                            temphand.append(totaldeck[0])
                            del totaldeck[0]
                        if extracounter == 0 or extracounter == 1:
                            random.shuffle(totaldeck)
                            temphand.append(totaldeck[0])
                            del totaldeck[0]
                        playerobj.setHand(temphand)
                        currentNode.setplayer(playerobj)
                        currentNode = currentNode.nextval
                        extracounter += 1
                    for i in range(2):
                        character = charactersind.pop(
                            random.randrange(len(charactersind)))
                        location = []
                        if character == 'Miss Scarlet':
                            location = [0, 3]
                            templist = characteruseddict.get(False)
                            templist.remove('Miss Scarlet')
                            templist2 = characteruseddict.get(True)
                            templist2.append('Miss Scarlet')
                            updict = {True: templist2}
                            updict2 = {False: templist}
                            characteruseddict.update(updict)
                            characteruseddict.update(updict2)
                        elif character == 'Mrs. White':
                            location = [4, 3]
                            templist = characteruseddict.get(False)
                            templist.remove('Mrs. White')
                            templist2 = characteruseddict.get(True)
                            templist2.append('Mrs. White')
                            updict = {True: templist2}
                            updict2 = {False: templist}
                            characteruseddict.update(updict)
                            characteruseddict.update(updict2)
                        elif character == 'Mrs. Peacock':
                            location = [3, 0]
                            templist = characteruseddict.get(False)
                            templist.remove('Mrs. Peacock')
                            templist2 = characteruseddict.get(True)
                            templist2.append('Mrs. Peacock')
                            updict = {True: templist2}
                            updict2 = {False: templist}
                            characteruseddict.update(updict)
                            characteruseddict.update(updict2)
                        elif character == 'Professor Plum':
                            location = [1, 0]
                            templist = characteruseddict.get(False)
                            templist.remove('Professor Plum')
                            templist2 = characteruseddict.get(True)
                            templist2.append('Professor Plum')
                            updict = {True: templist2}
                            updict2 = {False: templist}
                            characteruseddict.update(updict)
                            characteruseddict.update(updict2)
                        elif character == 'Mr.Green':
                            location = [4, 1]
                            templist = characteruseddict.get(False)
                            templist.remove('Mr.Green')
                            templist2 = characteruseddict.get(True)
                            templist2.append('Mr.Green')
                            updict = {True: templist2}
                            updict2 = {False: templist}
                            characteruseddict.update(updict)
                            characteruseddict.update(updict2)
                        elif character == 'Colonel Mustard':
                            location = [1, 4]
                            templist = characteruseddict.get(False)
                            templist.remove('Colonel Mustard')
                            templist2 = characteruseddict.get(True)
                            templist2.append('Colonel Mustard')
                            updict = {True: templist2}
                            updict2 = {False: templist}
                            characteruseddict.update(updict)
                            characteruseddict.update(updict2)
                        bothand = []
                        if i == 0:
                            newgamestate = session.getGameState()
                            bot1 = Players("bot1", character,
                                           bothand, location)
                            node4 = Node(
                                playerturnlist.listlength() + 1, 1, bot1)
                            node4.setready(False)
                            node3.nextval = node4
                            board = newgamestate.getGameBoard()
                            arr = board[bot1.getLocation()[0]
                                        ][bot1.getLocation()[1]]
                            arr.append(bot1.getCharacter())
                            board[bot1.getLocation()[0]][bot1.getLocation()[
                                1]] = arr
                            newgamestate.setGameBoard(board)
                            session.setGameState(newgamestate)
                        else:
                            newgamestate = session.getGameState()
                            bot2 = Players("bot2", character,
                                           bothand, location)
                            node5 = Node(
                                playerturnlist.listlength() + 1, 2, bot2)
                            node5.setready(False)
                            node4.nextval = node5
                            board = newgamestate.getGameBoard()
                            arr = board[bot2.getLocation()[0]
                                        ][bot2.getLocation()[1]]
                            arr.append(bot2.getCharacter())
                            board[bot2.getLocation()[0]][bot2.getLocation()[
                                1]] = arr
                            newgamestate.setGameBoard(board)
                            session.setGameState(newgamestate)
                if playerturnlist.listlength() == 5:
                    extracounter = 0
                    while currentNode is not None:
                        playerobj = currentNode.getplayer()
                        playernamecache.append(playerobj.getName())
                        temphand = playerobj.getHand()
                        for i in range(3):
                            random.shuffle(totaldeck)
                            temphand.append(totaldeck[0])
                            del totaldeck[0]
                        if extracounter == 0 or extracounter == 1 or extracounter == 2:
                            random.shuffle(totaldeck)
                            temphand.append(totaldeck[0])
                            del totaldeck[0]
                        playerobj.setHand(temphand)
                        currentNode.setplayer(playerobj)
                        currentNode = currentNode.nextval
                        extracounter += 1
                    for i in range(1):
                        character = charactersind.pop(
                            random.randrange(len(charactersind)))
                        location = []
                        if character == 'Miss Scarlet':
                            location = [0, 3]
                            templist = characteruseddict.get(False)
                            templist.remove('Miss Scarlet')
                            templist2 = characteruseddict.get(True)
                            templist2.append('Miss Scarlet')
                            updict = {True: templist2}
                            updict2 = {False: templist}
                            characteruseddict.update(updict)
                            characteruseddict.update(updict2)
                        elif character == 'Mrs. White':
                            location = [4, 3]
                            templist = characteruseddict.get(False)
                            templist.remove('Mrs. White')
                            templist2 = characteruseddict.get(True)
                            templist2.append('Mrs. White')
                            updict = {True: templist2}
                            updict2 = {False: templist}
                            characteruseddict.update(updict)
                            characteruseddict.update(updict2)
                        elif character == 'Mrs. Peacock':
                            location = [3, 0]
                            templist = characteruseddict.get(False)
                            templist.remove('Mrs. Peacock')
                            templist2 = characteruseddict.get(True)
                            templist2.append('Mrs. Peacock')
                            updict = {True: templist2}
                            updict2 = {False: templist}
                            characteruseddict.update(updict)
                            characteruseddict.update(updict2)
                        elif character == 'Professor Plum':
                            location = [1, 0]
                            templist = characteruseddict.get(False)
                            templist.remove('Professor Plum')
                            templist2 = characteruseddict.get(True)
                            templist2.append('Professor Plum')
                            updict = {True: templist2}
                            updict2 = {False: templist}
                            characteruseddict.update(updict)
                            characteruseddict.update(updict2)
                        elif character == 'Mr.Green':
                            location = [4, 1]
                            templist = characteruseddict.get(False)
                            templist.remove('Mr.Green')
                            templist2 = characteruseddict.get(True)
                            templist2.append('Mr.Green')
                            updict = {True: templist2}
                            updict2 = {False: templist}
                            characteruseddict.update(updict)
                            characteruseddict.update(updict2)
                        elif character == 'Colonel Mustard':
                            location = [1, 4]
                            templist = characteruseddict.get(False)
                            templist.remove('Colonel Mustard')
                            templist2 = characteruseddict.get(True)
                            templist2.append('Colonel Mustard')
                            updict = {True: templist2}
                            updict2 = {False: templist}
                            characteruseddict.update(updict)
                            characteruseddict.update(updict2)
                        bothand = []
                        if i == 0:
                            newgamestate = session.getGameState()
                            bot1 = Players("bot1", character,
                                           bothand, location)
                            node5 = Node(
                                playerturnlist.listlength() + 1, 1, bot1)
                            node5.setready(False)
                            node4.nextval = node5
                            board = newgamestate.getGameBoard()
                            arr = board[bot1.getLocation()[0]
                                        ][bot1.getLocation()[1]]
                            arr.append(bot1.getCharacter())
                            board[bot1.getLocation()[0]][bot1.getLocation()[
                                1]] = arr
                            newgamestate.setGameBoard(board)
                            session.setGameState(newgamestate)
                if playerturnlist.listlength() == 6:
                    while currentNode is not None:
                        playerobj = currentNode.getplayer()
                        playernamecache.append(playerobj.getName())
                        temphand = playerobj.getHand()
                        for i in range(3):
                            random.shuffle(totaldeck)
                            temphand.append(totaldeck[0])
                            del totaldeck[0]
                        playerobj.setHand(temphand)
                        currentNode.setplayer(playerobj)
                        currentNode = currentNode.nextval
                if playerturnlist.listlength() == 3:
                    while currentNode is not None:
                        playerobj = currentNode.getplayer()
                        playernamecache.append(playerobj.getName())
                        temphand = playerobj.getHand()
                        for i in range(6):
                            random.shuffle(totaldeck)
                            temphand.append(totaldeck[0])
                            del totaldeck[0]
                        playerobj.setHand(temphand)
                        currentNode.setplayer(playerobj)
                        currentNode = currentNode.nextval
                    for i in range(3):
                        character = charactersind.pop(
                            random.randrange(len(charactersind)))
                        location = []
                        if character == 'Miss Scarlet':
                            location = [0, 3]
                            templist = characteruseddict.get(False)
                            templist.remove('Miss Scarlet')
                            templist2 = characteruseddict.get(True)
                            templist2.append('Miss Scarlet')
                            updict = {True: templist2}
                            updict2 = {False: templist}
                            characteruseddict.update(updict)
                            characteruseddict.update(updict2)
                        elif character == 'Mrs. White':
                            location = [4, 3]
                            templist = characteruseddict.get(False)
                            templist.remove('Mrs. White')
                            templist2 = characteruseddict.get(True)
                            templist2.append('Mrs. White')
                            updict = {True: templist2}
                            updict2 = {False: templist}
                            characteruseddict.update(updict)
                            characteruseddict.update(updict2)
                        elif character == 'Mrs. Peacock':
                            location = [3, 0]
                            templist = characteruseddict.get(False)
                            templist.remove('Mrs. Peacock')
                            templist2 = characteruseddict.get(True)
                            templist2.append('Mrs. Peacock')
                            updict = {True: templist2}
                            updict2 = {False: templist}
                            characteruseddict.update(updict)
                            characteruseddict.update(updict2)
                        elif character == 'Professor Plum':
                            location = [1, 0]
                            templist = characteruseddict.get(False)
                            templist.remove('Professor Plum')
                            templist2 = characteruseddict.get(True)
                            templist2.append('Professor Plum')
                            updict = {True: templist2}
                            updict2 = {False: templist}
                            characteruseddict.update(updict)
                            characteruseddict.update(updict2)
                        elif character == 'Mr.Green':
                            location = [4, 1]
                            templist = characteruseddict.get(False)
                            templist.remove('Mr.Green')
                            templist2 = characteruseddict.get(True)
                            templist2.append('Mr.Green')
                            updict = {True: templist2}
                            updict2 = {False: templist}
                            characteruseddict.update(updict)
                            characteruseddict.update(updict2)
                        elif character == 'Colonel Mustard':
                            location = [1, 4]
                            templist = characteruseddict.get(False)
                            templist.remove('Colonel Mustard')
                            templist2 = characteruseddict.get(True)
                            templist2.append('Colonel Mustard')
                            updict = {True: templist2}
                            updict2 = {False: templist}
                            characteruseddict.update(updict)
                            characteruseddict.update(updict2)
                        bothand = []
                        if i == 0:
                            newgamestate = session.getGameState()
                            bot1 = Players("bot1", character,
                                           bothand, location)
                            node3 = Node(
                                playerturnlist.listlength() + 1, 1, bot1)
                            node3.setready(False)
                            node2.nextval = node3
                            board = newgamestate.getGameBoard()
                            arr = board[bot1.getLocation()[0]
                                        ][bot1.getLocation()[1]]
                            arr.append(bot1.getCharacter())
                            board[bot1.getLocation()[0]][bot1.getLocation()[
                                1]] = arr
                            newgamestate.setGameBoard(board)
                            session.setGameState(newgamestate)
                        elif i == 1:
                            newgamestate = session.getGameState()
                            bot2 = Players("bot2", character,
                                           bothand, location)
                            node4 = Node(
                                playerturnlist.listlength() + 1, 2, bot2)
                            node4.setready(False)
                            node3.nextval = node4
                            board = newgamestate.getGameBoard()
                            arr = board[bot2.getLocation()[0]
                                        ][bot2.getLocation()[1]]
                            arr.append(bot2.getCharacter())
                            board[bot2.getLocation()[0]][bot2.getLocation()[
                                1]] = arr
                            newgamestate.setGameBoard(board)
                            session.setGameState(newgamestate)
                        else:
                            newgamestate = session.getGameState()
                            bot3 = Players("bot3", character,
                                           bothand, location)
                            node5 = Node(
                                playerturnlist.listlength() + 1, 3, bot3)
                            node5.setready(False)
                            node4.nextval = node5
                            board = newgamestate.getGameBoard()
                            arr = board[bot3.getLocation()[0]
                                        ][bot3.getLocation()[1]]
                            arr.append(bot3.getCharacter())
                            board[bot3.getLocation()[0]][bot3.getLocation()[
                                1]] = arr
                            newgamestate.setGameBoard(board)
                            session.setGameState(newgamestate)
                currentNode = playerturnlist.headval
            return jsonify(
                sessionId=sessionId,
                playername=playername,
                playerready=str(isReady),
                result=playername + " is ready."
            )
        else:
            isReady = False
            if currentNode.uid == playeruid:
                tempplayer = currentNode.getplayer()
                tempplayer.setName(playername)
                currentNode.setready(isReady)
                currentNode.setplayer(tempplayer)
            else:
                currentNode = playerturnlist.headval
                while currentNode is not None:
                    if currentNode.getuid() == playeruid:
                        tempplayer = currentNode.getplayer()
                        tempplayer.setName(playername)
                        currentNode.setready(isReady)
                        currentNode.setplayer(tempplayer)
                    currentNode = currentNode.nextval
                currentNode = playerturnlist.headval
            return jsonify(
                sessionId=sessionId,
                playername=playername,
                playerready=str(isReady),
                result=playername + " is not ready."
            )
    elif request.method == 'GET':
        lobbyPlayers = []
        readyPlayers = []
        currentNode = playerturnlist.headval
        holder = playerturnlist.listlength()
        while currentNode is not None:
            templayer = currentNode.getplayer()
            playername = templayer.getName()
            if currentNode.getready():
                readyPlayers.append(playername)
            lobbyPlayers.append(playername)
            currentNode = currentNode.nextval
        currentNode = playerturnlist.headval
        if gamestate.getGameRunning():
            return jsonify(status='true',
                           playersready=readyPlayers,
                           lobbyPlayers=lobbyPlayers
                           )
        else:
            return jsonify(status='false',
                           playersready=readyPlayers,
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
    serverAlerts = messageManager.getMessages(uid)

    messageToSend = ""
    localMessage = messageToSend
    count = 0
    for x in uids:
        if x == uid:
            messages = messagequeue[count]
        count += 1
    global playernamecache
    if playerturnlist.listlength() == 1:
        tempplayers = []
        holdernode = playerturnlist.headval
        if holdernode is not None:
            tempplayers.append(holdernode.getplayer())
        if gamestate.getGameWon():
            return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                            'Player1': {'name': playernamecache[0], 'character': tempplayers[0].getCharacter(),
                                        'location': tempplayers[0].getLocation(), 'hand': tempplayers[0].getHand()},
                            'playerturn': getTurnName(), 'gamestatus': gamestate.getGameWon(),
                            'gamerunning': gamestate.getGameRunning(), 'messages': messages,
                            'subturn': gamestate.getSubturn(),
                            'gameboard': gamestate.getGameBoard(), 'casefile': gamestate.getCasefile()})
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                        'Player1': {'name': playernamecache[0], 'character': tempplayers[0].getCharacter(),
                                    'location': tempplayers[0].getLocation(), 'hand': tempplayers[0].getHand()},
                        'playerturn': getTurnName(), 'gamestatus': gamestate.getGameWon(),
                        'gamerunning': gamestate.getGameRunning(), 'messages': messages,
                        'alerts': serverAlerts,
                        'subturn': gamestate.getSubturn(),
                        'gameboard': gamestate.getGameBoard()})
    if playerturnlist.listlength() == 2:
        tempplayers = []
        holdernode = playerturnlist.headval
        while holdernode is not None:
            tempplayers.append(holdernode.getplayer())
            holdernode = holdernode.nextval
        if gamestate.getGameWon():
            return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                            'Player1': {'name': tempplayers[0].getName(), 'character': tempplayers[0].getCharacter(),
                                        'location': tempplayers[0].getLocation(), 'hand': tempplayers[0].getHand()},
                            'Player2': {'name': tempplayers[1].getName(), 'character': tempplayers[1].getCharacter(),
                                        'location': tempplayers[1].getLocation(), 'hand': tempplayers[1].getHand()},
                            'playerturn': getTurnName(), 'gamestatus': gamestate.getGameWon(),
                            'gamerunning': gamestate.getGameRunning(), 'messages': messages,
                            'alerts': serverAlerts,
                            'subturn': gamestate.getSubturn(),
                            'gameboard': gamestate.getGameBoard(), 'casefile': gamestate.getCasefile()})
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                        'Player1': {'name': tempplayers[0].getName(), 'character': tempplayers[0].getCharacter(),
                                    'location': tempplayers[0].getLocation(), 'hand': tempplayers[0].getHand()},
                        'Player2': {'name': tempplayers[1].getName(), 'character': tempplayers[1].getCharacter(),
                                    'location': tempplayers[1].getLocation(), 'hand': tempplayers[1].getHand()},
                        'playerturn': getTurnName(), 'gamestatus': gamestate.getGameWon(),
                        'gamerunning': gamestate.getGameRunning(), 'messages': messages,
                        'alerts': serverAlerts,
                        'subturn': gamestate.getSubturn(),
                        'gameboard': gamestate.getGameBoard()})
    if playerturnlist.listlength() == 3:
        tempplayers = []
        holdernode = playerturnlist.headval
        while holdernode is not None:
            tempplayers.append(holdernode.getplayer())
            holdernode = holdernode.nextval
        if gamestate.getGameWon():
            return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                            'Player1': {'name': tempplayers[0].getName(), 'character': tempplayers[0].getCharacter(),
                                        'location': tempplayers[0].getLocation(), 'hand': tempplayers[0].getHand()},
                            'Player2': {'name': tempplayers[1].getName(), 'character': tempplayers[1].getCharacter(),
                                        'location': tempplayers[1].getLocation(), 'hand': tempplayers[1].getHand()},
                            'Player3': {'name': tempplayers[2].getName(), 'character': tempplayers[2].getCharacter(),
                                        'location': tempplayers[2].getLocation(), 'hand': tempplayers[2].getHand()},
                            'playerturn': getTurnName(), 'gamestatus': gamestate.getGameWon(),
                            'gamerunning': gamestate.getGameRunning(), 'messages': messages,
                            'alerts': serverAlerts,
                            'subturn': gamestate.getSubturn(),
                            'gameboard': gamestate.getGameBoard(), 'casefile': gamestate.getCasefile()})
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                        'Player1': {'name': tempplayers[0].getName(), 'character': tempplayers[0].getCharacter(),
                                    'location': tempplayers[0].getLocation(), 'hand': tempplayers[0].getHand()},
                        'Player2': {'name': tempplayers[1].getName(), 'character': tempplayers[1].getCharacter(),
                                    'location': tempplayers[1].getLocation(), 'hand': tempplayers[1].getHand()},
                        'Player3': {'name': tempplayers[2].getName(), 'character': tempplayers[2].getCharacter(),
                                    'location': tempplayers[2].getLocation(), 'hand': tempplayers[2].getHand()},
                        'playerturn': getTurnName(), 'gamestatus': gamestate.getGameWon(),
                        'gamerunning': gamestate.getGameRunning(), 'messages': messages,
                        'alerts': serverAlerts,
                        'subturn': gamestate.getSubturn(),
                        'gameboard': gamestate.getGameBoard()})
    if playerturnlist.listlength() == 4:
        tempplayers = []
        holdernode = playerturnlist.headval
        while holdernode is not None:
            tempplayers.append(holdernode.getplayer())
            holdernode = holdernode.nextval
        if gamestate.getGameWon():
            return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                            'Player1': {'name': tempplayers[0].getName(), 'character': tempplayers[0].getCharacter(),
                                        'location': tempplayers[0].getLocation(), 'hand': tempplayers[0].getHand()},
                            'Player2': {'name': tempplayers[1].getName(), 'character': tempplayers[1].getCharacter(),
                                        'location': tempplayers[1].getLocation(), 'hand': tempplayers[1].getHand()},
                            'Player3': {'name': tempplayers[2].getName(), 'character': tempplayers[2].getCharacter(),
                                        'location': tempplayers[2].getLocation(), 'hand': tempplayers[2].getHand()},
                            'Player4': {'name': tempplayers[3].getName(), 'character': tempplayers[3].getCharacter(),
                                        'location': tempplayers[3].getLocation(), 'hand': tempplayers[3].getHand()},
                            'playerturn': getTurnName(), 'gamestatus': gamestate.getGameWon(),
                            'gamerunning': gamestate.getGameRunning(), 'messages': messages,
                            'alerts': serverAlerts,
                            'subturn': gamestate.getSubturn(),
                            'gameboard': gamestate.getGameBoard(), 'casefile': gamestate.getCasefile()})
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                        'Player1': {'name': tempplayers[0].getName(), 'character': tempplayers[0].getCharacter(),
                                    'location': tempplayers[0].getLocation(), 'hand': tempplayers[0].getHand()},
                        'Player2': {'name': tempplayers[1].getName(), 'character': tempplayers[1].getCharacter(),
                                    'location': tempplayers[1].getLocation(), 'hand': tempplayers[1].getHand()},
                        'Player3': {'name': tempplayers[2].getName(), 'character': tempplayers[2].getCharacter(),
                                    'location': tempplayers[2].getLocation(), 'hand': tempplayers[2].getHand()},
                        'Player4': {'name': tempplayers[3].getName(), 'character': tempplayers[3].getCharacter(),
                                    'location': tempplayers[3].getLocation(), 'hand': tempplayers[3].getHand()},
                        'playerturn': getTurnName(), 'gamestatus': gamestate.getGameWon(),
                        'gamerunning': gamestate.getGameRunning(), 'messages': messages,
                        'alerts': serverAlerts,
                        'subturn': gamestate.getSubturn(),
                        'gameboard': gamestate.getGameBoard()})
    if playerturnlist.listlength() == 5:
        tempplayers = []
        holdernode = playerturnlist.headval
        while holdernode is not None:
            tempplayers.append(holdernode.getplayer())
            holdernode = holdernode.nextval
        if gamestate.getGameWon():
            return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                            'Player1': {'name': tempplayers[0].getName(), 'character': tempplayers[0].getCharacter(),
                                        'location': tempplayers[0].getLocation(), 'hand': tempplayers[0].getHand()},
                            'Player2': {'name': tempplayers[1].getName(), 'character': tempplayers[1].getCharacter(),
                                        'location': tempplayers[1].getLocation(), 'hand': tempplayers[1].getHand()},
                            'Player3': {'name': tempplayers[2].getName(), 'character': tempplayers[2].getCharacter(),
                                        'location': tempplayers[2].getLocation(), 'hand': tempplayers[2].getHand()},
                            'Player4': {'name': tempplayers[3].getName(), 'character': tempplayers[3].getCharacter(),
                                        'location': tempplayers[3].getLocation(), 'hand': tempplayers[3].getHand()},
                            'Player5': {'name': tempplayers[4].getName(), 'character': tempplayers[4].getCharacter(),
                                        'location': tempplayers[4].getLocation(), 'hand': tempplayers[4].getHand()},
                            'playerturn': getTurnName(), 'gamestatus': gamestate.getGameWon(),
                            'gamerunning': gamestate.getGameRunning(), 'messages': messages,
                            'alerts': serverAlerts,
                            'subturn': gamestate.getSubturn(),
                            'gameboard': gamestate.getGameBoard(), 'casefile': gamestate.getCasefile()})
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                        'Player1': {'name': tempplayers[0].getName(), 'character': tempplayers[0].getCharacter(),
                                    'location': tempplayers[0].getLocation(), 'hand': tempplayers[0].getHand()},
                        'Player2': {'name': tempplayers[1].getName(), 'character': tempplayers[1].getCharacter(),
                                    'location': tempplayers[1].getLocation(), 'hand': tempplayers[1].getHand()},
                        'Player3': {'name': tempplayers[2].getName(), 'character': tempplayers[2].getCharacter(),
                                    'location': tempplayers[2].getLocation(), 'hand': tempplayers[2].getHand()},
                        'Player4': {'name': tempplayers[3].getName(), 'character': tempplayers[3].getCharacter(),
                                    'location': tempplayers[3].getLocation(), 'hand': tempplayers[3].getHand()},
                        'Player5': {'name': tempplayers[4].getName(), 'character': tempplayers[4].getCharacter(),
                                    'location': tempplayers[4].getLocation(), 'hand': tempplayers[4].getHand()},
                        'playerturn': getTurnName(), 'gamestatus': gamestate.getGameWon(),
                        'gamerunning': gamestate.getGameRunning(), 'messages': messages,
                        'alerts': serverAlerts,
                        'subturn': gamestate.getSubturn(),
                        'gameboard': gamestate.getGameBoard()})
    if playerturnlist.listlength() == 6:
        tempplayers = []
        holdernode = playerturnlist.headval
        while holdernode is not None:
            tempplayers.append(holdernode.getplayer())
            holdernode = holdernode.nextval
        if gamestate.getGameWon():
            return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                            'Player1': {'name': tempplayers[0].getName(), 'character': tempplayers[0].getCharacter(),
                                        'location': tempplayers[0].getLocation(), 'hand': tempplayers[0].getHand()},
                            'Player2': {'name': tempplayers[1].getName(), 'character': tempplayers[1].getCharacter(),
                                        'location': tempplayers[1].getLocation(), 'hand': tempplayers[1].getHand()},
                            'Player3': {'name': tempplayers[2].getName(), 'character': tempplayers[2].getCharacter(),
                                        'location': tempplayers[2].getLocation(), 'hand': tempplayers[2].getHand()},
                            'Player4': {'name': tempplayers[3].getName(), 'character': tempplayers[3].getCharacter(),
                                        'location': tempplayers[3].getLocation(), 'hand': tempplayers[3].getHand()},
                            'Player5': {'name': tempplayers[4].getName(), 'character': tempplayers[4].getCharacter(),
                                        'location': tempplayers[4].getLocation(), 'hand': tempplayers[4].getHand()},
                            'Player6': {'name': tempplayers[5].getName(), 'character': tempplayers[5].getCharacter(),
                                        'location': tempplayers[5].getLocation(), 'hand': tempplayers[5].getHand()},
                            'playerturn': getTurnName(), 'gamestatus': gamestate.getGameWon(),
                            'gamerunning': gamestate.getGameRunning(), 'messages': messages,
                            'alerts': serverAlerts,
                            'subturn': gamestate.getSubturn(),
                            'gameboard': gamestate.getGameBoard(), 'casefile': gamestate.getCasefile()})
        return jsonify({'numberofplayers': gamestate.getNumOfPlayers(),
                        'Player1': {'name': tempplayers[0].getName(), 'character': tempplayers[0].getCharacter(),
                                    'location': tempplayers[0].getLocation(), 'hand': tempplayers[0].getHand()},
                        'Player2': {'name': tempplayers[1].getName(), 'character': tempplayers[1].getCharacter(),
                                    'location': tempplayers[1].getLocation(), 'hand': tempplayers[1].getHand()},
                        'Player3': {'name': tempplayers[2].getName(), 'character': tempplayers[2].getCharacter(),
                                    'location': tempplayers[2].getLocation(), 'hand': tempplayers[2].getHand()},
                        'Player4': {'name': tempplayers[3].getName(), 'character': tempplayers[3].getCharacter(),
                                    'location': tempplayers[3].getLocation(), 'hand': tempplayers[3].getHand()},
                        'Player5': {'name': tempplayers[4].getName(), 'character': tempplayers[4].getCharacter(),
                                    'location': tempplayers[4].getLocation(), 'hand': tempplayers[4].getHand()},
                        'Player6': {'name': tempplayers[5].getName(), 'character': tempplayers[5].getCharacter(),
                                    'location': tempplayers[5].getLocation(), 'hand': tempplayers[5].getHand()},
                        'playerturn': getTurnName(), 'gamestatus': gamestate.getGameWon(),
                        'gamerunning': gamestate.getGameRunning(), 'messages': messages,
                        'alerts': serverAlerts,
                        'subturn': gamestate.getSubturn(),
                        'gameboard': gamestate.getGameBoard()})
    messagequeue[count].clear()
    return jsonify(
        result="error"
    )


def getTurnName():
    global currentNode
    turnUid = currentNode.uid
    for x in playerarray:
        if x.getUuid() == turnUid:
            return x.getCharacter()


@app.route('/chat', methods=['POST'])
def chat():
    if request.method == 'POST':

        some_json = request.get_json()
        character = some_json["character"]
        message = some_json["message"]
        print("chat message " + message + " received")
        messageManager.addMessage("(" + character + "): " + message)
        return jsonify(
            result="success"
        )


@app.route('/movement', methods=['POST'])
def move():
    if request.method == 'POST':
        some_json = request.get_json()
        character = some_json["character"]
        uid = some_json["uid"]
        xcoordinate = some_json["x"]
        ycoordinate = some_json["y"]
        if not isinstance(xcoordinate, int):
            xcoordinate = int(xcoordinate)
        if not isinstance(ycoordinate, int):
            ycoordinate = int(ycoordinate)
        loc = [xcoordinate, ycoordinate]
        if validatePlayerTurn(uid) is False:
            return jsonify(
                result="error",
                message="The attempted operation is invalid. Player is out of turn."
            )
        if validateBoardMovement(loc, character) is False:
            return jsonify(
                result="error",
                message="The attempted operation is invalid. Please try a valid movement."
            )

        print("Moving player " + character + " to " +
              str(xcoordinate) + ", " + str(ycoordinate))
        roomnamekey = str(xcoordinate) + str(ycoordinate)
        roomname = roomnames.get(roomnamekey)
        if roomname == None:
            roomname = "a Hallway"
        else:
            roomname = "the " + roomname

        print("roomkey: " + roomnamekey + " room name: " + roomname)
        for x in playerarray:
            if x.getName() == character:
                messageManager.addMessage(
                    x.getCharacter() + " moved to " + roomname)
        newLocation = [xcoordinate, ycoordinate]
        x = currentNode.getplayer()
        if x.getCharacter() == character:
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
        return jsonify(
            result="success",
            message="The player was successfuly moved."
        )
    else:
        return jsonify(
            result="error",
            message="The {0} method is not supported".format(request.method)
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
        if validatePlayerTurn(uid) is False:
            return jsonify(
                result="error",
                message="The attempted operation is invalid. Player is out of turn."
            )
        if validatePlayerIsInRoom(uid, room) is False:
            return jsonify(
                result="error",
                message="The attempted operation is invalid. Player must be in the suggestion room."
            )
        playcounter = 0
        playercounter = 0
        playercharacter = ""
        global currentNode, message
        if currentNode.getuid() == uid:
            currplayer = currentNode.getplayer()
            playercharacter = currplayer.getCharacter()
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
            value = playerturnlist.headval
            while value is not None:
                x = value.getplayer()
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
                    for z in weaponsarray:
                        if z.getName() == weapon:
                            z.setLocation([newLocation[0], newLocation[1]])
                    gamestate.setGameBoard(board)
                    message = "[SUGGESTION] {0} suggest that the murder was committed by {1} in the {2} with a {3}".format(
                        playercharacter,
                        character,
                        room,
                        weapon)

                    for i in range(6):
                        messagequeue[i].append(message)
                    suggestionmessage.append(message)
                    subturnplayer = currentNode.getdataval() + 1
                    if subturnplayer > gamestate.setNumOfPlayers():
                        gamestate.setSubturn(1)
                    else:
                        gamestate.setSubturn(subturnplayer)
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
        global currentNode
        global gamestate
        global session
        if currentNode.getuid() == uid:
            currplayer = currentNode.getplayer()
            character = currplayer.getCharacter()
            accusation_set = [room, suspect, weapon]
            message = "[ACCUSATION] {0} has made the accusation that the murder was committed by {1} in the {2} with a {3}".format(
                character,
                suspect,
                room,
                weapon)
            for i in range(6):
                messagequeue[i].append(message)
            if set(accusation_set) == set(casefile):
                message = "[ACCUSATION] {0} has won the game.".format(
                    character)
                for i in range(6):
                    messagequeue[i].append(message)
                gamestate.setGameWon(True)
                gamestate.setGameRunning(False)
                time.sleep(5)
                global rooms
                global suggrooms
                global characters
                global charactersind
                global weapons
                global playerturnlist
                global node1
                global node2
                global node3
                global node4
                global node5
                gamestate = GameState(casefile, 0, 1, False, [[["Rope"], [], ["Lead Pipe"], [], ["Knife"]],
                                                              [[], [], [], [], []],
                                                              [["Wrench"], [], ["Candlestick"],
                                                               [], ["Revolver"]],
                                                              [[], [], [], [], []],
                                                              [[], [], [], [], []]],
                                      False, 0)
                session.setGameState(gamestate)
                rooms = copy.deepcopy(Cards.ROOMS)
                suggrooms = copy.deepcopy(Cards.ROOMS)
                characters = copy.deepcopy(Cards.CHARACTERS)
                charactersind = copy.deepcopy(Cards.CHARACTERS)
                weapons = copy.deepcopy(Cards.WEAPONS)
                playerturnlist = SLinkedList()
                currentNode = Node(99)
                node1 = Node(99)
                node2 = Node(99)
                node3 = Node(99)
                node4 = Node(99)
                node5 = Node(99)
                return jsonify(
                    result="success",
                    gamewon=str(gamestate.getGameWon()),
                    gamerunning=str(gamestate.getGameRunning()),
                    message=message
                )
            else:
                message = "[ACCUSATION] {0} has made a false accusation and can no longer win the game.".format(
                    character)
                for i in range(6):
                    messagequeue[i].append(message)
                    currentNode.setready(False)
                currentNode = currentNode.nextval
                if currentNode is None:
                    currentNode = playerturnlist.headval
                gamestate.setPlayerturn = currentNode.dataval
                return jsonify(
                    result="success",
                    message=message
                )
    else:
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
        global currentNode
        if currentNode.uid == uid:
            currentNode = currentNode.nextval
            if currentNode is None:
                currentNode = playerturnlist.headval
            while currentNode.getready() is not True:
                currentNode = currentNode.nextval
                if currentNode is None:
                    currentNode = playerturnlist.headval
            gamestate.setPlayerturn(currentNode.dataval)
            return jsonify(result="success")
        else:
            return jsonify(result="It is not currently your turn, you are not allowed to end the turn.")


@app.route('/cards', methods=['GET'])
def cards():
    requestJSON = None

    if request.method == 'GET':
        weapons = Cards.WEAPONS
        characters = Cards.CHARACTERS
        rooms = Cards.ROOMS
        imageURLs = Cards.IMAGE_URLS
        return jsonify(json.dumps({'weapons': weapons, 'rooms': rooms, 'characters': characters, 'imageURLs': imageURLs}))


@app.route('/')
def index():
    return f"Welcome to ClueLite.\n Click Play to start the game."


if __name__ == "__main__":
    app.run(debug=True)
