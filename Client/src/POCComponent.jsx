import React from 'react';
import $ from 'jquery';
import Board from './Board'
//If you're going to add a new action, add it to this array
const actions = ["move", "accuse", "suggest"];

//Add the required parameters for the actions to this array,
//the selector/input fields will auto populate from this data
let requiredParameters = {
    "move": ["player", "newX", "newY"],
    "accuse": ["player", "room", "weapon"],
    "suggest": ["player", "room", "weapon"]
}
export class POCComponent extends React.Component {
    /**
     * Script for managing the UI for the Skeletal implementation.
     * 
     * Use the 'actions' array and 'requiredParameters' dict to define additional actions, this 
     * script will dynamically populate the page with the required dropdown option + input fields
     * to submit a payload for that action. Additional interpretation code will be required for 
     * interpreting them correctly.
     * 
     */

    constructor(props) {
        super(props);
        this.submit = this.submit.bind(this);
        this.getInputs = this.getInputs.bind(this);
        this.interpret = this.interpret.bind(this);
        this.displayRawPayload = this.displayRawPayload.bind(this);
        this.getSubmitButton = this.getSubmitButton.bind(this);
        this.getReadableString = this.getReadableString.bind(this);
        this.getReadableMove = this.getReadableMove.bind(this);
        this.getReadableAccuse = this.getReadableAccuse.bind(this);
        this.getReadableSuggest = this.getReadableSuggest.bind(this);
        this.clearDiv = this.clearDiv.bind(this);
        this.getDropdown = this.getDropdown.bind(this);
        this.getSelector = this.getSelector.bind(this);

        this.state = {
            x: 0,
            y: 0
        }
    }

    componentDidMount() {
        console.log(this.getSelector);
        var selector = this.getSelector();
        var publishDiv = document.getElementById('publishDiv');
        var parametersDiv = document.getElementById("parametersDiv");
        document.getElementById("publishDiv").insertBefore(selector, parametersDiv);
        this.getInputs("move");
    }

    //Generates input fields for the parameters for a given action, adds it to screen
    getInputs(action) {
        if (action.length === 0) {
            return;
        }
        var params = requiredParameters[action];
        var numParams = params.length;
        var parametersDiv = document.getElementById("parametersDiv");
        this.clearDiv(parametersDiv);

        for (var i = 0; i < numParams; i++) {
            var paramTextBox = document.createElement('input');
            paramTextBox.type = 'text';
            paramTextBox.setAttribute('name', params[i] + "_input");
            paramTextBox.setAttribute('placeholder', params[i]);
            paramTextBox.setAttribute('style', 'margin-top:15px;');
            parametersDiv.appendChild(paramTextBox);
            parametersDiv.appendChild(document.createElement('br'));

        }
        var submitButton = this.getSubmitButton();
        parametersDiv.appendChild(submitButton);

    }

    //Called when submit button is pressed, packages data into JSON and transmits to server
    submit() {
        var actionName = $("#action_selector").val();
        var payload = { 'action': actionName };
        $('input[type=text]').each(function () {
            var paramName = $(this).attr("placeholder"); //paramater names are the placeholder attributes for the inputs, we can just pull those for the key
            var paramValue = $(this).val();
            payload[paramName] = paramValue;
        });

        console.log(payload);

        console.log('transmission not yet implemented');

        //For now, have the interpreter process the submitted payload until we can actually transmit
        this.interpret(JSON.stringify(payload));
    }


    //Called upon reception of a transmission from the server, interprets our payload
    //Note: Currently just interprets the 'submitted' data, since we don't have server connections
    interpret(payload) {
        var interpretDiv = document.getElementById("interpretDiv");
        var payloadDiv = document.getElementById("payloadDiv");

        this.clearDiv(interpretDiv);
        this.clearDiv(payloadDiv);

        this.displayRawPayload(payload); //Display the raw payload for viewing

        var payloadObj = JSON.parse(payload);

        var readableInterpretation = this.getReadableString(payloadObj); //Fetch a human-readable interpretation of the payload
        interpretDiv.appendChild(document.createTextNode(readableInterpretation));
    }

    //Displays the raw JSON contents of the payload
    displayRawPayload(payload) {
        var payloadDiv = document.getElementById("payloadDiv");
        var content = document.createElement("pre");
        content.innerHTML = payload;
        payloadDiv.appendChild(content);
    }

    //Generates the 'Submit' button, binds its onclick to submit()
    getSubmitButton() {
        var submitButton = document.createElement('button');
        submitButton.setAttribute('id', 'submit_request');
        submitButton.appendChild(document.createTextNode('Submit'));
        submitButton.addEventListener('click', this.submit);
        submitButton.setAttribute('style', 'margin-top:15px;');

        return submitButton;
    }


    //Generates a human-readable interpretation of a payload object
    getReadableString(payloadObj) {
        var action = payloadObj["action"];
        if (action === 'move') {
            return this.getReadableMove(payloadObj);
        } else if (action === 'accuse') {
            return this.getReadableAccuse(payloadObj);
        } else if (action === 'suggest') {
            return this.getReadableSuggest(payloadObj);
        }
        return 'Unsupported action.';

    }

    //Generates a human-readable interpretation of a move payload
    getReadableMove(payloadObj) {
        var player = payloadObj['player'];
        var newX = payloadObj['newX'];
        var newY = payloadObj['newY'];
        this.setState({ x: newX, y: newY });
        console.log(this.state);
        this.render()

        return "Move player " + player + " to position (" + newX + ", " + newY + ")";
    }

    //Generates a human-readable interpretation of an accusation payload
    getReadableAccuse(payloadObj) {
        var player = payloadObj['player'];
        var weapon = payloadObj['weapon'];
        var location = payloadObj['room'];
        return "Accuse player " + player + " of using the " + weapon + " in " + location;
    }

    //Generates a human-readable interpretation of a suggestion payload
    getReadableSuggest(payloadObj) {
        var player = payloadObj['player'];
        var weapon = payloadObj['weapon'];
        var location = payloadObj['room'];
        return `Suggest player ${player} of using the ${weapon} in ${location}`;
    }

    //Clears a div
    clearDiv(div) {
        div.innerHTML = "";
    }

    //Generates a bootstrap dropdown for selecting an action to submit, binds the onchange to getInputs
    //Note: This is not currently used, but if we want to make the UI look a bit nicer it might be a good route to go down.
    getDropdown() {
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

        for (var i = 0; i < numActions; i++) {
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
    getSelector() {
        var selector = document.createElement('select');
        selector.setAttribute('id', 'action_selector');
        selector.setAttribute('onchange', 'getInputs(this.options[this.selectedIndex].value)');
        var option;
        var numActions = actions.length;

        for (var i = 0; i < numActions; i++) {
            option = document.createElement('option');
            option.setAttribute('value', actions[i]);
            option.appendChild(document.createTextNode(actions[i]));
            selector.appendChild(option);
        }
        return selector;
    }



    render() {
        return (
            <React.Fragment>
                <h2> Client Message Publish Proof of Architecture </h2>
                <p> This utility generates a game payload that conforms to the mutually shared server-client payload format, and transmits it to the server for interpretation. <br />
    Select an action from the drop-down menu, and fill in the input fields that appear. Afterwards, press submit and the message will be sent to the server.
</p>
                <div id="publishDiv">
                    <div id="parametersDiv">
                    </div>
                </div>

                <hr />

                <div id="receiveDiv">
                    <h2> Client Message Reception Proof of Architecture </h2>
                    <p> This utility receives game payload transmission from the server, and interprets the contents of the payload. The first text region contains the <br />
        raw JSON package that the server sent, while the second text section displays the client's interpretation of the payload's contents.

    </p>

                    <h3> Raw Payload Contents </h3>
                    <div id="payloadDiv">

                    </div>
                    <h3> Payload Interpretation </h3>
                    <div id="interpretDiv">

                    </div>
                    <div>
                        <Board x={this.state.x} y={this.state.y} />
                    </div>
                </div>
            </React.Fragment>
        )
    }
}
export default POCComponent;