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
let actions = ["move", "accuse", "suggest"];

//Add the required parameters for the actions to this array,
//the selector/input fields will auto populate from this data
let requiredParameters = {
    "move" : ["player", "newX", "newY"],
    "accuse" : ["player", "room", "weapon"],
    "suggest" : ["player", "room", "weapon"]
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
    var payload = {'action' : actionName};
    $('input[type=text]').each(function() {
        var paramName = $(this).attr("placeholder"); //paramater names are the placeholder attributes for the inputs, we can just pull those for the key
        var paramValue = $(this).val();
        payload[paramName] = paramValue;
    });

    console.log(payload);

    console.log('transmission not yet implemented');

    //For now, have the interpreter process the submitted payload until we can actually transmit
    interpret(JSON.stringify(payload));
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
    interpretDiv.appendChild(document.createTextNode(readableInterpretation));
}

//Displays the raw JSON contents of the payload
function displayRawPayload(payload){
    var payloadDiv = document.getElementById("payloadDiv");
    var content = document.createElement("pre");
    content.innerHTML = payload;
    payloadDiv.appendChild(content);
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
    var action = payloadObj["action"];
    if(action === 'move'){
        return getReadableMove(payloadObj);
    } else if(action === 'accuse'){
        return getReadableAccuse(payloadObj);
    } else if(action === 'suggest'){
        return getReadableSuggest(payloadObj);
    } 
    return 'Unsupported action.';

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
    var location = payloadObj['location'];
    return "Accuse player " + player + " of using the " + weapon + " in " + location;
}

//Generates a human-readable interpretation of a suggestion payload
function getReadableSuggest(payloadObj){
    var player = payloadObj['player'];
    var weapon = payloadObj['weapon'];
    var location = payloadObj['location'];
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