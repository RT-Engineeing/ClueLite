import './Game.css'
import React from 'react';
import Card from 'react-bootstrap/Card'
import Button from 'react-bootstrap/Button'
import GameBoard from '../GameBoard/GameBoard';
import Modal from 'react-bootstrap/Modal'
import Carousel from 'react-bootstrap/Carousel'
import 'bootstrap/dist/css/bootstrap.min.css';
import { characters, weapons, rooms, cardImages } from '../../Cards/Cards';

const TMP_PLAYER_CARDS = [
    "exodiaRightArm", "exodiaBody", "exodiaLeftArm", "exodiaRightLeg", "exodiaLeftLeg"
];

export class Game extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            showSuggestModal: false,
            showAccusationModal: false,
            showSecondarySuggestionModal: false
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
                        {characters.map((character) =>
                        (
                            <Carousel.Item className="carouselItem">
                                {character}
                            </Carousel.Item>
                        ))}
                    </Carousel>
                    <Carousel interval={null} indicators={false}>
                        {weapons.map((weapon) =>
                        (
                            <Carousel.Item className="carouselItem">
                                {weapon}
                            </Carousel.Item>
                        ))}
                    </Carousel>
                    <Carousel interval={null} indicators={false}>
                        {rooms.map((room) =>
                        (
                            <Carousel.Item className="carouselItem">
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
                        {characters.map((character) =>
                        (
                            <Carousel.Item className="carouselItem">
                                {character}
                            </Carousel.Item>
                        ))}
                    </Carousel>
                    <Carousel interval={null} indicators={false}>
                        {weapons.map((weapon) =>
                        (
                            <Carousel.Item className="carouselItem">
                                {weapon}
                            </Carousel.Item>
                        ))}
                    </Carousel>
                    <Carousel interval={null} indicators={false}>
                        {rooms.map((room) =>
                        (
                            <Carousel.Item className="carouselItem">
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
                        {TMP_PLAYER_CARDS.map((card) =>
                        (
                            <Carousel.Item className="carouselItem">
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
                { <GameBoard />}
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
                                    <Card.Img src={cardImages[TMP_PLAYER_CARDS[0]]} />
                                    <Card.ImgOverlay>
                                    </Card.ImgOverlay>
                                </Card>
                            </div>
                            <div className="cardCol col" align="center">
                                <Card className="playerCard" align="center">
                                    <Card.Img src={cardImages[TMP_PLAYER_CARDS[1]]} />
                                    <Card.ImgOverlay>
                                    </Card.ImgOverlay>
                                </Card>
                            </div>
                            <div className="cardCol col" align="left">
                                <Card className="playerCard" align="center">
                                    <Card.Img src={cardImages[TMP_PLAYER_CARDS[2]]} />
                                    <Card.ImgOverlay>
                                    </Card.ImgOverlay>
                                </Card>
                            </div>
                        </div>
                        <div className="cardRow row">
                            <div className="cardCol col" align="right">
                                <Card className="playerCard" align="center">
                                    <Card.Img src={cardImages[TMP_PLAYER_CARDS[3]]} />
                                    <Card.ImgOverlay>
                                    </Card.ImgOverlay>
                                </Card>
                            </div>
                            <div className="cardCol col" align="left">
                                <Card className="playerCard" align="center">
                                    <Card.Img src={cardImages[TMP_PLAYER_CARDS[4]]} />
                                    <Card.ImgOverlay>
                                    </Card.ImgOverlay>
                                </Card>
                            </div>
                        </div>
                    </div>
                </div>
            </div >
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