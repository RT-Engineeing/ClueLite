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

//Add the required parameters for the actions to this array,
//the selector/input fields will auto populate from this data
let requiredParameters = {
    "signup": ["playername", "character"],
    "move" : ["character", "playername", "x", "y"],
    "accuse" : ["suspect", "room", "weapon", "character"],
    "suggest" : ["suspect", "x", "y", "room", "weapon", "character"]
}

//Generates input fields for the parameters for a given action, adds it to screen
function getInputs(action) {
    if(action.length == 0){
        return;
    }
    var params = requiredParameters[action];
    var numParams = params.length;
    var parametersDiv = document.getElementById("parametersDiv");
    clearDiv(parametersDiv);

    for(var i = 0; i < numParams; i++){
        var paramTextBox = document.createElement('input');
        paramTextBox.type = 'text';
        paramTextBox.setAttribute('name', params[i] + "_input");
        paramTextBox.setAttribute('placeholder', params[i]);
        paramTextBox.setAttribute('style', 'margin-top:15px;');
        parametersDiv.appendChild(paramTextBox);
        parametersDiv.appendChild(document.createElement('br'));
        
    }
    var submitButton = getSubmitButton();
    parametersDiv.appendChild(submitButton);

}

//Called when submit button is pressed, packages data into JSON and transmits to server
function submit() {
    var actionName = $("#action_selector").val();
    let toTransmit = {};
    
    $('input[type=text]').each(function() {
        console.log("found input method");
        var paramName = $(this).attr("placeholder"); //paramater names are the placeholder attributes for the inputs, we can just pull those for the key
        var paramValue = $(this).val();
        toTransmit[paramName] = paramValue;
        console.log("set payload value " + paramName + " as " + paramValue);
        console.log("current payload: " + toTransmit);
    });

    console.log("movement payload: " + toTransmit);

    if(actionName === "move"){
        submitRequest(toTransmit, "Movement");
    } else if(actionName === "accuse"){
        submitRequest(toTransmit, "Accusation");
    } else if(actionName === "suggest") {
        submitRequest(toTransmit, "Suggestion");
    } else if(actionName === "signup"){
        submitRequest(toTransmit, "signup");
    }


    

//   console.log(JSON.parse(updatedGamestate));

    //For now, have the interpreter process the submitted payload until we can actually transmit
   // interpret(JSON.stringify(payload));
}

function submitRequest(transmission, endpoint){

    console.log("submitting request "+  JSON.stringify(transmission) + " to endpoint " + endpoint);
    $.ajax({
        contentType: "application/json",
        type: "POST",
        url: baseUrl + "/" + endpoint,
        data: JSON.stringify(transmission),
        crossDomain:true,
        success: function(data) {
            console.log("payload submitted successfully");
            displayResponsePayload(JSON.stringify(data));
            console.log(data);
            requestGameState();
            
        },
        error: function(data, error) {
            console.log("error submitting payload: " + JSON.stringify(data));
            console.log(error);
        }
    });
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

//Generates a bootstrap dropdown for selecting an action to submit, binds the onchange to getInputs
//Note: This is not currently used, but if we want to make the UI look a bit nicer it might be a good route to go down.
function getDropdown() {
    var dropdown = document.createElement('div');
    dropdown.setAttribute('class', 'dropdown');

    var button = document.createElement('button');
    button.setAttribute('class', 'btn btn-secondary dropdown-toggle');
    button.setAttribute('type', 'button');
    button.setAttribute('id', 'dropdownMenuButton');
    button.setAttribute('data-toggle', 'dropdown');
    button.setAttribute('aria-haspopup', 'true');
    button.setAttribute('aria-expanded', 'false');
    button.appendChild(document.createTextNode('Actions Menu'));

    dropdown.appendChild(button);

    var menu = document.createElement('div');
    menu.setAttribute('class', 'dropdown-menu');
    menu.setAttribute('aria-labelledby', 'dropdownMenuButton');
    
    var option;
    var numActions = actions.length;

    for(var i = 0; i < numActions; i++){
        option = document.createElement('a');
        option.setAttribute('class', 'dropdown-item');
        option.setAttribute('href', '#');
        option.appendChild(document.createTextNode(actions[i]));
        menu.appendChild(option);
    }

    dropdown.appendChild(menu);

    return dropdown;
}


//Generates an HTML select element and populates it with the actions defined in the 'actions' array
function getSelector() {
    var selector = document.createElement('select');
    selector.setAttribute('id', 'action_selector');
    selector.setAttribute('onchange', 'getInputs(this.options[this.selectedIndex].value)');
    var option;
    var numActions = actions.length;

    for(var i = 0; i < numActions; i++){
        option = document.createElement('option');
        option.setAttribute('value', actions[i]);
        option.appendChild(document.createTextNode(actions[i]));
        selector.appendChild(option);
    }
    return selector;
}

