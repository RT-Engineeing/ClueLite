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

for i in range(6):
    playername = "Player" + str(i)
    character = random.choice(characdeck)
    while (character in selectedChars):
        character = random.choice(characdeck)
    selectedChars.append(character)
    hand = []
    location = []
    for i in range(3):
        random.shuffle(totaldeck)
        hand.append(totaldeck[0])
        del totaldeck[0]
    if (character == characters[0]):
        location = [0, 3]
    if (character == characters[1]):
        location = [4, 3]
    if (character == characters[2]):
        location = [3, 0]
    if (character == characters[3]):
        location = [1, 0]
    if (character == characters[4]):
        location = [4, 1]
    if (character == characters[5]):
        location = [1, 4]
    player = Players(playername, character, hand, location)
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
        sessionstate.isSessionFull(True)
    board = gamestate.getGameBoard()
    board[player.getLocation()[0]][player.getLocation()[1]][0] = len(playerarray)
    gamestate.setGameBoard(board)
    return jsonify({"result": "success"})