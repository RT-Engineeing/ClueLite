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


let SESSIONS_ENDPOINT = "Sessions";


//Add the required parameters for the actions to this array,
//the selector/input fields will auto populate from this data
let requiredParameters = {
    "signup": ["playername", "character"],
    "move" : ["character", "playername", "x", "y"],
    "accuse" : ["suspect", "room", "weapon", "character"],
    "suggest" : ["suspect", "x", "y", "room", "weapon", "character"]
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
function submitRequest(transmission, endpoint){

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

function requestSessions(actionType) {

    let transmission = { "action": actionType};

    var sessions = submitRequest(transmission, SESSIONS_ENDPOINT);
    if(sessions !== null){
        return sessions; 
    }
}


function joinSession(sessionKey){
    let transmission = {"action": "join",
    "sessionkey": sessionKey};

    var joinStatus = submitRequest(transmission, SESSIONS_ENDPOINT);
    return joinStatus;
}

function searchForLobby() {

    var openSessions = requestSessions("poll");
    var sessionToJoin = "";
    if(openSessions.length == 0){
        sessionToJoin = requestSessions("create");
    } else {
        sessionToJoin = openSessions[0];
    }

    var joinStatus = joinSession(sessionToJoin);

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
    let transmission = {
        "action": "lobby_poll",
        "sessionkey": sessionKey
    }

    var playerList = submitRequest(tranmission, SESSIONS_ENDPOINT);
    var numPlayers = playerList.length;

    var gameCanStart = numPlayers === 6;

    var i;
    for(i = 0;i < numPlayers; i++){
        /**
         * How will the server package up this data?
         * Is it just a username, or a full player object?
         */

         //populate the player list with this data

    }


    // check if host
    if(gameCanStart){
        //activate the start button, allow game to begin
    }
}

function changeUserName(oldName, newName, sessionKey){
    let transmission = {
        "action": "change_name",
        "new_name": newName,
        "source_player": oldName,
        "sessionkey": sessionkey
    }

    var changeResponse = submitRequest(tranmission, "WHAT_ENDPOINT_WILL_THIS_BE_DONE_THROUGH?");

    if(changeResponse === 'Success'){
        //name change was a success, update player text
    } else {
        //name change failed (maybe someone else had that name already?)
    }
}

