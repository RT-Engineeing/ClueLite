import './Game.css'
import React from 'react';
import Card from 'react-bootstrap/Card'
import Button from 'react-bootstrap/Button'
import 'bootstrap/dist/css/bootstrap.min.css';

export class Game extends React.Component {
    render() {
        return (
            <div class="d-flex justify-content-center">
                <div id="gamePageContainer" className="container" align="center">
                    <div className="row">
                        <div className="col">
                            <div id="gameBoardContainer" className="container text-center">
                                <div className="row">
                                    <div className="col">
                                        <Card id="game" text="white">
                                        </Card >
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="col">
                            <div className="container">
                                <div id="gameUpdatesContainer" className="row ">
                                    <div className="col d-flex justify-content-center">
                                        <Card id="updatesContainer" text="white">
                                            <Card.Header className="justify-content-center d-flex" style={{ width: "100%" }}>Game Updates</Card.Header>
                                            <div>
                                            </div>
                                        </Card >
                                    </div>
                                </div>
                                <div id="cards" className="row">
                                    <div className="col d-flex justify-content-center">
                                        <div className="container">
                                            <div className="cardRow row">
                                                <div className="cardCol col" align="right">
                                                    <Card className="playerCard" text="white">
                                                        Card1
                                                </Card>
                                                </div>
                                                <div className="cardCol col" align="center">
                                                    <Card className="playerCard" text="white">
                                                        Card2
                                                </Card>
                                                </div>
                                                <div className="cardCol col" align="left">
                                                    <Card className="playerCard" text="white">
                                                        Card3
                                                </Card>
                                                </div>
                                            </div>
                                            <div className="cardRow row">
                                                <div className="cardCol col" align="right">
                                                    <Card className="playerCard" text="white">
                                                        Card4
                                                </Card>
                                                </div>
                                                <div className="cardCol col" align="left">
                                                    <Card className="playerCard" text="white">
                                                        Card5
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
                </div>
            </div>
        )
    }
}
export default Game;