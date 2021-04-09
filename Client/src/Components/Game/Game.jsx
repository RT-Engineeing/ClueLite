import './Game.css'
import React from 'react';
import Card from 'react-bootstrap/Card'
import Button from 'react-bootstrap/Button'
import GameBoard from '../GameBoard/GameBoard';
import 'bootstrap/dist/css/bootstrap.min.css';

const TMP_PLAYER_CARDS = [
    "CARD 1", "CARD 2", "CARD 3", "CARD 4", "CARD 5"
];

export class Game extends React.Component {
    render() {
        return (
            <div className="d-flex justify-content-center" style={{ minWidth: '1800px' }}>
                <div id="gamePageContainer" className="container-fluid">
                    <div className="row">
                        <div className="col-md-5" style={{ maxHeight: '710px' }} >
                            <Card id="game" text="white">
                                {<GameBoard />}
                            </Card >
                        </div>
                        <div className="col-md-5" style={{ maxHeight: '710px' }}>
                            <div className="container">
                                <div id="gameUpdatesContainer" className="row">
                                    <div className="col d-flex justify-content-center">
                                        <Card id="updatesContainer" text="white">
                                            <Card.Header className="justify-content-center d-flex" style={{ width: "100%" }}>Game Updates</Card.Header>
                                        </Card >
                                    </div>
                                </div>
                                {/* Currently, some elements do not scale properly with page resizing. This should be fixed in the target increment */}
                                <div id="cards" className="row">
                                    <div className="col d-flex justify-content-center">
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
                                <div id="accuseSuggest" className="row">
                                    <div id="suggestButton" className="col d-flex justify-content-center">
                                        <Button className="actionButton">Suggest</Button>
                                    </div>
                                    <div id="accuseButton" className="col d-flex justify-content-center">
                                        <Button className="actionButton">Accuse</Button>
                                    </div>
                                </div>
                            </div >
                        </div >
                    </div >
                </div >
            </div>
        )
    }
}
export default Game;