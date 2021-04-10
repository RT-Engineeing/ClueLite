/**
 * Script for managing the UI for the Skeletal implementation.
 * 
 * Use the 'actions' array and 'requiredParameters' dict to define additional actions, this 
 * script will dynamically populate the page with the required dropdown option + input fields
 * to submit a payload for that action. Additional interpretation code will be required for 
 * interpreting them correctly.
 * 
 */

//If you're going to add a new action, add it to this array
let actions = ["signup", "move", "accuse", "suggest"];

let baseUrl = "http://localhost:5000";

let sessionKey = "";


let SESSIONS_ENDPOINT = "Sessions";

let playerName = "";



//Add the required parameters for the actions to this array,
//the selector/input fields will auto populate from this data
let requiredParameters = {
    "signup": ["playername", "character"],
    "move" : ["character", "playername", "x", "y"], //is move really going to need a character/playername field combo?
    "accuse" : ["suspect", "room", "weapon", "character"],
    "suggest" : ["suspect", "suggestor", "room", "weapon"]
}

let endpoints = {
    "movement": "Movement",
    "accuse": "Accusation",
    "suggest": "Suggestion",
    "signup": "signup",
    "session": "TODO",
    "gamestate": "getstate",
    "heartbeat": "TODO"

}



function requestGameState() {
    console.log("requesting game state");
    $.ajax({
        contentType: "application/json; charset=utf-8",
        type: "GET",
        url: baseUrl + "/getstate",
        crossDomain:true,
        success: function(data) {
            console.log("updated state: " + data);
            interpret(JSON.stringify(data));
            return data;
        },
        error: function(data) {
            console.log("whoopsy daisy");
            console.log(data);
        }
    });
}


//Called upon reception of a transmission from the server, interprets our payload
//Note: Currently just interprets the 'submitted' data, since we don't have server connections
function interpret(payload){

    
    var interpretDiv = document.getElementById("interpretDiv");
    var payloadDiv = document.getElementById("payloadDiv");

    clearDiv(interpretDiv);
    clearDiv(payloadDiv);

    displayRawPayload(payload); //Display the raw payload for viewing
    
    var payloadObj = JSON.parse(payload);
   
    var readableInterpretation = getReadableString(payloadObj); //Fetch a human-readable interpretation of the payload

    $("#interpretDiv").append(readableInterpretation);
    // interpretDiv.appendChild(document.createTextNode(readableInterpretation));
}

//Displays the raw JSON contents of the payload
function displayRawPayload(payload){
    var payloadDiv = document.getElementById("payloadDiv");
    var content = document.createElement("pre");
    content.innerHTML = payload;
    payloadDiv.appendChild(content);
}

function displayResponsePayload(payload){
    var responseDiv = document.getElementById("responseDiv");
    responseDiv.innerHTML = "";
    var content = document.createElement("pre");
    
    content.innerHTML = payload;
    responseDiv.appendChild(content);
}


//Generates the 'Submit' button, binds its onclick to submit()
function getSubmitButton() {
    var submitButton = document.createElement('button');
    submitButton.setAttribute('id', 'submit_request');
    submitButton.appendChild(document.createTextNode('Submit'));
    submitButton.setAttribute('onclick', 'submit()');
    submitButton.setAttribute('style', 'margin-top:15px;');

    return submitButton;
}


//Generates a human-readable interpretation of a payload object
function getReadableString(payloadObj){
    // var action = payloadObj["action"];
    // if(action === 'move'){
    //     return getReadableMove(payloadObj);
    // } else if(action === 'accuse'){
    //     return getReadableAccuse(payloadObj);
    // } else if(action === 'suggest'){
    //     return getReadableSuggest(payloadObj);
    // } 
    console.log("beginning interpretation of " + JSON.stringify(payloadObj));

    var player = payloadObj["Player1"];

    var character = player["character"];
    var hand = player["hand"];
    var location = player["location"];
    var name = player["name"];

    var gameboard = payloadObj["gameboard"];

    var gamestatus = payloadObj["gamestatus"];
    var numberofplayers = payloadObj["numberofplayers"];
    var playerturn = payloadObj["playerturn"];

    
    var output = "<b> Players </b> <br /> "

    var playerArray = [];
    var i = 0;
    for(i = 0; i < numberofplayers; i++){
        var key = "Player" + (i + 1);
        console.log("fetching key " + key);
        var currentPlayer = payloadObj[key];
        console.log(JSON.stringify(currentPlayer));
        output += "Number: " + (i + 1) + "<br />";
        output += "Player Name: " + currentPlayer["name"] + "<br />";
        output += "Character: " + currentPlayer["character"] + "<br />";
        output += "Hand: ";
        
        var currentHand = currentPlayer["hand"];
        var j;
        for(j = 0; j < currentHand.length-1; j++){
            output += currentHand[j] + ", ";
        }
        output += currentHand[currentHand.length-1] + "<br />";

        var currentLocation = currentPlayer["location"];
        output += "Player Location: (" + currentLocation[0] + ", " + currentLocation[1] + ")<br />";

        output += "<hr />";
    }

    output += gameboardAsString(gameboard);

    console.log(output);

    return output;

}

function gameboardAsString(gameboard){
    var gameboardLength = gameboard.length;
    var i = 0;
    var output = "";
    for(i = 0; i < gameboardLength; i++){
        for(j = 0; j < gameboard[i].length; j++){
            var entry = gameboard[i][j];
            var s = sum(entry);
            console.log("(" + i + ", " + j + ")" + s);
            output += s + " ";
        }
        output += "<br />";
    }
    return output;
}

function sum(arr){
    var i;
    var sum = 0;

    for(i = 0; i < arr.length; i++){
        sum += arr[i];
    }

    if(sum === 0){
        return "&#129001;";
    }
    if(sum === 99){
        return "&#128997";
    }
    return "&#128100;";
}

//Generates a human-readable interpretation of a move payload
function getReadableMove(payloadObj){
    var player = payloadObj['player'];
    var newX = payloadObj['newX'];
    var newY = payloadObj['newY'];
    return "Move player " + player + " to position (" + newX + ", " + newY + ")";
}

//Generates a human-readable interpretation of an accusation payload
function getReadableAccuse(payloadObj){
    var player = payloadObj['player'];
    var weapon = payloadObj['weapon'];
    var location = payloadObj['room'];
    return "Accuse player " + player + " of using the " + weapon + " in " + location;
}

//Generates a human-readable interpretation of a suggestion payload
function getReadableSuggest(payloadObj){
    var player = payloadObj['player'];
    var weapon = payloadObj['weapon'];
    var location = payloadObj['room'];
   return `Suggest player ${player} of using the ${weapon} in ${location}`;
}

//Clears a div
function clearDiv(div){
    div.innerHTML = "";
}

/** BEGIN UNIVERSAL METHODS **/
function submitPostRequest(transmission, endpoint){

    var sessionDependentRequest = sessionKey !== ""; //indicates if a session key exists. if so, we need to include it in the request
    transmission["sessionKey"] = sessionKey;



    console.log("submitting request "+  JSON.stringify(transmission) + " to endpoint " + endpoint);
    $.ajax({
        contentType: "application/json",
        type: "POST",
        url: baseUrl + "/" + endpoint,
        data: JSON.stringify(transmission),
        crossDomain:true,
        success: function(data) {
            return JSON.parse(data);
            
        },
        error: function(data, error) {
            console.log("error submitting payload: " + JSON.stringify(data));
            console.log(error);
        }
    });
}


/**  BEGIN SESSION FETCH/CREATE SECTION **/

function requestSession(actionType) {

    let transmission = { "action": actionType};

    var sessions = submitPostRequest(transmission, endpoints["session"]);
    if(sessions !== null){
        return sessions; 
    }
}


function joinSession(sessionKey){
    let transmission = {"action": "join",
    "sessionkey": sessionKey};

    var joinStatus = submitPostRequest(transmission, endpoints["session"]);
    return joinStatus;
}

function searchForLobby() {

    var session = requestSession("poll");
    /**
     * As per 09APR2021 meeting, if the server detects no open sessions, it will create one and return the session key.
     * 
     * Discuss with Zach: instead of returning a list of active sessions if they exist, return only one so that we can handle this case seamlessly
     */

    if(session === null){
        console.log("ERROR: NO SESSION KEY RETURNED FROM SERVER");
        return;
    }


    var joinStatus = joinSession(session);

    if(joinStatus === 'Success'){
        // successfully joined, move into lobby screen
    } else {
        // failed to join the session, give some alert to the user
    }


    //workflow for this: 
    // 1. Request a list of open lobbies from the server
    // 2. If response payload contains a session key, do joinGame(sessionKey)
    // 3. Otherwise, submit request to server to create a new game
    //    3a. Response from server here should be a session key for the new game
}
/**  END SESSION FETCH/CREATE SECTION **/

/**  BEGIN LOBBY SECTION **/

function getPlayerList(sessionKey){

    /**
     * TODO: Update transmission payload + sessions endpoint to reflect updated APIs
     */
    let transmission = {
        "action": "lobby_poll",
        "sessionkey": sessionKey
    }

    var playerList = submitPostRequest(tranmission, endpoints["session"]);
    var numPlayers = playerList.length;


    var i;
    var numReady = 0;
    for(i = 0;i < numPlayers; i++){
        /**
         * How will the server package up this data?
         * Is it just a username, or a full player object?
         *
         * Per 09APR2021 meeting, this will just return names + ready state
         */

         //populate the player list with this data

         var currentPlayerData = playerList[i];

         var playerName = currentPlayerData["name"];
         var readyState = currentPlayerData["readyState"];

         if(readyState === true){
            numReady++;
        }

         //fetch the i-th React player list item and update the name + ready state
    }


    var gameCanStart = numPlayers === 6 && numReady === numPlayers;
    // check if host
    if(gameCanStart){
        //activate the start button, allow game to begin
    } else {
        //not all players are ready, keep start button inactive
    }
}


/**
 * 
 * @param {*} oldName - old player name
 * @param {*} newName - new player name
 * @param {*} sessionKey - current session key
 */
function changeUserName(oldName, newName, sessionKey){
    let transmission = {
        "action": "change_name",
        "new_name": newName,
        "source_player": oldName,
        "sessionkey": sessionkey
    }

    var changeResponse = submitPostRequest(tranmission, "WHAT_ENDPOINT_WILL_THIS_BE_DONE_THROUGH?");

    if(changeResponse === 'Success'){
        //name change was a success, update player text
    } else {
        //name change failed (maybe someone else had that name already?)
    }
}

function startGame() {
    let transmission = {}; //what needs to be in here outside of the sessionkey?

    var startResponse = submitPostRequest(tranmission, "START_GAME_ENDPOINT");

    if(startResponse === 'Success'){
        //progress to board screen
    } else {
        //game failed to start.
        console.log(startResponse);
    }
}


/** END LOBBY SECTION  **/

/** BEGIN GAME BOARD SECTION **/

function initGameSequence() {

    //send heartbeat every 5 seconds
    setInterval(sendHeartbeat, 5000);
    setInterval(getGameState, 2000);
    setInterval(pollForGameUpdates, 2000);
}

function sendHeartbeat() {
    let transmission = {};
    var heartbeatResponse = submitPostRequest(tranmission, endpoints["heartbeat"]);
}

function getGameState() {
    let transmission = {};
    var gamestate = submitPostRequest(transmission, endpoints["gamestate"]);

    //do stuff with gamestate
}

function processGamestate(gamestate) {


    var players = gamestate["Players"];

    var i;
    for(i = 0; i < players.length; i++){
        var currentPlayer = players[i];

        var currentPlayerLocation = currentPlayer["location"];
        var currentPlayerX = currentPlayerLocation[0];
        var currentPlayerY = currentPlayerLocation[1];

        //validate that players are at the right position, move if necessary


    }

    var gameboard = gamestate["gameboard"];



    var playerTurn = gamestate["turn"];

    if(playerTurn === playerName){
        //activate react components for this player's turn
    } else {
        //disable react components if necessary
    }
}

function processGameboard(gameboard){
    //TODO: Discuss with Zach any changes to the gameboard format so that we can process it
    var gameboardLength = gameboard.length;
    var i = 0;
    var j = 0;
    var k = 0;
    for(i = 0; i < gameboardLength; i++){
        for(j = 0; j < gameboard[i].length; j++){
            var entry = gameboard[i][j];
            for(k = 0; k < entry.length; k++){
                if(entry[k] !== 0){
                    var playerNum = entry[k];
                    //update react component to have player `playerNum` at location (i,j)
                    //how are weapons handled with this?
                    //possible: gameboard[i][j] is a comma-separated inventory of everything in that room, including weapons + players
                }
            }
        }
    }

}

function move(player, x, y) {
    let transmission = {
        "player": player,
        "x": x,
        "y": y
    }

    var movementResponse = submitPostRequest(transmission, endpoints["movement"]);
}

function suggest(suspect, room, weapon, suggestor){
    let transmission = {
        "suspect": suspect,
        "room": room,
        "weapon": weapon,
        "suggestor": suggestor
    }

    var suggestionResponse = submitPostRequest(transmission, endpoints["suggest"]);

}

function accuse(suspect, room, weapon, accuser){
    let transmission = {
        "suspect": suspect,
        "room": room,
        "weapon": weapon,
        "accuser": accuser
    }

    var accusationResponse = submitPostRequest(transmission, endpoints["accuse"]);
    
    if(accusationResponse === true){
        // game over
    } else {
        // uh oh spaghettio 
    }
}

function provideCard(recipient, card, sender){
    let transmission = {
        "recipient": recipient,
        "card": card,
        "sender": sender
    }

    var cardProvideResposne = submitPostRequest(transmission, "PROVIDE_CARD_SERVICE");
}

/**
 * TODO: Discuss with Zach how they plan on handling the case where a user provides a card.
 * 
 * Should the suggestor poll for cards? 
 */

 function pollForCards(player){
    let transmission = {
        "player": player
    }

    var cardResponse = submitPostRequest(transmission, "POLL_FOR_CARDS_SERVCE");

    if(cardResponse !== "" && cardResponse !== "None"){
        // we got a card back, display it
    } else if(cardResponse === "None") {
        //no cards were given by any players, all players were checked
    } else {
        setTimeout(pollForCards.bind(null, player), 2000);
    }
 }

 function pollForGameUpdates(){
    let transmission = {};

    var gameUpdatesResponse = submitPostRequest(transmission, "GAME_UPDATES_ENDPOINT");

    if(gameUpdatesResponse.length !== 0){
        //add to react game updates section
    } else {
        //no updates
    }
 }





