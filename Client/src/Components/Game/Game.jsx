import './Game.css'
import React from 'react';
import Card from 'react-bootstrap/Card'
import Button from 'react-bootstrap/Button'
import GameBoard from '../GameBoard/GameBoard';
import Modal from 'react-bootstrap/Modal'
import Carousel from 'react-bootstrap/Carousel'
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import { characters, weapons, rooms, cardImages } from '../../Cards/Cards';

const TMP_PLAYER_CARDS = [
    "exodiaRightArm", "exodiaBody", "exodiaLeftArm", "exodiaRightLeg", "exodiaLeftLeg"
];

export class Game extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            polling: false,
            showSuggestModal: false,
            showAccusationModal: false,
            showSecondarySuggestionModal: false,
            cards: ["1", "2", "3", "4", "5"],
            currentGameBoard: [
                [
                    [
                        1
                    ],
                    [
                        2
                    ],
                    [
                        3
                    ],
                    [
                        4
                    ],
                    [
                        5
                    ]
                ],
                [
                    [
                        6
                    ],
                    [
                        7
                    ],
                    [
                        8
                    ],
                ],
                [
                    [
                        9
                    ],
                    [
                        10
                    ],
                    [
                        11
                    ],
                    [
                        12
                    ],
                    [
                        13
                    ]
                ],
                [
                    [
                        14
                    ],
                    [
                        15
                    ],
                    [
                        16
                    ],
                ],
                [
                    [
                        17
                    ],
                    [
                        18
                    ],
                    [
                        19
                    ],
                    [
                        20
                    ],
                    [
                        21
                    ]
                ]
            ]
        }
    }


    async pollGameState() {
        
        const response = await axios.get("http://localhost:5000/getstate");

        const gamestate = response.data;
        const player1 = gamestate["Player1"];
        const playerHand = player1["hand"][0];
        const oldboard = this.state.currentGameBoard;
        this.setState({ cards: playerHand });
        this.setState({ currentGameBoard: gamestate["gameboard"] });

        if (oldboard !== this.state.currentGameBoard) {
            this.render();
        }
    }

    processGameState(gamestate) {
        console.log(gamestate);
    }


    componentDidMount() {
        this.interval = setInterval(() => this.pollGameState(), 5000);
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

    render() {
        const showSuggestionModal = () => {
            this.setState({ showSuggestModal: true });
        }
        const hideSuggestionModal = () => {
            this.setState({ showSuggestModal: false });
        }
        const showSecondarySuggestionModal = () => {
            this.setState({ showSecondarySuggestionModal: true });
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
                    <Carousel interval={null} indicators={false}>
                        {characters.map((character, idx) =>
                        (
                            <Carousel.Item className="carouselItem" id={idx}>
                                {character}
                            </Carousel.Item>
                        ))}
                    </Carousel>
                    <Carousel interval={null} indicators={false}>
                        {weapons.map((weapon, idx) =>
                        (
                            <Carousel.Item className="carouselItem" id={idx}>
                                {weapon}
                            </Carousel.Item>
                        ))}
                    </Carousel>
                    <Carousel interval={null} indicators={false}>
                        {rooms.map((room, idx) =>
                        (
                            <Carousel.Item className="carouselItem" id={idx}>
                                {room}
                            </Carousel.Item>
                        ))}
                    </Carousel>
                </Modal.Body>
                <Modal.Footer className="modalFooterButtons">
                    <Button variant="secondary" onClick={hideSuggestionModal}>
                        Cancel
                     </Button>
                    <Button variant="primary" onClick={hideSuggestionModal}>
                        Suggest
                    </Button>
                </Modal.Footer>
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
                    <Carousel interval={null} indicators={false}>
                        {characters.map((character, idx) =>
                        (
                            <Carousel.Item className="carouselItem" id={idx}>
                                {character}
                            </Carousel.Item>
                        ))}
                    </Carousel>
                    <Carousel interval={null} indicators={false}>
                        {weapons.map((weapon, idx) =>
                        (
                            <Carousel.Item className="carouselItem" id={idx}>
                                {weapon}
                            </Carousel.Item>
                        ))}
                    </Carousel>
                    <Carousel interval={null} indicators={false}>
                        {rooms.map((room, idx) =>
                        (
                            <Carousel.Item className="carouselItem" id={idx}>
                                {room}
                            </Carousel.Item>
                        ))}
                    </Carousel>
                </Modal.Body>
                <Modal.Footer className="modalFooterButtons">
                    <Button variant="secondary" onClick={hideAccusationModal}>
                        Cancel
                     </Button>
                    <Button variant="primary" onClick={hideAccusationModal}>
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

                    <Carousel interval={null} indicators={false}>
                        {TMP_PLAYER_CARDS.map((card, idx) =>
                        (
                            <Carousel.Item className="carouselItem" id={idx}>
                                {card}
                            </Carousel.Item>
                        ))}
                    </Carousel>
                    <div className="secondarySuggestionInstructions" >
                        Choose a card to disprove the suggesiton
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooterButtons">
                    <Button variant="primary" onClick={hideSecondarySuggestionModal}>
                        Show Card
                    </Button>
                </Modal.Footer>
            </Modal >
        );

        const gameBoard = (
            <Card id="game">
                { <GameBoard gameState={this.getGameState} />}
            </Card >
        )

        const updatesContainer = (
            <div className="row">
                < div className="col d-flex justify-content-center" >
                    <Card id="updatesContainer">
                        <Card.Header className="justify-content-center d-flex" style={{ width: "100%" }}>Game Updates</Card.Header>
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
                        {secondarySuggestionModal}
                    </div>
                    <div className="container">
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

                <div id="suggestButton2" className="col d-flex justify-content-center">
                    <Button className="actionButton"
                        onClick={showSecondarySuggestionModal}>Suggestion (2)</Button>
                </div>


                <div id="endTurnButton" className="col d-flex justify-content-center">
                    <Button className="actionButton"
                    //    onClick={window.endTurn()}
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
                            {gameBoard}
                        </div>
                        <div className="col-md-5" >
                            <div className="container">
                                {updatesContainer}
                                {cards}
                                {accuseSuggestEndTurn}
                            </div >
                        </div >
                    </div >
                </div >
            </div>
        )
    }
}
export default Game;