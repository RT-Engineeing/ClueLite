import './Game.css'
import React from 'react';
import Card from 'react-bootstrap/Card'
import Button from 'react-bootstrap/Button'
import GameBoard from '../GameBoard/GameBoard';
import Modal from 'react-bootstrap/Modal'
import Carousel from 'react-bootstrap/Carousel'
import 'bootstrap/dist/css/bootstrap.min.css';

const TMP_PLAYER_CARDS = [
    "CARD 1", "CARD 2", "CARD 3", "CARD 4", "CARD 5"
];

const TMP_WEAPONS = [
    "Flamethrower", "Shuriken", "Poison", "Glitter Cannon", "Dark Magic"
]

const TMP_CHARACTERS = [
    "Jordan DeBarth", "Elon Musk", "Sam Schappelle", "Jeffery Garonzik", "Joe DeMasco", "Brian's Future Wife", "Mace Windu", "The Colonel"
]

const TMP_ROOMS = [
    "Popeyes",
    "Lockheed Martin HQ",
    "Boeing HQ",
    "Ft. Meade",
    "Alarm.com Zoom Meeting",
    "Sam's Doppleganger's Office"
]

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
                        {TMP_CHARACTERS.map((character) =>
                        (
                            <Carousel.Item className="carouselItem">
                                {character}
                            </Carousel.Item>
                        ))}
                    </Carousel>
                    <Carousel interval={null} indicators={false}>
                        {TMP_WEAPONS.map((weapon) =>
                        (
                            <Carousel.Item className="carouselItem">
                                {weapon}
                            </Carousel.Item>
                        ))}
                    </Carousel>
                    <Carousel interval={null} indicators={false}>
                        {TMP_ROOMS.map((room) =>
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
                        {TMP_CHARACTERS.map((character) =>
                        (
                            <Carousel.Item className="carouselItem">
                                {character}
                            </Carousel.Item>
                        ))}
                    </Carousel>
                    <Carousel interval={null} indicators={false}>
                        {TMP_WEAPONS.map((weapon) =>
                        (
                            <Carousel.Item className="carouselItem">
                                {weapon}
                            </Carousel.Item>
                        ))}
                    </Carousel>
                    <Carousel interval={null} indicators={false}>
                        {TMP_ROOMS.map((room) =>
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
                    <div className="secondarySuggestionInstructions" >
                        Choose a card to disprove the suggesiton
                    </div>
                    <Carousel interval={null} indicators={false}>
                        {TMP_PLAYER_CARDS.map((card) =>
                        (
                            <Carousel.Item className="carouselItem">
                                {card}
                            </Carousel.Item>
                        ))}
                    </Carousel>
                </Modal.Body>
                <Modal.Footer className="modalFooterButtons">
                    <Button variant="secondary" onClick={hideSecondarySuggestionModal}>
                        Pass
                     </Button>
                    <Button variant="primary" onClick={hideSecondarySuggestionModal}>
                        Show Card
                    </Button>
                </Modal.Footer>
            </Modal >
        );

        const gameBoard = (
            <Card id="game" text="white">
                {<GameBoard />}
            </Card >
        )

        const updatesContainer = (
            <div id="gameUpdatesContainer" className="row">
                <div className="col d-flex justify-content-center">
                    <Card id="updatesContainer" text="white">
                        <Card.Header className="justify-content-center d-flex" style={{ width: "100%" }}>Game Updates</Card.Header>
                    </Card >
                </div>
            </div>
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
                                <Card className="playerCard" text="black" align="center">
                                    {TMP_PLAYER_CARDS[0]}
                                </Card>
                            </div>
                            <div className="cardCol col" align="center">
                                <Card className="playerCard" text="black" align="center">
                                    {TMP_PLAYER_CARDS[1]}
                                </Card>
                            </div>
                            <div className="cardCol col" align="left">
                                <Card className="playerCard" text="black" align="center">
                                    {TMP_PLAYER_CARDS[2]}
                                </Card>
                            </div>
                        </div>
                        <div className="cardRow row">
                            <div className="cardCol col" align="right">
                                <Card className="playerCard" text="black" align="center">
                                    {TMP_PLAYER_CARDS[3]}
                                </Card>
                            </div>
                            <div className="cardCol col" align="left">
                                <Card className="playerCard" text="black" align="center">
                                    {TMP_PLAYER_CARDS[4]}
                                </Card>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );

        const accuseSuggest = (
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
                        onClick={showSecondarySuggestionModal}>TMP</Button>
                </div>
            </div>
        );

        return (
            <div className="d-flex justify-content-center" style={{ minWidth: '1800px' }}>
                <div id="gamePageContainer" className="container-fluid">
                    <div className="row">
                        <div className="col-md-5" style={{ maxHeight: '710px' }} >
                            {gameBoard}
                        </div>
                        <div className="col-md-5" style={{ maxHeight: '710px' }}>
                            <div className="container">
                                {updatesContainer}
                                {/* Currently, some elements do not scale properly with page resizing. This should be fixed in the target increment */}
                                {cards}
                                {accuseSuggest}
                            </div >
                        </div >
                    </div >
                </div >
            </div>
        )
    }
}
export default Game;