from State import GameState
from Player import Players
from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/getstate', methods=['GET'])
def hello():
    #created a bs gamestate for now
    player1 = Players("tim", "colmustard", "ballroom" , "knife")
    player2 = Players("sam", "profproton", "library", "gun")
    gamestate = GameState(2, player1, player2, None, None, None, None, 0, False, [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]] )
    return jsonify({'numberofplayers': gamestate.getNumOfPlayers(), 'Player1': {'name': gamestate.getPlayer1().getName(), 'character': gamestate.getPlayer1().getCharacter(), 'location': gamestate.getPlayer1().getLocation(), 'weapon': gamestate.getPlayer1().getWeapon()}, 'Player2': {'name': gamestate.getPlayer2().getName(), 'character': gamestate.getPlayer2().getCharacter(), 'location': gamestate.getPlayer2().getLocation(), 'weapon': gamestate.getPlayer2().getWeapon()}, 'playerturn': gamestate.getPlayerturn(), 'gamestatus': gamestate.getGameWon(), 'gameboard': gamestate.getGameBoard()})

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