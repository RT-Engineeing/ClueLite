import './Game.css'
import React from 'react';
import Card from 'react-bootstrap/Card'
import Button from 'react-bootstrap/Button'
import GameBoard from '../GameBoard/GameBoard';
import Modal from 'react-bootstrap/Modal'
import Carousel from 'react-bootstrap/Carousel'
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

const tmpGameBoard = [[[1], [2], [3], [4], [5]], [[6], [7], [8],], [[9], [10], [11], [12], [13]], [[14], [15], [16],], [[17], [18], [19], [20], [21]]];
let characters = [];
let weapons = [];
let rooms = [];

export class Game extends React.Component {

    constructor(props) {
        super(props);
        characters = props.location.state.characters;
        rooms = props.location.state.rooms;
        weapons = props.location.state.weapons;

        this.state = {
            polling: false,
            showSuggestModal: false,
            showAccusationModal: false,
            showGameWonModal: false,
            showGameLostModal: false,
            showSecondarySuggestionModal: false,
            cards: ["1", "2", "3", "4", "5"],
            uuid: props.location.state.uuid,
            playerName: props.location.state.playerName,
            charactername: props.location.state.charactername,
            sessionkey: props.location.state.sessionkey,
            accusationSelected: {
                suspect: characters[0],
                weapon: weapons[0],
                room: rooms[0]
            },
            suggestionSelected: {
                suspect: characters[0],
                weapon: weapons[0],
                room: rooms[0]
            },
            suggestionDisproofSelected: {
                card: characters[0]
            },
            currentGameBoard: tmpGameBoard,
            turnIndicator: " ",
            pendingDisproof: true,

            alertBuffer: ["", "", "", "", ""],
            alertNum: 0
        }

        this.makeAccusation = this.makeAccusation.bind(this);
        this.makeSuggestion = this.makeSuggestion.bind(this);
        this.submitCardToSuggestion = this.submitCardToSuggestion.bind(this);
    }


    async pollGameState() {
        // Converts the 5,5,5,5,5 gameboard returned by the server to a 5,3,5,3,5 game board.
        function cvt_5x5_gameboard(gameBoard) {
            // Don't modify this function.
            gameBoard[1].splice(3, 1);
            gameBoard[1].splice(1, 1);
            gameBoard[3].splice(3, 1);
            gameBoard[3].splice(1, 1);
            return gameBoard
        }

        const response = await axios.post("http://localhost:5000/getstate",
            {
                uid: this.state.uuid
            });

        const gamestate = response.data;
        this.processAlerts(gamestate)
        const playerdata = gamestate[this.state.playerName];
        const playerHand = playerdata["hand"];
        const newGameboard = gamestate["gameboard"];
        const playerTurn = "Player" + (gamestate["playerturn"]);

        const myTurn = playerTurn === this.state.playerName;
        if (myTurn && this.state.showGameLostModal) {
            this.endTurn();
        }
        const turnString = playerTurn + "'s " + (playerTurn === this.state.playerName ? " (You) " : "") + " Turn";

        if (!response.data.gamerunning && !this.state.showGameWonModal) {
            this.setState({ caseFile: response.data.casefile });
            this.setState({ showGameLostModal: true });
        }

        this.setState({
            cards: playerHand,
            currentGameBoard: cvt_5x5_gameboard(newGameboard),
            turnIndicator: turnString
        });

        const messages = gamestate["messages"];
        if (messages.length > 0) {
            console.log("message: " + messages[0]);
            //
            // playersList.forEach(player => {
            //     let readyStatus = readyPlayers.includes(player) ? true : false;
            //     lobbyData.push([player, readyStatus]);
            // });



            messages.forEach(message => {
                console.log("fetched message: " + JSON.stringify(message));
                if (JSON.stringify(message).includes("[SUGGESTION]")) {
                    //suggestion message
                    this.showSecondarySuggestionModal();
                } else if (JSON.stringify(message).includes("[ACCUSATION]")) {
                    //accusation message

                } else {
                    //card message
                    if (this.state.pendingDisproof) {
                        alert("You received the card: " + JSON.stringify(message) + " to disprove your suggestion.");
                        this.state.pendingDisproof = false;
                    }
                }
            });
        }
    }

    async submitCardToSuggestion() {
        //for disproving

        console.log("submitting disproof " + this.state.suggestionDisproof);
        const response = await axios.post("http://localhost:5000/suggestionresponse",
            {
                childSuggestion: this.state.suggestionDisproofSelected
            });
        this.hideSecondarySuggestionModal()
        console.log("response to disproof: " + response.data);

    }


    async endTurn() {
        const response = await axios.post("http://localhost:5000/endturn",
            {
                uid: this.state.uuid
            });
    }




    async makeSuggestion() {
        const response = await axios.post("http://localhost:5000/suggestion",
            {
                uid: this.state.uuid,
                character: this.state.charactername,
                weapon: this.state.suggestionSelected.weapon,
                room: this.state.suggestionSelected.room,
                suspect: this.state.suggestionSelected.suspect
            });
        this.state.pendingDisproof = true;
        console.log(response.data);
    }

    async makeAccusation() {
        const response = await axios.post("http://localhost:5000/accusation",
            {
                uid: this.state.uuid,
                character: this.state.charactername,
                weapon: this.state.accusationSelected.weapon,
                room: this.state.accusationSelected.room,
                suspect: this.state.accusationSelected.suspect
            });
        if (response.data.gamewon) {
            this.setState({ showGameWonModal: true });
        } else {
            this.setState({ showGameLostModal: true });
        }
        this.setState({ showAccusationModal: false })
    }

    processAlerts(gamestate){
        const alerts = gamestate["alerts"];
        if(alerts.length !== 0){
            console.log("found new alerts " + JSON.stringify(alerts));
            var i;
            for(i = 0; i < alerts.length; i++){
                this.state.alertBuffer[this.state.alertNum] = alerts[i];
                this.state.alertNum = (this.state.alertNum == 4 ? 0 : this.state.alertNum + 1);
            }
        }
    }


    componentDidMount() {
        this.interval = setInterval(() => this.pollGameState(), 1000);
    }

    componentWillUnmount() {
        clearInterval(this.interval);
    }


    getGameState = () => {
        const currGameBoard = this.state.currentGameBoard;
        return {
            gameBoard: currGameBoard
        }
    }

    showSecondarySuggestionModal = () => {
        this.setState({ showSecondarySuggestionModal: true });
    }

    hideSecondarySuggestionModal = () => {
        this.setState({ showSecondarySuggestionModal: false });
    }

    render() {
        const showSuggestionModal = () => {
            this.setState({ showSuggestModal: true });
        }
        const hideSuggestionModal = () => {
            this.setState({ showSuggestModal: false });
        }
        const hideSecondarySuggestionModal = () => {
            this.setState({ showSecondarySuggestionModal: false });
        }
        const showAccusationModal = () => {
            this.setState({ showAccusationModal: true });
        }
        const hideAccusationModal = () => {
            this.setState({ showAccusationModal: false });
        }
        const hideGameLostModal = () => {
            this.setState({ showGameLostModal: false });
        }
        const hideGameWonModal = () => {
            this.setState({ showGameWonModal: false });
        }
        const handleAccusationSuspectSelect = (idx) => {
            this.setState({ accusationSelected: { ...this.state.accusationSelected, suspect: characters[idx] } })
        }
        const handleAccusationWeaponSelect = (idx) => {
            this.setState({ accusationSelected: { ...this.state.accusationSelected, weapon: weapons[idx] } })
        }
        const handleAccusationRoomSelect = (idx) => {
            this.setState({ accusationSelected: { ...this.state.accusationSelected, room: rooms[idx] } })
        }

        const handleSuggestionSuspectSelect = (idx) => {
            this.setState({ suggestionSelected: { ...this.state.suggestionSelected, suspect: characters[idx] } })
        }
        const handleSuggestionWeaponSelect = (idx) => {
            this.setState({ suggestionSelected: { ...this.state.suggestionSelected, weapon: weapons[idx] } })
        }
        const handleSuggestionRoomSelect = (idx) => {
            this.setState({ suggestionSelected: { ...this.state.suggestionSelected, room: rooms[idx] } })
        }

        const handleSuggestionDisproofSelect = (idx) => {
            this.setState({ suggestDisproofSelected: this.state.cards[idx] })
        }

        const endTurn = () => {
            this.endTurn();
        }

        const suggestionModal = (
            <Modal
                show={this.state.showSuggestModal}
                onHide={hideSuggestionModal}
                backdrop="static"
                keyboard={false}
                centered
                size="lg"
                contentClassName="suggestionModal"
            >
                <Modal.Header className="modalHeader">
                    <Modal.Title>Make a Suggestion</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Carousel interval={null} indicators={false} onSelect={handleSuggestionSuspectSelect}>
                        {characters.map((character, idx) =>
                        (
                            <Carousel.Item className="carouselItem" id={idx} >
                                {character}
                            </Carousel.Item>
                        ))}
                    </Carousel>
                    <Carousel interval={null} indicators={false} onSelect={handleSuggestionWeaponSelect}>
                        {weapons.map((weapon, idx) =>
                        (
                            <Carousel.Item className="carouselItem" id={idx} >
                                {weapon}
                            </Carousel.Item>
                        ))}
                    </Carousel>
                    <Carousel interval={null} indicators={false} onSelect={handleSuggestionRoomSelect}>
                        {rooms.map((room, idx) =>
                        (
                            <Carousel.Item className="carouselItem" id={idx} >
                                {room}
                            </Carousel.Item>
                        ))}
                    </Carousel>
                </Modal.Body>
                <Modal.Footer className="modalFooterButtons">
                    <Button variant="secondary" onClick={hideSuggestionModal}>
                        Cancel
                     </Button>
                    <Button variant="primary" onClick={this.makeSuggestion}>
                        Suggest
                    </Button>
                </Modal.Footer>
            </Modal >
        );

        const gameWonModal = (
            <Modal
                show={this.state.showGameWonModal}
                onHide={hideGameWonModal}
                backdrop="static"
                keyboard={false}
                centered
                size="lg"
                contentClassName="gameWonModal"
            ><Modal.Header className="modalHeader">
                    <Modal.Title>
                        <span className="finalText"> You Win!</span>
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                </Modal.Body>
            </Modal >
        );
        const gameLostModal = (
            <Modal
                show={this.state.showGameLostModal}
                onHide={hideGameLostModal}
                backdrop="static"
                keyboard={false}
                centered
                size="lg"
                contentClassName="gameLostModal"
            ><Modal.Header className="modalHeader">
                    <Modal.Title>
                        <span className="finalText"> You Lose</span></Modal.Title>
                </Modal.Header>
                <Modal.Body className="caseFile">
                    <span >
                        {this.state.caseFile ?
                            `The murder was committed by ${this.state.caseFile[1]} with the ${this.state.caseFile[2]} in the ${this.state.caseFile[0]}` : ""}
                    </span>
                </Modal.Body>
            </Modal >
        );

        const accusationModal = (
            <Modal
                show={this.state.showAccusationModal}
                onHide={hideAccusationModal}
                backdrop="static"
                keyboard={false}
                centered
                size="lg"
                contentClassName="accusationModal"
            >
                <Modal.Header className="modalHeader">
                    <Modal.Title>Make an Accusation</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Carousel interval={null} indicators={false} onSelect={handleAccusationSuspectSelect}>
                        {characters.map((character, idx) =>
                        (
                            <Carousel.Item className="carouselItem" id={idx}>
                                {character}
                            </Carousel.Item>
                        ))}
                    </Carousel>
                    <Carousel interval={null} indicators={false} onSelect={handleAccusationWeaponSelect}>
                        {weapons.map((weapon, idx) =>
                        (
                            <Carousel.Item className="carouselItem" id={idx} >
                                {weapon}
                            </Carousel.Item>
                        ))}
                    </Carousel>
                    <Carousel interval={null} indicators={false} onSelect={handleAccusationRoomSelect}>
                        {rooms.map((room, idx) =>
                        (
                            <Carousel.Item className="carouselItem" id={idx} >
                                {room}
                            </Carousel.Item>
                        ))}
                    </Carousel>
                </Modal.Body>
                <Modal.Footer className="modalFooterButtons">
                    <Button variant="secondary" onClick={hideAccusationModal}>
                        Cancel
                     </Button>
                    <Button variant="primary" onClick={this.makeAccusation}>
                        Accuse
                    </Button>
                </Modal.Footer>
            </Modal >
        );

        const secondarySuggestionModal = (
            <Modal
                show={this.state.showSecondarySuggestionModal}
                onHide={hideSecondarySuggestionModal}
                backdrop="static"
                keyboard={false}
                centered
                size="lg"
                contentClassName="secondarySuggestionModal"
            >
                <Modal.Header className="modalHeader">
                    <Modal.Title>Respond to the Suggestion</Modal.Title>
                </Modal.Header>
                <Modal.Body>

                    <Carousel interval={null} indicators={false} onSelect={handleSuggestionDisproofSelect}>
                        {this.state.cards.map((card, idx) =>
                        (
                            <Carousel.Item className="carouselItem" id={idx}>
                                {card}
                            </Carousel.Item>
                        ))}
                    </Carousel>
                    <div className="secondarySuggestionInstructions" >
                        Choose a card to disprove the suggestion
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooterButtons">
                    <Button variant="primary" onClick={this.submitCardToSuggestion}>
                        Show Card
                    </Button>
                </Modal.Footer>
            </Modal >
        );

        const gameBoard = (
            <Card id="game">
                { <GameBoard rooms={rooms} gameState={this.getGameState} charactername={this.state.charactername} playerName={this.state.playerName} />}
            </Card >
        )

        const updatesContainer = (
            <div className="row">
                < div className="col d-flex justify-content-center" >
                    <Card id="updatesContainer">
                        <Card.Header className="justify-content-center d-flex" style={{ width: "100%" }}>Game Updates</Card.Header>
                        <span>
                        {
                            this.state.alertBuffer.map((alert, idx) => (
                            <div key={idx}>
                                [{alert}]
                            </div>
                            ))
                    }
                </span>
                    </Card >
                </div >
            </div >
        )

        const cards = (
            <div id="cards" className="row">
                <div className="col d-flex justify-content-center">
                    <div>
                        {suggestionModal}
                        {accusationModal}
                        {gameWonModal}
                        {gameLostModal}
                        {secondarySuggestionModal}
                    </div>
                    <div className="container">
                        <h3 id="cardsHeader"> Your Hand ({this.state.charactername}):</h3>
                        <div className="cardRow row">
                            <div className="cardCol col" align="right">
                                <Card className="playerCard" align="center">
                                    {this.state.cards[0]}
                                </Card>
                            </div>
                            <div className="cardCol col" align="center">
                                <Card className="playerCard" align="center">
                                    {this.state.cards[1]}
                                </Card>
                            </div>
                            <div className="cardCol col" align="left">
                                <Card className="playerCard" align="center">
                                    {this.state.cards[2]}
                                </Card>
                            </div>
                        </div>
                        <div className="cardRow row">
                            <div className="cardCol col" align="right">
                                <Card className="playerCard" align="center">
                                    {this.state.cards[3]}
                                </Card>
                            </div>
                            <div className="cardCol col" align="left">
                                <Card className="playerCard" align="center">
                                    {this.state.cards[4]}
                                </Card>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );

        const accuseSuggestEndTurn = (
            <div id="accuseSuggest" className="row">
                <div id="suggestButton" className="col d-flex justify-content-center">
                    <Button className="actionButton"
                        onClick={showSuggestionModal}>Suggest</Button>
                </div>
                <div id="accuseButton" className="col d-flex justify-content-center">
                    <Button className="actionButton"
                        onClick={showAccusationModal}>Accuse</Button>
                </div>

                {/* <div id="suggestButton2" className="col d-flex justify-content-center">
                    <Button className="actionButton"
                        onClick={showSecondarySuggestionModal}>Suggestion (2)</Button>
                </div> */}


                <div id="endTurnButton" className="col d-flex justify-content-center">
                    <Button className="actionButton"
                        onClick={endTurn}
                    >
                        End Turn
                    </Button>
                </div>
            </div>
        );

        return (
            <div className="d-flex justify-content-center" style={{ minWidth: '1800px' }}>
                <div id="gamePageContainer">
                    <div className="row">
                        <div className="col-md-5" >
                            <h3 className="turnIndicator"> {this.state.turnIndicator} </h3>
                            {gameBoard}
                        </div>
                        <div className="col-md-5" style={{ paddingTop: "50px" }}>
                            <div className="container">
                                {updatesContainer}
                                {cards}
                                {accuseSuggestEndTurn}
                            </div >
                        </div >
                    </div >
                </div >
            </div >
        )
    }
}
export default Game;